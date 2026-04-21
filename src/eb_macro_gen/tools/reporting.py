from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Set

from eb_macro_gen.objects import EasyBuilderTag


@dataclass
class ConflictRecord:
    kind: str          # "address" | "name"
    action: str        # "replace" | "skip"
    incoming: EasyBuilderTag
    existing: EasyBuilderTag

    @property
    def is_identical(self) -> bool:
        """True when name and address are the same on both sides — a pure duplicate."""
        return (
            self.incoming.Name    == self.existing.Name
            and self.incoming.Address == self.existing.Address
            and self.incoming.Host    == self.existing.Host
        )


class ConflictReport:
    """Collects conflict records during a merge and renders them as a table.

    Usage
    -----
    >>> report = ConflictReport()
    >>> merge_eb_tags(base, incoming, strategy, on_conflict=report.record)
    >>> report.print(show={"address"}, truncate=20)

    Identical duplicates (same name *and* same address on both sides) are
    tracked but excluded from the default output.  Pass ``verbose=True`` to
    include them.
    """

    # Valid values for the --show CLI flag ("none" is handled separately in the CLI)
    SHOW_CHOICES = ("address", "name", "replaced", "skipped", "all")

    def __init__(self):
        self._records: List[ConflictRecord] = []

    def record(self, tag: EasyBuilderTag, kind: str, existing: EasyBuilderTag, action: str):
        """on_conflict callback — matches the merge_eb_tags signature."""
        self._records.append(ConflictRecord(kind, action, tag, existing))

    @property
    def identical_count(self) -> int:
        return sum(1 for r in self._records if r.is_identical)

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter(self, show: Set[str], verbose: bool = False) -> List[ConflictRecord]:
        """Return records matching the *show* filter set.

        Parameters
        ----------
        show:
            Any combination of ``"address"``, ``"name"``, ``"replaced"``,
            ``"skipped"``, ``"all"``.  An empty set or ``{"all"}`` returns
            everything that passes the *verbose* gate.
        verbose:
            If False (default), identical duplicates are excluded — tags where
            both name and address match on both sides carry no useful
            information in the conflict table.
        """
        records = self._records if verbose else [r for r in self._records if not r.is_identical]

        if not show or "all" in show:
            return records

        return [r for r in records if r.kind in show or r.action in show]

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def print(
        self,
        show: Optional[Set[str]] = None,
        truncate: int = 0,
        verbose: bool = False,
    ):
        """Print conflict groups as aligned tables to stdout.

        Parameters
        ----------
        show:
            Filter set (any of SHOW_CHOICES).  ``None`` / empty → show all
            non-identical conflicts.
        truncate:
            If > 0, each group shows at most *truncate* rows then
            "… and N more".  0 = no truncation.
        verbose:
            If True, also shows identical duplicates (same name and address on
            both sides).  These are hidden by default as they carry no
            actionable information.
        """
        records = self.filter(show or {"all"}, verbose=verbose)
        if not records:
            n_hidden = self.identical_count
            if n_hidden and not verbose:
                print(f"  (no meaningful conflicts; {n_hidden} identical duplicate(s) hidden — use --verbose to show)")
            else:
                print("  (no conflicts to show)")
            return

        # Group by (kind, action) preserving first-seen order
        groups: dict[tuple, list] = {}
        for r in records:
            groups.setdefault((r.kind, r.action), []).append(r)

        # Column widths — measured across all visible records, capped for readability
        def addr_str(tag: EasyBuilderTag) -> str:
            return f"{tag.Address},{tag.Host}"

        col_in_name = min(max(len(r.incoming.Name)      for r in records), 36)
        col_in_addr = min(max(len(addr_str(r.incoming)) for r in records), 30)
        col_ex_name = min(max(len(r.existing.Name)      for r in records), 36)
        col_ex_addr = min(max(len(addr_str(r.existing)) for r in records), 30)

        header = (
            f"  {'Incoming name':<{col_in_name}}  "
            f"{'Incoming addr':<{col_in_addr}}  "
            f"{'Existing name':<{col_ex_name}}  "
            f"Existing addr"
        )
        sep = "  " + "-" * (col_in_name + 2 + col_in_addr + 2 + col_ex_name + 2 + col_ex_addr + 4)

        for (kind, action), recs in groups.items():
            # Always show total including identical duplicates in the heading count
            total_in_group = sum(
                1 for r in self._records
                if r.kind == kind and r.action == action
                and (verbose or not r.is_identical)
            )
            hidden_in_group = sum(
                1 for r in self._records
                if r.kind == kind and r.action == action and r.is_identical
            ) if not verbose else 0

            heading = f"\n{kind.capitalize()} conflicts ({total_in_group})"
            if hidden_in_group:
                heading += f" [{hidden_in_group} identical hidden]"
            heading += f" → {action}:"
            print(heading)
            print(header)
            print(sep)

            visible = recs if (truncate <= 0 or len(recs) <= truncate) else recs[:truncate]

            for r in visible:
                in_name = r.incoming.Name[:col_in_name]
                in_addr = addr_str(r.incoming)[:col_in_addr]
                ex_name = r.existing.Name[:col_ex_name]
                ex_addr = addr_str(r.existing)[:col_ex_addr]

                name_changed = r.incoming.Name    != r.existing.Name
                addr_changed = (r.incoming.Address != r.existing.Address
                                or r.incoming.Host  != r.existing.Host)

                in_name_ann = f"{in_name} ←" if name_changed else in_name
                in_addr_ann = f"{in_addr} ←" if addr_changed else in_addr

                print(
                    f"  {in_name_ann:<{col_in_name + (3 if name_changed else 1)}} "
                    f"{in_addr_ann:<{col_in_addr + (3 if addr_changed else 1)}} "
                    f"{ex_name:<{col_ex_name}}  "
                    f"{ex_addr}"
                )

            if truncate > 0 and len(recs) > truncate:
                print(f"  … and {len(recs) - truncate} more")

        if not verbose and self.identical_count:
            print(f"\n  ({self.identical_count} identical duplicate(s) hidden — use --verbose to show)")
        print()

    def __len__(self):
        return len(self._records)