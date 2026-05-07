"""Tests for ``Variable``, ``VariableArray`` and ``VariableItem`` rendering
and bounds-checking."""
import pytest

from eb_macro_gen.syntax import (
    VariableArray,
    vbool,
    vfloat,
    vint,
    vint_arr,
    vshort,
)


# ---------- declare strings -------------------------------------------------

def test_variable_declare_without_default():
    assert vint("a").declare() == "int a"
    assert vshort("b").declare() == "short b"


def test_variable_declare_with_default():
    assert vint("a", 7).declare() == "int a = 7"
    assert vfloat("f", 3.5).declare() == "float f = 3.5"


def test_vbool_default_is_normalized_to_int():
    """``deboolify`` should turn the bool default into 0/1 so the
    declaration is valid EasyBuilder syntax."""
    assert vbool("flag", True).declare() == "bool flag = 1"
    assert vbool("flag", False).declare() == "bool flag = 0"


def test_variable_str_returns_name():
    assert str(vint("answer")) == "answer"


# ---------- VariableArray ---------------------------------------------------

def test_variable_array_declare_without_default():
    arr = vint_arr("xs", 4)
    assert arr.declare() == "int xs[4]"


def test_variable_array_declare_with_default():
    arr = vint_arr("xs", 3, [1, 2, 3])
    assert arr.declare() == "int xs[3] = { 1, 2, 3 }"


def test_variable_array_default_normalizes_bools():
    arr = VariableArray("flags", "bool", 2, [True, False])
    assert arr.declare() == "bool flags[2] = { 1, 0 }"


def test_variable_array_indexing_returns_a_variable_item():
    arr = vint_arr("xs", 4)
    item = arr[2]
    assert str(item) == "xs[2]"


def test_variable_array_indexing_supports_variable_index():
    arr = vint_arr("xs", 4)
    i = vint("i")
    assert str(arr[i]) == "xs[i]"


def test_variable_array_getitem_rejects_out_of_range_int():
    arr = vint_arr("xs", 3)
    with pytest.raises(IndexError):
        _ = arr[10]


def test_variable_array_setitem_rejects_negative_int():
    arr = vint_arr("xs", 3)
    with pytest.raises(IndexError):
        arr[-1] = 0


# ---------- VariableItem ----------------------------------------------------

def test_variable_item_set_renders_assignment():
    arr = vint_arr("xs", 4)
    stmt = arr[1].set(99)
    assert str(stmt) == "xs[1] = 99\n"


def test_variable_item_set_normalizes_bool_value():
    arr = vint_arr("xs", 2)
    stmt = arr[0].set(True)
    assert str(stmt) == "xs[0] = 1\n"


def test_variable_set_renders_assignment_with_variable_rhs():
    a = vint("a")
    b = vint("b")
    assert str(a.set(b)) == "a = b\n"


def test_variable_set_with_expression_rhs():
    a = vint("a")
    assert str(a.set(a + 1)) == "a = a + 1\n"
