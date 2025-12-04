# `koyo_tags_import` tool

This tool is used to import tags from Click Programming Software (Koyo PLCs) into EasyBuilder Pro.

This script can also append those tags to an existing tag CSV from EasyBuilder Pro.

## Usage
Make sure you have installed the python package as mentioned [here](../../ReadMe.md#usage).

```
usage: koyo_tags_import [-h] [-a APPEND] [-f] koyo_file_csv output_file_csv koyo_name

positional arguments:
  koyo_file_csv        The koyo exported 'nicknames' csv file
  output_file_csv      The csv file to export the tags
  koyo_name            The plcs name as set in the easy builder settings

options:
  -h, --help           show this help message and exit
  -a, --append APPEND  Original easy builder exported tags csv to append the tags to
  -f, --force          Non-interactive
```

Here is what you would normally do:

1. Export Koyo tags:
   1. Open a Click project
   2. Go to File -> Export -> Nicknames
2. Optionally export EasyBuilder Pro tags:
   1. Navigate to the Address window
   2. Click on Export CSV
3. Run the `koyo_tags_import` script:
   - If you exported the EasyBuilder Pro tags, use `--append FILE.csv`
   - For `koyo_file_csv` set the Koyo's exported nicknames file (with .csv)
   - For `output_file_csv` write path to save the new file (with .csv)
   - For `koyo_name` write the name of the PLC as it appears in EasyBuilder Pro

## Example:
If you have the following files:
```
koyo_tags.csv
eb_tags.csv
```
Run:
```sh
koyo_tags_import -a "eb_tags.csv" "koyo_tags.csv" "output.csv" "KOYO CLICK V3 MODBUS TCP/IP"
```