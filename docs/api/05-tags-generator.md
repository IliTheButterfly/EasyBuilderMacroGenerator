# Tags generator (`EasyBuilderTagList`)

`EasyBuilderTagList` is a helper class used to generate EasyBuilder tag CSV files from Python.

It is defined in [`objects.py`](../../src/eb_macro_gen/objects.py) and is built around the `EasyBuilderTag` dataclass.

## When to use it

Use `EasyBuilderTagList` when you want to:
- Build large tag lists programmatically (loops, naming rules, address auto-increment, etc.)
- Avoid manual CSV edits in EasyBuilder Pro
- Export generated tags and combine them with an existing EasyBuilder export

## Core objects

### `EasyBuilderTag`
Represents one tag row in the CSV.

Constructor fields:
- `Name`: Tag name
- `Host`: Device/host name (for example `Local HMI`)
- `Address`: Address string (for example `LW,70`)
- `Comment`: Description/comment
- `Type`: EasyBuilder type string (for example `16-bit Signed`)

### `EasyBuilderTagList`
A container of `EasyBuilderTag` entries with duplicate checks.

Main methods:
- `add(tag)`
  - Adds a tag to the collection
  - Returns `False` when the tag conflicts with an existing tag (same `Address+Host` or same `Name`)
- `read(stream)`
  - Reads an existing EasyBuilder CSV stream into the collection
- `write(stream)`
  - Writes the collection to a CSV stream

## Example

```python
from pathlib import Path
from eb_macro_gen.objects import EasyBuilderTagList, EasyBuilderTag, DT_EB_MAP, DataType
from eb_macro_gen.instructions import LOCAL_HMI
from eb_macro_gen.syntax import vshort

REACTORS = ["R1", "R2", "R3"]
PHASES = ["fill", "mix", "heat", "transfer"]

def hmi_counter_tag(reactor: str, phase: str) -> str:
    return f"{reactor}_{phase}_count"

def hmi_status_tag(reactor: str, phase: str) -> str:
    return f"{reactor}_{phase}_active"

# Variable example: maybe used later in your macro to select a phase index
phase_index = vshort("phase_index", 0)

tags = EasyBuilderTagList()
lw_address = 120
lb_address = 300

for reactor in REACTORS:
    for phase in PHASES:
        tags.add(EasyBuilderTag(
            hmi_counter_tag(reactor, phase),
            LOCAL_HMI,
            f"LW,{lw_address}",
            f"{reactor} {phase} completed cycles",
            DT_EB_MAP[DataType.S16],
        ))
        lw_address += 1

        tags.add(EasyBuilderTag(
            hmi_status_tag(reactor, phase),
            LOCAL_HMI,
            f"LB,{lb_address}",
            f"{reactor} {phase} active flag",
            DT_EB_MAP[DataType.Bit],
        ))
        lb_address += 1

# Export tags csv
path = Path("./temp/reactor_phase_tags.csv")
with path.open("w", newline="") as wr:
    tags.write(wr)
```

## Combining the generated CSV with other files

After export, combine your generated CSV with an existing EasyBuilder export using one of the available tool flows:

- CLI tool: [`combine_tags`](../tools/combine-tags.md)
- Python API/tooling workflows under [`src/eb_macro_gen/tools`](../../src/eb_macro_gen/tools)

A common workflow is:
1. Export current tags from EasyBuilder Pro
2. Generate additional tags with `EasyBuilderTagList`
3. Merge both CSV files with `combine_tags`
4. Re-import the merged CSV into EasyBuilder Pro

|[Previous](04-how-does-it-work.md) | [Index](../index.md) | [Next]() |
|:-|:-:|-:|
