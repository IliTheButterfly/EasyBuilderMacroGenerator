import io

from src.eb_macro_gen.instructions import ACOS, ASYNC_TRIG_MACRO, BCD2BIN
from src.eb_macro_gen.syntax import C_ELIF, C_END_IF, C_IF, C_ELSE, COMMENT, IF, Macro, vfloat, vint, vshort


def render_macro(macro: Macro) -> str:
    stream = io.StringIO()
    macro.display(io=stream)
    return stream.getvalue()


def test_issue_2_c_if_c_elif_declares_condition_variable():
    macro = Macro("test_c_ifs")

    with macro:
        var1 = vint("var1")

        for i in range(3):
            macro.write(C_IF(var1 == i) if i == 0 else C_ELIF(var1 == i))
            macro.write(COMMENT(f"Case {i}"))

        macro.write(C_ELSE(), COMMENT("Case Else"), C_END_IF())

    output = render_macro(macro)

    assert "int var1" in output
    assert "if var1 == 0 then" in output
    assert "else if var1 == 1 then" in output
    assert "else if var1 == 2 then" in output


def test_if_elif_builder_declares_variable_used_only_in_condition():
    macro = Macro("test_if_elif")

    with macro:
        selector = vshort("selector")
        macro.write(
            IF(selector == 0)(
                COMMENT("zero"),
            ).ELIF(selector == 1)(
                COMMENT("one"),
            ).ELSE()(
                COMMENT("other"),
            )
        )

    output = render_macro(macro)

    assert "short selector" in output
    assert "if selector == 0 then" in output
    assert "else if selector == 1 then" in output


def test_instruction_calls_render_and_track_variables():
    macro = Macro("instructions")

    with macro:
        source = vfloat("source", 0.5)
        trig_result = vfloat("trig_result")
        packed = vshort("packed", 0x1234)
        unpacked = vshort("unpacked")

        macro.write(
            ACOS(source, trig_result),
            BCD2BIN(packed, unpacked),
            ASYNC_TRIG_MACRO("next_macro"),
        )

    output = render_macro(macro)

    assert 'ASYNC_TRIG_MACRO("next_macro")' in output
    assert "ACOS(source, trig_result)" in output
    assert "BCD2BIN(packed, unpacked)" in output
    assert "float source = 0.5" in output
    assert "short packed = 4660" in output
