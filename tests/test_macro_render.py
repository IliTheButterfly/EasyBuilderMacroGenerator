"""Strong rendering assertions for full Macro output.

The existing ``test_objects.py`` tests build complete macros but only call
``.display()`` for visual inspection — they don't assert on the output.
These tests render to a ``StringIO`` and assert structural properties of
the generated EasyBuilder code.
"""
import io

from eb_macro_gen.objects import DataType, ROUTINE, Tag
from eb_macro_gen.syntax import (
    BLOCK,
    CASE,
    COMMENT,
    EMPTY,
    IF,
    SWITCH,
    Macro,
    vbool,
    vint,
    vshort,
)


def _render(macro: Macro) -> str:
    out = io.StringIO()
    macro.display(io=out)
    return out.getvalue()


# ---------- header & lifecycle ----------------------------------------------

def test_macro_emits_macro_command_main_and_end_macro():
    m = Macro("simple")
    with m:
        m.write(COMMENT("hi"))
    rendered = _render(m)
    assert "macro_command main()" in rendered
    assert "end macro_command" in rendered


def test_macro_description_appears_as_comment():
    m = Macro("with_desc", "this is the description")
    with m:
        pass
    rendered = _render(m)
    assert "this is the description" in rendered


def test_variable_declarations_are_emitted_inside_the_macro_body():
    m = Macro("with_vars")
    with m:
        a = vint("a", 0)
        b = vbool("flag", True)
        m.write(a.set(1), b.set(0))
    rendered = _render(m)
    assert "int a = 0" in rendered
    assert "bool flag = 1" in rendered


# ---------- IF / ELIF / ELSE -------------------------------------------------

def test_if_elif_else_renders_as_a_chained_block():
    m = Macro("if_chain")
    with m:
        x = vint("x", 0)
        m.write(
            IF(x == 0)(
                COMMENT("zero"),
            ).ELIF(x == 1)(
                COMMENT("one"),
            ).ELSE()(
                COMMENT("other"),
            )
        )
    rendered = _render(m)
    assert "if x == 0 then" in rendered
    assert "else if x == 1 then" in rendered
    assert "else" in rendered
    assert "end if" in rendered
    # The else-branch comment must come after the elif comment.
    assert rendered.index("// one") < rendered.index("// other")


def test_if_without_else_still_emits_end_if():
    m = Macro("just_if")
    with m:
        x = vint("x", 0)
        m.write(IF(x == 0)(COMMENT("body")))
    rendered = _render(m)
    assert "if x == 0 then" in rendered
    assert "end if" in rendered


def test_nested_if_increments_indentation():
    m = Macro("nested")
    with m:
        x = vint("x", 0)
        m.write(
            IF(x == 0)(
                IF(x == 1)(
                    COMMENT("deep"),
                ),
            )
        )
    rendered = _render(m)
    # The inner comment should be indented more than the outer ``if`` keyword.
    deep_line = next(line for line in rendered.splitlines() if "// deep" in line)
    inner_if_line = next(line for line in rendered.splitlines() if "if x == 1 then" in line)
    outer_if_line = next(line for line in rendered.splitlines() if "if x == 0 then" in line)
    assert (len(inner_if_line) - len(inner_if_line.lstrip())) > (
        len(outer_if_line) - len(outer_if_line.lstrip())
    )
    assert (len(deep_line) - len(deep_line.lstrip())) > (
        len(inner_if_line) - len(inner_if_line.lstrip())
    )


# ---------- SWITCH / CASE ---------------------------------------------------

def test_switch_renders_first_case_as_if_and_rest_as_else_if():
    m = Macro("switch_demo")
    with m:
        sel = vshort("sel", 0)
        m.write(
            SWITCH(sel)(
                CASE(0)(COMMENT("zero")),
                CASE(1)(COMMENT("one")),
                CASE(2)(COMMENT("two")),
            )
        )
    rendered = _render(m)
    # First case becomes a plain ``if``, rest become ``else if``.
    assert "if sel == 0 then" in rendered
    assert rendered.count("else if sel ==") == 2
    assert "end if" in rendered


# ---------- ROUTINE ---------------------------------------------------------

def test_routine_emits_step_dispatch_and_increment():
    m = Macro("with_routine")
    with m:
        step_tag = Tag("step", "Local HMI", "LW,10", DataType.S16)
        m.write(
            ROUTINE("my_routine", step_tag, [
                BLOCK(COMMENT("step zero body")),
                BLOCK(COMMENT("step one body")),
                BLOCK(COMMENT("step two body")),
            ])
        )
    rendered = _render(m)
    # The routine should declare a step variable, dispatch on it, and reset
    # back to zero after the last step.
    assert "short my_routine_step" in rendered
    assert "if my_routine_step == 0 then" in rendered
    assert "else if my_routine_step == 1 then" in rendered
    assert "else if my_routine_step == 2 then" in rendered
    # Comment markers from the ROUTINE template.
    assert "START ROUTINE my_routine" in rendered
    assert "END ROUTINE my_routine" in rendered
    # Each step body must be present in order.
    z = rendered.index("step zero body")
    o = rendered.index("step one body")
    t = rendered.index("step two body")
    assert z < o < t


# ---------- write() input validation ----------------------------------------

def test_macro_write_rejects_non_statement():
    """``Macro.write`` raises SyntaxError when given an arbitrary object."""
    import pytest

    m = Macro("bad")
    with m, pytest.raises(SyntaxError):
        m.write("not a statement")  # type: ignore[arg-type]


def test_empty_renders_blank_line():
    """EMPTY() should produce a line break between the two comments. The
    line itself may carry indentation whitespace, but it must not contain
    the comment marker."""
    m = Macro("empties")
    with m:
        m.write(COMMENT("a"), EMPTY(), COMMENT("b"))
    rendered = _render(m)
    lines = rendered.splitlines()
    a_idx = next(i for i, line in enumerate(lines) if "// a" in line)
    b_idx = next(i for i, line in enumerate(lines) if "// b" in line)
    assert b_idx > a_idx + 1, "EMPTY should insert at least one line"
    blank_or_ws_only = [line for line in lines[a_idx + 1:b_idx] if line.strip() == ""]
    assert blank_or_ws_only, "expected a blank/whitespace-only line from EMPTY()"
