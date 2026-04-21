# `koyo_tags_import` tool

This tool converts a Koyo PLC (Click Programming Software) nicknames CSV export into an EasyBuilder Pro tag CSV, optionally merging the result with an existing EasyBuilder tag export.

## Usage
Make sure you have installed the python package as mentioned [here](../../ReadMe.md#usage).

```
usage: koyo_tags_import [-h] [-a APPEND] [-f]
                        [--strategy {skip,replace,replace-address,replace-name}]
                        [--dry-run] [--show FILTER [FILTER ...]] [--truncate N] [--verbose]
                        koyo_file_csv output_file_csv koyo_name

positional arguments:
  koyo_file_csv        Koyo-exported nicknames CSV file
  output_file_csv      Destination EasyBuilder tag CSV
  koyo_name            PLC device name as configured in EasyBuilder Pro

options:
  -h, --help            show this help message and exit
  -a, --append APPEND   Existing EasyBuilder tag CSV to merge the converted tags into
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

1. Export Koyo tags from Click Programming Software:
   1. Open your Click project
   2. Go to **File → Export → Nicknames**
2. *(Optional)* Export your current EasyBuilder Pro tags:
   1. Navigate to the **Address** window
   2. Click **Export CSV**
3. Run `koyo_tags_import`:
   - `koyo_file_csv` — the nicknames file exported from Click
   - `output_file_csv` — path for the output EasyBuilder tag CSV
   - `koyo_name` — the PLC device name **exactly as it appears** in EasyBuilder Pro's device settings
   - `--append` — if you exported existing EasyBuilder tags, pass that file here to merge

## Conflict resolution

Applies only when `--append` is used. A conflict occurs when a converted Koyo tag shares an **address+host** or a **name** with a tag already in the append file.

Without `--force`, the tool prompts interactively for each conflict:
```
A tag with the address 'V,100,MyKoyoPLC' already exists. Replace it (OldName -> NewName)? (y[es], n[o], a[ll], none)
```

With `--force`, all conflicts are resolved silently according to `--strategy` (default: `skip`).

| Strategy           | Address conflict | Name conflict |
|--------------------|-----------------|---------------|
| `skip`             | keep existing   | keep existing |
| `replace`          | incoming wins   | incoming wins |
| `replace-address`  | incoming wins   | keep existing |
| `replace-name`     | keep existing   | incoming wins |

## Conflict reporting

The tool displays a grouped table showing what changed on each side. A `←` marks the field that differs between incoming and existing.

By default, **identical duplicates** (same name and address on both sides) are hidden from the table. They still appear in the summary counts. Use `--verbose` to include them.

```
Name conflicts (3) → replace:
  Incoming name    Incoming addr      Existing name    Existing addr
  -------------------------------------------------------------------
  F32_flush_hours  LW,180,Local HMI ← F32_flush_hours  LW,179,Local HMI
  heat_minutes     LW,79,Local HMI  ← heat_minutes     LW,16,Local HMI

  (714 identical duplicate(s) hidden — use --verbose to show)
```

Conflict output is controlled by `--show`:
- **`--dry-run`** — shows all meaningful conflicts by default (no file written). The primary way to inspect conflicts before committing.
- **Normal run** — conflicts hidden by default. Use `--show` to opt in without a dry run.

## Output summary

Every run prints a summary regardless of `--show`:
```
Merge summary:
  Added:            52
  Replaced (addr):   0
  Replaced (name):   0
  Skipped (addr):    3
  Skipped (name):    0
```

## Examples

### Convert Koyo tags to a new EasyBuilder CSV
```sh
koyo_tags_import "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP"
```

### Inspect conflicts before merging
```sh
koyo_tags_import -a "eb_tags.csv" "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP" \
  --force --strategy replace --dry-run
```

### Inspect only name conflicts, 10 rows max
```sh
koyo_tags_import -a "eb_tags.csv" "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP" \
  --force --dry-run --show name --truncate 10
```

### Merge and show address conflicts on the actual run
```sh
koyo_tags_import -a "eb_tags.csv" "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP" \
  --force --strategy replace-address --show address
```

### Include identical duplicates in the conflict table
```sh
koyo_tags_import -a "eb_tags.csv" "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP" \
  --force --dry-run --verbose
```

## Python API

```python
from eb_macro_gen.tools.io import load_koyo_tags, load_eb_tags, save_eb_tags
from eb_macro_gen.tools.merge import merge_eb_tags, ConflictStrategy
from eb_macro_gen.tools.reporting import ConflictReport

koyo_tags = load_koyo_tags("koyo_tags.csv", "KOYO CLICK V3 MODBUS TCP/IP")
existing  = load_eb_tags("eb_tags.csv")

report = ConflictReport()
merged, result = merge_eb_tags(existing, koyo_tags, strategy=ConflictStrategy.REPLACE_ADDRESS,
                                on_conflict=report.record)

report.print(show={"name"}, truncate=10)
print(result)

save_eb_tags(merged, "output.csv")
```

You can also skip the CSV round-trip and use loaded tags directly in a macro script:

```python
from eb_macro_gen.tools.io import load_koyo_tags
from eb_macro_gen.syntax import *
from eb_macro_gen.objects import *

koyo_tags = load_koyo_tags("koyo_tags.csv", "MyKoyoPLC")

temp_tag = koyo_tags.map.get_from_key2("TankTemp").to_tag()
temp_val = vfloat("temp_val")
macro    = Macro("read_tank", "Read tank temperature")

with macro:
    macro.write(temp_tag.read(temp_val))

macro.display()
```

See [Tags generator](../api/05-tags-generator.md) for more detail on working with `EasyBuilderTagList`.

| [Index](../index.md) |
|:-:|