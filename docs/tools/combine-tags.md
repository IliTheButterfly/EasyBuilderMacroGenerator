# `combine_tags` tool

This tool merges two EasyBuilder Pro tag CSV exports into one, with conflict resolution for tags that share an address or name.

This is useful especially when creating tags from a script with `EasyBuilderTagList` and merging them with an existing EasyBuilder export.

## Usage
Make sure you have installed the python package as mentioned [here](../../ReadMe.md#usage).

```
usage: combine_tags [-h] [-f] [--strategy {skip,replace,replace-address,replace-name}]
                    [--dry-run] [--show FILTER [FILTER ...]] [--truncate N] [--verbose]
                    file1_csv file2_csv output_file_csv

positional arguments:
  file1_csv        Base EasyBuilder tag CSV (existing tags)
  file2_csv        Incoming EasyBuilder tag CSV to merge in
  output_file_csv  Destination CSV file

options:
  -h, --help            show this help message and exit
  -f, --force           Non-interactive: resolve all conflicts using --strategy
                        without prompting
  --strategy {skip,replace,replace-address,replace-name}
                        Conflict resolution strategy when --force is set (default: skip).
                        skip             Keep existing tag, drop incoming
                        replace          Incoming tag wins on both address and name conflicts
                        replace-address  Incoming tag wins on address conflicts only
                        replace-name     Incoming tag wins on name conflicts only
  --dry-run             Show conflicts and summary without writing the output file.
                        Implies --show all unless --show is specified explicitly.
  --show FILTER         Filter which conflict groups to display. One or more of:
                        address, name, replaced, skipped, all, none.
                        Default when --dry-run is set: all.
                        Default otherwise: none.
                        Combine filters freely, e.g. --show address skipped.
  --truncate N          Show at most N rows per conflict group, then '… and M more'.
                        0 = no limit (default).
  --verbose             Include identical duplicates (same name and address on both sides)
                        in the conflict table. Hidden by default as they carry no
                        actionable information.
```

## Step-by-step

1. Export your current EasyBuilder Pro tags:
   1. Navigate to the **Address** window
   2. Click **Export CSV**
2. Generate a second CSV from a script (see [Tags generator](../api/05-tags-generator.md)) or obtain it from another source
3. Run `combine_tags`:
   - `file1_csv` — your existing EasyBuilder export (the base)
   - `file2_csv` — the new tags to merge in
   - `output_file_csv` — path for the merged output file

## Conflict resolution

A conflict occurs when an incoming tag shares an **address+host** or a **name** with an existing tag.

Without `--force`, the tool prompts interactively for each conflict:
```
A tag with the name 'TankTemp' already exists. Replace it? (y[es], n[o], a[ll], none)
```

With `--force`, all conflicts are resolved silently according to `--strategy` (default: `skip`).

| Strategy           | Address conflict | Name conflict |
|--------------------|-----------------|---------------|
| `skip`             | keep existing   | keep existing |
| `replace`          | incoming wins   | incoming wins |
| `replace-address`  | incoming wins   | keep existing |
| `replace-name`     | keep existing   | incoming wins |

## Conflict reporting

The tool displays a grouped table showing what changed on each side — useful for spotting tags whose address has moved or whose name has been reassigned. A `←` marks the field that differs.

By default, **identical duplicates** (same name and address on both sides) are hidden from the table since they carry no actionable information. They still appear in the summary counts. Use `--verbose` to include them.

```
Name conflicts (4) → replace:
  Incoming name        Incoming addr       Existing name        Existing addr
  -----------------------------------------------------------------------
  F32_flush_hours      LW,180,Local HMI ←  F32_flush_hours      LW,179,Local HMI
  heat_minutes         LW,79,Local HMI  ←  heat_minutes         LW,16,Local HMI

  (717 identical duplicate(s) hidden — use --verbose to show)
```

Conflict output is controlled by `--show`:
- **`--dry-run`** — shows all meaningful conflicts by default (no file written). The primary way to inspect conflicts before committing.
- **Normal run** — conflicts hidden by default. Use `--show` to opt in without a dry run.

## Output summary

Every run prints a summary regardless of `--show`:
```
Merge summary:
  Added:            38
  Replaced (addr):   2
  Replaced (name):   0
  Skipped (addr):    1
  Skipped (name):    1
```

## Examples

### Interactive merge (default)
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv"
```

### Inspect conflicts before committing
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv" --force --strategy replace --dry-run
```

### Inspect only name conflicts, 10 rows max
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv" --force --dry-run --show name --truncate 10
```

### Merge and show name conflicts on the actual run
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv" --force --strategy replace --show name
```

### Include identical duplicates in the conflict table
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv" --force --dry-run --verbose
```

### Non-interactive merge, no conflict output
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv" --force --show none
```

## Python API

The merge and reporting logic is available as importable classes, useful when you want to merge tags inside a larger Python script without going through the CLI.

```python
from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags
from eb_macro_gen.tools.merge import merge_eb_tags, ConflictStrategy
from eb_macro_gen.tools.reporting import ConflictReport

base     = load_eb_tags("eb_tags.csv")
incoming = load_eb_tags("created_tags.csv")

report = ConflictReport()
merged, result = merge_eb_tags(base, incoming, strategy=ConflictStrategy.REPLACE_ADDRESS,
                                on_conflict=report.record)

# Show only name conflicts, 10 rows max (identical duplicates hidden by default)
report.print(show={"name"}, truncate=10)
print(result)

save_eb_tags(merged, "output.csv")
```

See [Tags generator](../api/05-tags-generator.md) for a full end-to-end example.

| [Index](../index.md) |
|:-:|