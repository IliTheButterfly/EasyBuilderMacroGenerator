"""Verify the curated public API surface exposed at the package root."""
import eb_macro_gen


def test_version_is_exposed():
    assert isinstance(eb_macro_gen.__version__, str)
    assert eb_macro_gen.__version__.count(".") >= 1


def test_top_level_re_exports_match_submodules():
    from eb_macro_gen import objects, syntax

    assert eb_macro_gen.Macro is syntax.Macro
    assert eb_macro_gen.IF is syntax.IF
    assert eb_macro_gen.vint is syntax.vint
    assert eb_macro_gen.Tag is objects.Tag
    assert eb_macro_gen.DataType is objects.DataType


def test_all_listed_exports_are_resolvable():
    missing = [name for name in eb_macro_gen.__all__ if not hasattr(eb_macro_gen, name)]
    assert missing == []
