#!/usr/bin/python
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
import sys

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from eb_macro_gen.tools.io import load_eb_tags, load_koyo_tags, save_eb_tags
from eb_macro_gen.tools.merge import (
    ConflictStrategy,
    merge_eb_tags,
    merge_eb_tags_interactive,
)
from eb_macro_gen.tools.reporting import ConflictReport

_SHOW_HELP = (
    "Filter which conflict groups to display. "
    "One or more of: address, name, replaced, skipped, all, none. "
    "Default when --dry-run is set: all. "
    "Default otherwise: none (use --show or --dry-run to see conflicts). "
    "Combine filters freely, e.g. --show address skipped."
)


def main():
    parser = ArgumentParser(
        "koyo_tags_import",
        description="Convert a Koyo PLC nicknames CSV to an EasyBuilder tag CSV.",
    )
    parser.add_argument("koyo_file_csv", help="Koyo-exported nicknames CSV file")
    parser.add_argument("output_file_csv", help="Destination EasyBuilder tag CSV")
    parser.add_argument("koyo_name", help="PLC device name as configured in EasyBuilder Pro")
    parser.add_argument(
        "-a", "--append",
        help="Existing EasyBuilder tag CSV to merge the converted tags into",
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Non-interactive: resolve all conflicts using --strategy without prompting",
    )
    parser.add_argument(
        "--strategy",
        choices=[s.value for s in ConflictStrategy],
        default=ConflictStrategy.SKIP.value,
        help=(
            "Conflict resolution strategy when --force is set (default: skip). "
            "skip=keep existing, replace=incoming wins on both keys, "
            "replace-address=incoming wins on address only, "
            "replace-name=incoming wins on name only."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Show conflicts and summary without writing the output file. "
            "Implies --show all unless --show is specified explicitly."
        ),
    )
    parser.add_argument(
        "--show",
        nargs="+",
        choices=(*ConflictReport.SHOW_CHOICES, "none"),
        default=None,
        metavar="FILTER",
        help=_SHOW_HELP,
    )
    parser.add_argument(
        "--truncate",
        type=int,
        default=0,
        metavar="N",
        help="Show at most N rows per conflict group, then '… and M more'. 0 = no limit.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help=(
            "Include identical duplicates (same name and address on both sides) "
            "in the conflict table. These are hidden by default as they carry no "
            "actionable information."
        ),
    )

    args = parser.parse_args(sys.argv[1:])

    koyo_file = Path(args.koyo_file_csv)
    if not koyo_file.exists():
        parser.error(f"koyo_file_csv '{args.koyo_file_csv}' does not exist")

    incoming = load_koyo_tags(koyo_file, args.koyo_name)

    if args.append is not None:
        append_path = Path(args.append)
        if not append_path.exists():
            parser.error(f"append file '{args.append}' does not exist")
        base = load_eb_tags(append_path)
    else:
        from eb_macro_gen.objects import EasyBuilderTagList
        base = EasyBuilderTagList()

    report = ConflictReport()

    if args.force:
        strategy = ConflictStrategy(args.strategy)
        merged, result = merge_eb_tags(base, incoming, strategy=strategy, on_conflict=report.record)
    else:
        merged, result = merge_eb_tags_interactive(base, incoming)

    if args.show is not None:
        show = set(args.show)
    elif args.dry_run:
        show = {"all"}
    else:
        show = {"none"}

    if "none" not in show:
        report.print(show=show, truncate=args.truncate, verbose=args.verbose)

    print("Merge summary:")
    print(result)

    if not args.dry_run:
        save_eb_tags(merged, args.output_file_csv)
        print(f"\nWritten to {args.output_file_csv}")
    else:
        print("\n(Dry run — no file written)")


if __name__ == "__main__":
    main()