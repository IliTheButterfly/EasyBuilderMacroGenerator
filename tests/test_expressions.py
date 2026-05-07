"""Tests for expression rendering: comparisons, arithmetic, AND/OR/NOT, EVAL,
LITERAL, and the ``deboolify`` helper.

These cover the forward-direction operator overloads on ``Variable`` and
``EXPRESSION`` (the reverse operators are covered by
``test_reverse_operators.py``).
"""
import pytest

from eb_macro_gen.syntax import (
    AND,
    EVAL,
    LITERAL,
    NOT,
    OR,
    deboolify,
    vbool,
    vint,
    vint_arr,
)


# ---------- deboolify --------------------------------------------------------

def test_deboolify_passes_through_none():
    assert deboolify(None) is None


def test_deboolify_converts_bools_to_ints():
    assert deboolify(True) == 1
    assert deboolify(False) == 0


def test_deboolify_leaves_other_values_untouched():
    assert deboolify(0) == 0
    assert deboolify(3.14) == 3.14
    assert deboolify("hi") == "hi"


# ---------- comparison operators on Variable --------------------------------

def test_variable_comparison_operators_render():
    a = vint("a")
    assert str(a == 1) == "a == 1"
    assert str(a != 2) == "a <> 2"
    assert str(a < 3) == "a < 3"
    assert str(a <= 4) == "a <= 4"
    assert str(a > 5) == "a > 5"
    assert str(a >= 6) == "a >= 6"


def test_variable_eq_uses_eb_inequality_operator():
    """EasyBuilder uses ``<>`` for not-equal, not ``!=``."""
    a = vint("a")
    rendered = str(a != 0)
    assert "<>" in rendered
    assert "!=" not in rendered


def test_variable_eq_against_bool_is_normalized_to_int():
    a = vbool("a")
    assert str(a == True) == "a == 1"   # noqa: E712 -- testing operator overload
    assert str(a == False) == "a == 0"  # noqa: E712


def test_variable_all_comparison_ops_normalize_bool_literals():
    a = vbool("a")
    assert str(a != True) == "a <> 1"   # noqa: E712
    assert str(a < True) == "a < 1"     # noqa: E712
    assert str(a <= False) == "a <= 0"  # noqa: E712
    assert str(a > True) == "a > 1"     # noqa: E712
    assert str(a >= False) == "a >= 0"  # noqa: E712


@pytest.mark.xfail(
    reason=(
        "VariableItem.__eq__/__ne__/__lt__/__le__/__gt__/__ge__ render with "
        "{self.array.name} instead of {self}, so the [index] is dropped. "
        "Tracked as a follow-up — VariableItem arithmetic ops correctly "
        "include the index (see test_reverse_operators_variable_item)."
    ),
    strict=True,
)
def test_variable_item_comparison_includes_index():
    item = vint_arr("arr", 3)[0]
    assert str(item == 1) == "arr[0] == 1"
    assert str(item == True) == "arr[0] == 1"  # noqa: E712


def test_variable_item_comparison_normalizes_bool():
    """The deboolify fix applies here even though the index is dropped — the
    bool literal still becomes 0/1 instead of True/False."""
    item = vint_arr("arr", 3)[0]
    rendered = str(item == True)  # noqa: E712
    assert rendered.endswith("== 1")
    assert "True" not in rendered


def test_expression_comparison_ops_normalize_bool_literals():
    expr = EVAL("FN", 1)
    assert str(expr == True) == "FN(1) == 1"   # noqa: E712
    assert str(expr != False) == "FN(1) <> 0"  # noqa: E712


# ---------- forward arithmetic operators ------------------------------------

def test_variable_forward_arithmetic_operators():
    a = vint("a")
    assert str(a + 1) == "a + 1"
    assert str(a - 2) == "a - 2"
    assert str(a * 3) == "a * 3"
    assert str(a / 4) == "a / 4"
    assert str(a % 5) == "a % 5"


def test_variable_item_forward_arithmetic_operators():
    item = vint_arr("arr", 4)[2]
    assert str(item + 1) == "arr[2] + 1"
    assert str(item * 7) == "arr[2] * 7"


# ---------- AND / OR / NOT ---------------------------------------------------

def test_and_renders_with_lowercase_keyword_and_parens():
    a = vbool("a")
    b = vbool("b")
    assert str(a & b) == "(a and b)"


def test_or_renders_with_lowercase_keyword_and_parens():
    a = vbool("a")
    b = vbool("b")
    assert str(a | b) == "(a or b)"


def test_chained_and_collapses_to_a_single_and_expression():
    """``AND & AND`` should flatten into a single ``AND(...)``."""
    a, b, c = vbool("a"), vbool("b"), vbool("c")
    expr = AND(a, b) & AND(c, vbool("d"))
    assert isinstance(expr, AND)
    assert str(expr) == "(a and b and c and d)"


def test_chained_or_collapses_to_a_single_or_expression():
    a, b, c = vbool("a"), vbool("b"), vbool("c")
    expr = OR(a, b) | OR(c, vbool("d"))
    assert isinstance(expr, OR)
    assert str(expr) == "(a or b or c or d)"


def test_not_wraps_with_lowercase_keyword():
    a = vbool("a")
    expr = ~a
    assert isinstance(expr, NOT)
    assert str(expr) == "(not a)"


def test_double_not_returns_inner_expression():
    """NOT.__invert__ should peel back to the wrapped expression rather than
    nest another NOT."""
    a = vbool("a")
    inner = ~a
    assert str(~inner) == "a"


# ---------- EVAL / LITERAL ---------------------------------------------------

def test_eval_renders_function_call_with_args():
    expr = EVAL("MAX", 1, 2, vint("x"))
    assert str(expr) == "MAX(1, 2, x)"


def test_eval_normalizes_bool_args_to_ints():
    expr = EVAL("FN", True, False)
    assert str(expr) == "FN(1, 0)"


def test_literal_renders_verbatim():
    assert str(LITERAL("LB-100 == 1")) == "LB-100 == 1"


# ---------- expression-on-expression composition ----------------------------

def test_eq_against_eval_renders_both_sides():
    a = vint("a")
    rendered = str(a == EVAL("FN", 1))
    assert rendered == "a == FN(1)"


def test_and_handles_a_variable_bool_via_as_literal():
    """Regression for a previous ``__and__`` shadowing bug: variables of bool
    type must still be wrapped via ``as_literal`` rather than dropped."""
    a = vbool("a")
    expr = (a == 1) & a
    # The variable side should be rendered as its name (via ``as_literal``).
    assert str(expr) == "(a == 1 and a)"
