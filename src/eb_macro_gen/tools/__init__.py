"""eb_macro_gen.tools — Tag import/export, merge, and conflict reporting utilities.

Public API
----------
from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags, load_koyo_tags
from eb_macro_gen.tools.merge import merge_eb_tags, merge_eb_tags_interactive, ConflictStrategy, MergeResult
from eb_macro_gen.tools.reporting import ConflictReport
"""

from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags, load_koyo_tags
from eb_macro_gen.tools.merge import (
    merge_eb_tags,
    merge_eb_tags_interactive,
    ConflictStrategy,
    MergeResult,
)
from eb_macro_gen.tools.reporting import ConflictReport

__all__ = [
    "load_eb_tags",
    "save_eb_tags",
    "load_koyo_tags",
    "merge_eb_tags",
    "merge_eb_tags_interactive",
    "ConflictStrategy",
    "MergeResult",
    "ConflictReport",
]