"""Tests for ``EasyBuilderTag`` and ``EasyBuilderTagList`` (CSV I/O)."""
import io
from pathlib import Path

from eb_macro_gen.objects import (
    DataType,
    EasyBuilderTag,
    EasyBuilderTagList,
)


TAGS_DIR = Path(__file__).parent / "tags"


# ---------- EasyBuilderTag ---------------------------------------------------

def test_easybuilder_tag_to_tag_round_trips_data_type():
    tag = EasyBuilderTag("V1", "Local HMI", "LW, 200", "V1 value", "16-bit Signed")
    converted = tag.to_tag()
    assert converted.dtype is DataType.S16
    assert converted.name == "V1"
    assert converted.address == "LW, 200"


def test_easybuilder_tag_to_tag_for_32_bit_signed():
    """Regression for the previous DT_EB_MAP bug — S32 must round-trip."""
    tag = EasyBuilderTag("BIG", "Local HMI", "LW, 200", "", "32-bit Signed")
    assert tag.to_tag().dtype is DataType.S32


def test_easybuilder_tag_export_quotes_comments_with_commas():
    tag = EasyBuilderTag("V1", "Local HMI", "LW, 200", "hello, world", "16-bit Signed")
    line = tag.export()
    assert '"hello, world"' in line
    assert line.startswith("V1,Local HMI,LW, 200,")
    assert line.endswith(",16-bit Signed")


def test_easybuilder_tag_export_leaves_simple_comment_unquoted():
    tag = EasyBuilderTag("V1", "Local HMI", "LW, 200", "simple", "16-bit Signed")
    assert tag.export() == "V1,Local HMI,LW, 200,simple,16-bit Signed"


# ---------- EasyBuilderTagList ----------------------------------------------

def test_tag_list_reads_fixture_csv():
    lst = EasyBuilderTagList()
    with (TAGS_DIR / "hmi_tags0.csv").open() as f:
        lst.read(f)
    # The fixture has 30 tags.
    assert len(lst.map) == 30
    v1 = lst.map.get_from_key2("V1")
    assert v1 is not None
    # smart_split strips whitespace from each part, so "LW, 200" round-trips
    # to "LW,200".
    assert v1.Address == "LW,200"
    assert v1.Type == "16-bit Signed"


def test_tag_list_add_rejects_duplicate_name_or_address():
    lst = EasyBuilderTagList()
    base = EasyBuilderTag("V1", "Local HMI", "LW, 200", "", "16-bit Signed")
    assert lst.add(base) is True
    # Same address+host, different name -> rejected.
    assert lst.add(EasyBuilderTag("OTHER", "Local HMI", "LW, 200", "", "16-bit Signed")) is False
    # Same name, different address -> rejected.
    assert lst.add(EasyBuilderTag("V1", "Local HMI", "LW, 999", "", "16-bit Signed")) is False
    # Disjoint -> accepted.
    assert lst.add(EasyBuilderTag("V2", "Local HMI", "LW, 999", "", "16-bit Signed")) is True


def test_tag_list_round_trip_through_csv():
    """Reading a CSV, writing it out, and reading it back must preserve
    every tag (modulo unspecified order)."""
    original = EasyBuilderTagList()
    with (TAGS_DIR / "hmi_tags0.csv").open() as f:
        original.read(f)

    buf = io.StringIO()
    original.write(buf)
    buf.seek(0)

    re_read = EasyBuilderTagList()
    re_read.read(buf)

    assert len(re_read.map) == len(original.map)
    for _, name, tag in original.map:
        round_tripped = re_read.map.get_from_key2(name)
        assert round_tripped is not None, name
        assert round_tripped.Address == tag.Address
        assert round_tripped.Host == tag.Host
        assert round_tripped.Type == tag.Type


def test_tag_list_contains_checks_name_and_address():
    lst = EasyBuilderTagList()
    tag = EasyBuilderTag("V1", "Local HMI", "LW, 200", "", "16-bit Signed")
    lst.add(tag)
    assert tag in lst
    # An unrelated tag is not contained.
    assert EasyBuilderTag("UNK", "Local HMI", "LW, 999", "", "16-bit Signed") not in lst
    # Non-EasyBuilderTag objects are simply not contained.
    assert "V1" not in lst
