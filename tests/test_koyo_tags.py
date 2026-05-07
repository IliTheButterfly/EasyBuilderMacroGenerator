"""Tests for the Koyo PLC tag list and KoyoTag -> Tag conversion."""
from pathlib import Path

from eb_macro_gen.objects import DataType
from eb_macro_gen.plcs.koyo import (
    EB_KOYO_TYPE_MAP,
    KOYO_EB_TYPE_MAP,
    KoyoTag,
    KoyoTagList,
)


TAGS_DIR = Path(__file__).parent / "tags"
DEVICE = "KOYO CLICK V3 MODBUS TCP/IP"


def test_koyo_eb_type_maps_are_inverse():
    for koyo_type, eb_type in KOYO_EB_TYPE_MAP.items():
        assert EB_KOYO_TYPE_MAP[eb_type] == koyo_type, koyo_type


def test_koyo_tag_to_tag_for_int_yields_signed_short_data_type():
    tag = KoyoTag("DS1", "INT", "Time1", 0, True, "")
    converted = tag.to_tag(DEVICE)
    assert converted.dtype is DataType.S16
    assert converted.name == "Time1"
    assert converted.address == "DS1"
    assert converted.device_name == DEVICE


def test_koyo_tag_to_tag_for_int2_yields_signed_long_data_type():
    """Regression for the prior DT_EB_MAP bug — Koyo INT2 must reach S32."""
    tag = KoyoTag("DD1", "INT2", "BigNumber", 0, True, "")
    assert tag.to_tag(DEVICE).dtype is DataType.S32


def test_koyo_tag_to_tag_for_float_yields_f32_data_type():
    tag = KoyoTag("DF1", "FLOAT", "Value1", 0.0, False, "")
    assert tag.to_tag(DEVICE).dtype is DataType.F32


def test_koyo_tag_to_tag_for_bit_yields_bit_data_type():
    tag = KoyoTag("X001", "BIT", "BitIN1", 0, False, "")
    assert tag.to_tag(DEVICE).dtype is DataType.Bit


def test_koyo_tag_list_skips_header_when_reading_csv():
    lst = KoyoTagList()
    with (TAGS_DIR / "koyo_tags.csv").open() as f:
        lst.read(f)
    # Header line ("Address,Data Type,...") must not appear as a tag.
    assert lst.map.get_from_key2("Nickname") is None
    # Sanity check on a few known nicknames from the fixture.
    assert lst.map.get_from_key2("BitIN1") is not None
    assert lst.map.get_from_key2("Timer1_dn") is not None
    assert lst.map.get_from_key2("Value1") is not None


def test_koyo_tag_list_round_trip_to_eb_tag():
    lst = KoyoTagList()
    with (TAGS_DIR / "koyo_tags.csv").open() as f:
        lst.read(f)

    bit_in_1 = lst.map.get_from_key2("BitIN1")
    assert bit_in_1 is not None
    converted = bit_in_1.to_tag(DEVICE)
    assert converted.dtype is DataType.Bit
    assert converted.address == "X001"

    value_1 = lst.map.get_from_key2("Value1")
    assert value_1.to_tag(DEVICE).dtype is DataType.F32
