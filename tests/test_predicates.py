"""Tests for the ``is_int`` and ``is_float`` type predicates."""
from eb_macro_gen.objects import DataType, Tag, is_float, is_int
from eb_macro_gen.syntax import vfloat, vint, vint_arr


# ---------- DataType --------------------------------------------------------

def test_is_int_recognizes_integer_data_types():
    for dt in (
        DataType.BCD16, DataType.BCD32,
        DataType.U16, DataType.S16,
        DataType.U32, DataType.S32,
        DataType.U64, DataType.S64,
    ):
        assert is_int(dt), dt
        assert not is_float(dt), dt


def test_is_float_recognizes_float_data_types():
    for dt in (DataType.F32, DataType.F64):
        assert is_float(dt), dt
        assert not is_int(dt), dt


def test_bit_and_undesignated_are_neither_int_nor_float():
    for dt in (DataType.Bit, DataType.Undesignated):
        assert not is_int(dt)
        assert not is_float(dt)


# ---------- string dtype ----------------------------------------------------

def test_is_int_recognizes_c_int_type_strings():
    for s in ("char", "unsigned char", "short", "unsigned short",
              "int", "unsigned int", "long", "unsigned long"):
        assert is_int(s), s


def test_is_float_recognizes_c_float_type_strings():
    assert is_float("float")
    assert is_float("double")


def test_string_predicates_do_not_cross_categories():
    assert not is_float("int")
    assert not is_int("float")
    assert not is_int("bool")
    assert not is_float("bool")


# ---------- Variable / VariableItem / Tag ----------------------------------

def test_is_int_on_integer_variable():
    assert is_int(vint("a"))
    assert not is_float(vint("a"))


def test_is_float_on_float_variable():
    assert is_float(vfloat("f"))
    assert not is_int(vfloat("f"))


def test_is_int_on_integer_variable_item():
    arr = vint_arr("xs", 3)
    assert is_int(arr[0])
    assert not is_float(arr[0])


def test_is_int_on_integer_tag():
    t = Tag("t", "PLC", "LW,1", DataType.S16)
    assert is_int(t)
    assert not is_float(t)


def test_is_float_on_float_tag():
    t = Tag("f", "PLC", "LW,1", DataType.F32)
    assert is_float(t)
    assert not is_int(t)


# ---------- Python primitives -----------------------------------------------

def test_is_int_on_python_ints_and_is_float_on_python_floats():
    assert is_int(7)
    assert is_float(3.14)
    assert not is_int(3.14)
    assert not is_float(7)
