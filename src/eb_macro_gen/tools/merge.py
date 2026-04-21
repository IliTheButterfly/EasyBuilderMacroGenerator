from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

from eb_macro_gen.objects import EasyBuilderTag, EasyBuilderTagList


class ConflictStrategy(Enum):
    """How to resolve conflicts when merging two tag lists.

    SKIP             Keep the existing tag; drop the incoming one (default / safe).
    REPLACE          Incoming tag wins on both address and name conflicts.
    REPLACE_ADDRESS  Incoming tag wins only when the address already exists.
    REPLACE_NAME     Incoming tag wins only when the name already exists.
    """
    SKIP = "skip"
    REPLACE = "replace"
    REPLACE_ADDRESS = "replace-address"
    REPLACE_NAME = "replace-name"


@dataclass
class MergeResult:
    """Summary of what happened during a merge."""
    added: int = 0
    skipped_address: int = 0
    skipped_name: int = 0
    replaced_address: int = 0
    replaced_name: int = 0
    # Per-tag detail: list of (tag, reason) for every non-trivial decision
    details: list = field(default_factory=list)

    @property
    def total_skipped(self) -> int:
        return self.skipped_address + self.skipped_name

    @property
    def total_replaced(self) -> int:
        return self.replaced_address + self.replaced_name

    def __str__(self) -> str:
        lines = [
            f"  Added:            {self.added}",
            f"  Replaced (addr):  {self.replaced_address}",
            f"  Replaced (name):  {self.replaced_name}",
            f"  Skipped (addr):   {self.skipped_address}",
            f"  Skipped (name):   {self.skipped_name}",
        ]
        return "\n".join(lines)


# Callback type: receives the incoming tag, the conflict kind ("address" | "name"),
# the existing tag that it conflicts with, and the strategy-resolved action
# ("replace" | "skip").  Return value is ignored; it's purely for logging/display.
ConflictCallback = Callable[[EasyBuilderTag, str, EasyBuilderTag, str], None]


def merge_eb_tags(
    base: EasyBuilderTagList,
    incoming: EasyBuilderTagList,
    strategy: ConflictStrategy = ConflictStrategy.SKIP,
    on_conflict: Optional[ConflictCallback] = None,
) -> tuple[EasyBuilderTagList, MergeResult]:
    """Merge *incoming* tags into *base*, returning the merged list and a summary.

    The *base* list is mutated in-place and also returned for convenience.
    *incoming* is never modified.

    Parameters
    ----------
    base:
        The tag list to merge into (the "existing" set).
    incoming:
        Tags to add. Conflicts are resolved according to *strategy*.
    strategy:
        How to handle tags that conflict on address or name.
    on_conflict:
        Optional callback invoked for every conflict, useful for logging.
        Signature: ``(incoming_tag, kind, existing_tag, action) -> None``
        where *kind* is ``"address"`` or ``"name"`` and *action* is
        ``"replace"`` or ``"skip"``.

    Returns
    -------
    (merged_list, result)
    """
    result = MergeResult()

    for key1, key2, tag in iter(incoming.map):
        tag: EasyBuilderTag
        addr_key = f"{tag.Address},{tag.Host}"

        addr_conflict = addr_key in base.map
        name_conflict = tag.Name in base.map

        if addr_conflict or name_conflict:
            # Snapshot both existing entries BEFORE any removal.
            # When both keys point to the same tag, the first removal would
            # leave the second lookup returning None.
            existing_by_addr = base.map.get_from_key1(addr_key) if addr_conflict else None
            existing_by_name = base.map.get_from_key2(tag.Name) if name_conflict else None

            # --- resolve address conflict ---
            if addr_conflict:
                replace = strategy in (
                    ConflictStrategy.REPLACE,
                    ConflictStrategy.REPLACE_ADDRESS,
                )
                action = "replace" if replace else "skip"
                if on_conflict:
                    on_conflict(tag, "address", existing_by_addr, action)
                if replace:
                    base.map.remove_from_key1(addr_key)
                    result.replaced_address += 1
                    result.details.append((tag, "address", "replaced"))
                else:
                    result.skipped_address += 1
                    result.details.append((tag, "address", "skipped"))
                    continue  # skip this tag entirely

            # --- resolve name conflict (only reached if addr didn't skip) ---
            # Guard: if both conflicts pointed at the same tag it was already
            # removed above, so there is nothing left to remove by name.
            if name_conflict and tag.Name in base.map:
                replace = strategy in (
                    ConflictStrategy.REPLACE,
                    ConflictStrategy.REPLACE_NAME,
                )
                action = "replace" if replace else "skip"
                if on_conflict:
                    on_conflict(tag, "name", existing_by_name, action)
                if replace:
                    base.map.remove_from_key2(tag.Name)
                    result.replaced_name += 1
                    result.details.append((tag, "name", "replaced"))
                else:
                    result.skipped_name += 1
                    result.details.append((tag, "name", "skipped"))
                    continue

        if base.add(tag):
            result.added += 1
        # If add() still fails after removing conflicts it means we hit a
        # concurrent duplicate within the incoming list itself — just skip.

    return base, result


def merge_eb_tags_interactive(
    base: EasyBuilderTagList,
    incoming: EasyBuilderTagList,
) -> tuple[EasyBuilderTagList, MergeResult]:
    """Interactive version of :func:`merge_eb_tags` using stdin prompts.

    Equivalent to the original CLI behaviour: per-tag yes/no/all/none prompts.
    """
    from eb_macro_gen.common import PromptResult, prompt_yna

    result = MergeResult()

    replace_all_addr = False
    replace_no_addr = False
    replace_all_names = False
    replace_no_names = False

    for key1, key2, tag in iter(incoming.map):
        tag: EasyBuilderTag
        addr_key = f"{tag.Address},{tag.Host}"

        addr_conflict = addr_key in base.map
        name_conflict = tag.Name in base.map

        if addr_conflict or name_conflict:
            # --- name conflict ---
            if name_conflict:
                existing = base.map.get_from_key2(tag.Name)
                do_replace = False
                if not (replace_all_names or replace_no_names):
                    r = prompt_yna(
                        f"A tag with the name '{tag.Name}' already exists. Replace it?"
                    )
                    if r == PromptResult.ALL:
                        replace_all_names = True
                    elif r == PromptResult.NONE:
                        replace_no_names = True
                    elif r == PromptResult.YES:
                        do_replace = True
                if (do_replace or replace_all_names) and not replace_no_names:
                    base.map.remove_from_key2(tag.Name)
                    result.replaced_name += 1
                elif replace_no_names or not do_replace:
                    result.skipped_name += 1
                    continue

            # --- address conflict ---
            if addr_conflict:
                existing = base.map.get_from_key1(addr_key)
                do_replace = False
                if not (replace_all_addr or replace_no_addr):
                    r = prompt_yna(
                        f"A tag with the address '{addr_key}' already exists. "
                        f"Replace it ({existing.Name} -> {tag.Name})?"
                    )
                    if r == PromptResult.ALL:
                        replace_all_addr = True
                    elif r == PromptResult.NONE:
                        replace_no_addr = True
                    elif r == PromptResult.YES:
                        do_replace = True
                if (do_replace or replace_all_addr) and not replace_no_addr:
                    base.map.remove_from_key1(addr_key)
                    result.replaced_address += 1
                elif replace_no_addr or not do_replace:
                    result.skipped_address += 1
                    continue

        if base.add(tag):
            result.added += 1

    return base, result