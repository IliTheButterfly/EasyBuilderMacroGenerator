# Tags generator (`EasyBuilderTagList`)

`EasyBuilderTagList` is a helper class used to build EasyBuilder Pro tag CSV files from Python.

It is defined in [`objects.py`](../../src/eb_macro_gen/objects.py) and is built around the `EasyBuilderTag` dataclass.

## When to use it

Use `EasyBuilderTagList` when you want to:
- Build large tag lists programmatically (loops, naming rules, address auto-increment, etc.)
- Avoid manual CSV edits in EasyBuilder Pro
- Export generated tags and combine them with an existing EasyBuilder export
- Load tags from a PLC export and use them directly in a macro script

## Core objects

### `EasyBuilderTag`
Represents one tag row in the CSV.

Constructor fields:
- `Name` — tag name
- `Host` — device name as it appears in EasyBuilder Pro (e.g. `"Local HMI"`)
- `Address` — address string in `"register,number"` format (e.g. `"LW,70"`)
- `Comment` — description shown in the Address window
- `Type` — EasyBuilder type string (e.g. `"16-bit Signed"`)

`EasyBuilderTag` has a `to_tag()` method that returns a `Tag` object ready for use in macro generation.

### `EasyBuilderTagList`
A container of `EasyBuilderTag` entries with duplicate checks on both address+host and name.

Main methods:
- `add(tag)` — adds a tag; returns `False` if it conflicts with an existing tag
- `read(stream)` — reads an EasyBuilder CSV stream into the collection
- `write(stream)` — writes the collection to a CSV stream

## Convenience I/O functions

Rather than opening files and calling `.read()`/`.write()` manually, use the functions in `eb_macro_gen.tools.io`:

```python
from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags, load_koyo_tags

# Load an EasyBuilder export
tags = load_eb_tags("eb_tags.csv")

# Load and convert a Koyo PLC nicknames export
koyo_tags = load_koyo_tags("koyo_nicknames.csv", "MyKoyoPLC")

# Save any EasyBuilderTagList back to CSV
save_eb_tags(tags, "output.csv")
```

## Generating tags programmatically

```python
from pathlib import Path
from eb_macro_gen.objects import EasyBuilderTagList, EasyBuilderTag, DT_EB_MAP, DataType
from eb_macro_gen.instructions import LOCAL_HMI

REACTORS = ["R1", "R2", "R3"]
PHASES   = ["fill", "mix", "heat", "transfer"]

tags = EasyBuilderTagList()
lw_address = 120
lb_address = 300

for reactor in REACTORS:
    for phase in PHASES:
        tags.add(EasyBuilderTag(
            f"{reactor}_{phase}_count",
            LOCAL_HMI,
            f"LW,{lw_address}",
            f"{reactor} {phase} completed cycles",
            DT_EB_MAP[DataType.S16],
        ))
        lw_address += 1

        tags.add(EasyBuilderTag(
            f"{reactor}_{phase}_active",
            LOCAL_HMI,
            f"LB,{lb_address}",
            f"{reactor} {phase} active flag",
            DT_EB_MAP[DataType.Bit],
        ))
        lb_address += 1

save_eb_tags(tags, "reactor_phase_tags.csv")
```

## Merging with an existing export

Use `merge_eb_tags` to combine your generated tags with an existing EasyBuilder export.
Pass a `ConflictReport` as the `on_conflict` callback to capture and inspect conflicts:

```python
from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags
from eb_macro_gen.tools.merge import merge_eb_tags, ConflictStrategy
from eb_macro_gen.tools.reporting import ConflictReport

existing  = load_eb_tags("eb_tags.csv")
generated = load_eb_tags("reactor_phase_tags.csv")

report = ConflictReport()
merged, result = merge_eb_tags(existing, generated, strategy=ConflictStrategy.SKIP,
                                on_conflict=report.record)

# Show all meaningful conflicts (identical duplicates hidden by default)
report.print()
print(result)  # summary of added / skipped / replaced counts

save_eb_tags(merged, "output.csv")
```

Filter and truncate the conflict output as needed:

```python
# Show only name conflicts, at most 10 rows
report.print(show={"name"}, truncate=10)

# Show everything including identical duplicates
report.print(verbose=True)
```

Or use the CLI tools directly — see [`combine_tags`](../tools/combine-tags.md) and [`koyo_tags_import`](../tools/koyo-tags-import.md).

## Using loaded tags in a macro script

Once tags are loaded you can look them up by name or address and use them directly in macro generation — no intermediate CSV required:

```python
from eb_macro_gen.tools.io import load_koyo_tags
from eb_macro_gen.syntax import *
from eb_macro_gen.objects import *

koyo_tags = load_koyo_tags("koyo_nicknames.csv", "MyKoyoPLC")

# get_from_key2 looks up by tag name
tank_temp_eb = koyo_tags.map.get_from_key2("TankTemp")
tank_temp    = tank_temp_eb.to_tag()

temp_val = vfloat("temp_val")
macro = Macro("read_tank", "Read tank temperature from PLC")

with macro:
    macro.write(
        COMMENT("Read temperature"),
        tank_temp.read(temp_val),
        IF(temp_val > 80.0)(
            COMMENT("Over-temperature alarm"),
        ),
    )

macro.display()
```

## Typical end-to-end workflow

1. Export current tags from EasyBuilder Pro (Address window → Export CSV)
2. Export PLC nicknames from Click Programming Software (File → Export → Nicknames)
3. Run `koyo_tags_import` (or call `load_koyo_tags` in a script) to convert and merge
4. Re-import the merged CSV into EasyBuilder Pro

|[Previous](04-how-does-it-work.md) | [Index](../index.md) | [Next]() |
|:-|:-:|-:|