from pathlib import Path
from typing import Optional

from eb_macro_gen.tools.combine_tags import main as combine_tags_main
from eb_macro_gen.tools.io import load_eb_tags
from eb_macro_gen.tools.koyo_tags_import import main as koyo_tags_import_main


TEST_TAGS_DIR = Path(__file__).parent / "tags"
KOYO_DEVICE = "KOYO CLICK V3 MODBUS TCP/IP"


def _run_combine(base: Path, incoming: Path, output: Path) -> None:
    import sys

    prev_argv = sys.argv
    sys.argv = [
        "combine_tags",
        str(base),
        str(incoming),
        str(output),
        "--force",
        "--strategy",
        "skip",
    ]
    try:
        combine_tags_main()
    finally:
        sys.argv = prev_argv


def _run_koyo_import(koyo_csv: Path, output: Path, append: Optional[Path] = None) -> None:
    import sys

    args = [
        "koyo_tags_import",
        str(koyo_csv),
        str(output),
        KOYO_DEVICE,
        "--force",
        "--strategy",
        "skip",
    ]

    if append is not None:
        args.extend(["--append", str(append)])

    prev_argv = sys.argv
    sys.argv = args
    try:
        koyo_tags_import_main()
    finally:
        sys.argv = prev_argv


def test_combine_hmi_tags0_with_hmi_tags1(tmp_path):
    output = tmp_path / "combined.csv"

    _run_combine(TEST_TAGS_DIR / "hmi_tags0.csv", TEST_TAGS_DIR / "hmi_tags1.csv", output)

    combined = load_eb_tags(output)

    assert len(list(combined.map)) == 47
    assert combined.map.get_from_key2("C1").Address == "LW,400"
    assert combined.map.get_from_key2("D1") is None
    assert combined.map.get_from_key2("F10").Address == "LW,609"


def test_convert_koyo_tags_into_hmi_tags(tmp_path):
    output = tmp_path / "koyo_as_hmi.csv"

    _run_koyo_import(TEST_TAGS_DIR / "koyo_tags.csv", output)

    converted = load_eb_tags(output)

    assert len(list(converted.map)) == 14
    assert converted.map.get_from_key2("BitIN1").Address == "X,001"
    assert converted.map.get_from_key2("Timer2_dn").Address == "T,2"
    assert converted.map.get_from_key2("Value2").Type == "32-bit Float"


def test_import_koyo_tags_into_hmi_tags0(tmp_path):
    output = tmp_path / "koyo_into_hmi0.csv"

    _run_koyo_import(
        TEST_TAGS_DIR / "koyo_tags.csv",
        output,
        append=TEST_TAGS_DIR / "hmi_tags0.csv",
    )

    merged = load_eb_tags(output)

    assert len(list(merged.map)) == 44
    assert merged.map.get_from_key2("V1").Address == "LW,200"
    assert merged.map.get_from_key2("BitOUT2").Address == "Y,002"


def test_import_koyo_tags_into_hmi_tags1(tmp_path):
    output = tmp_path / "koyo_into_hmi1.csv"

    _run_koyo_import(
        TEST_TAGS_DIR / "koyo_tags.csv",
        output,
        append=TEST_TAGS_DIR / "hmi_tags1.csv",
    )

    merged = load_eb_tags(output)

    assert len(list(merged.map)) == 44
    assert merged.map.get_from_key2("BitIN").Address == "X,001"
    assert merged.map.get_from_key2("BitIN2").Address == "X,002"


def test_import_koyo_tags_into_hmi_tags2(tmp_path):
    output = tmp_path / "koyo_into_hmi2.csv"

    _run_koyo_import(
        TEST_TAGS_DIR / "koyo_tags.csv",
        output,
        append=TEST_TAGS_DIR / "hmi_tags2.csv",
    )

    merged = load_eb_tags(output)

    assert len(list(merged.map)) == 14
    assert merged.map.get_from_key2("BitIN").Address == "X,001"
    assert merged.map.get_from_key2("BitIN2").Address == "X,002"
