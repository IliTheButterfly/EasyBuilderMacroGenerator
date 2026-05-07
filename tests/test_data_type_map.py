"""Tests covering the DataType <-> EasyBuilder string mapping.

The previous map duplicated ``"16-bit Signed"`` for both S16 and S32, so
S32 round-tripped to the wrong DataType and S16 lookup was unreachable.
"""
from eb_macro_gen.objects import DT_EB_MAP, EB_DT_MAP, DataType


def test_each_datatype_has_a_unique_string():
    strings = list(DT_EB_MAP.values())
    assert len(strings) == len(set(strings)), strings


def test_signed_types_round_trip():
    assert DT_EB_MAP[DataType.S16] == "16-bit Signed"
    assert DT_EB_MAP[DataType.S32] == "32-bit Signed"
    assert EB_DT_MAP["16-bit Signed"] is DataType.S16
    assert EB_DT_MAP["32-bit Signed"] is DataType.S32


def test_round_trip_all_mapped_datatypes():
    for dt, s in DT_EB_MAP.items():
        assert EB_DT_MAP[s] is dt
