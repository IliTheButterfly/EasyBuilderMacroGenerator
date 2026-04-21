# Index

## API
- [Getting started](api/01-getting-started.md)
- [Syntax](api/02-syntax.md)
- [Instructions](api/03-instructions.md)
- [How does it work?](api/04-how-does-it-work.md)
- [Tags generator (`EasyBuilderTagList`)](api/05-tags-generator.md)

## Tools
- [`koyo_tags_import`](tools/koyo-tags-import.md)
- [`combine_tags`](tools/combine-tags.md)

## Tools Python API (`eb_macro_gen.tools`)
- `load_eb_tags(path)` — load an EasyBuilder tag CSV
- `save_eb_tags(tags, path)` — save an `EasyBuilderTagList` to CSV
- `load_koyo_tags(path, device_name)` — load and convert a Koyo nicknames CSV
- `merge_eb_tags(base, incoming, strategy, on_conflict)` — programmatic merge with `ConflictStrategy`
- `merge_eb_tags_interactive(base, incoming)` — interactive merge (stdin prompts, same behaviour as the CLI tools without `--force`)
- `ConflictReport` — collects conflicts during a merge and renders them as a grouped table; pass `report.record` as the `on_conflict` callback