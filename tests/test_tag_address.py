"""Address parsing on Tag — the parsed properties used to swallow all
exceptions from ``str.split`` / ``int``. Now they raise on internal bugs
and only swallow the documented parse failures.
"""
from eb_macro_gen.objects import DataType, Tag


def test_address_register_and_num_for_typical_addresses():
    t = Tag("t", "PLC", "LW,42", DataType.S16)
    assert t.address_register == "LW"
    assert t.address_num == 42


def test_address_register_returns_whole_string_when_no_comma():
    t = Tag("t", "PLC", "LW", DataType.Bit)
    assert t.address_register == "LW"
    assert t.address_num is None


def test_address_num_is_none_for_non_integer_suffix():
    t = Tag("t", "PLC", "LW,abc", DataType.S16)
    assert t.address_num is None
    assert t.address_register == "LW"
