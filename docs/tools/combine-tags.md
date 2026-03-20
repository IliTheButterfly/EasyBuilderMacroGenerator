# `combine_tags` tool

This tool is used to combine tags CSV files.

This is useful especially when creating tags from a script with `EasyBuilderTagList`

## Usage
Make sure you have installed the python package as mentioned [here](../../ReadMe.md#usage).

```
usage: combine_tags [-h] [-f] file1_csv file2_csv output_file_csv

positional arguments:
  file1_csv        Original easy builder exported tags csv to append the tags to
  file2_csv        Original easy builder exported tags csv to append the tags to
  output_file_csv  The csv file to export the tags

options:
  -h, --help       show this help message and exit
  -f, --force      Non-interactive
```

Here is what you would normally do:

1. Export EasyBuilder Pro tags:
   1. Navigate to the Address window
   2. Click on Export CSV
2. Generate a CSV from a script:
   - See example below
3. Run the `combine_tags` script:
   - For `file1_csv` and `file2_csv` set your first and second files path (with .csv)
   - For `output_file_csv` set a path to the file to be created (with .csv)

## Example:
If you have the following files:
```
created_tags.csv
eb_tags.csv
```
Run:
```sh
combine_tags "eb_tags.csv" "created_tags.csv" "output.csv"
```
| [Index](../index.md) |
|:-:|