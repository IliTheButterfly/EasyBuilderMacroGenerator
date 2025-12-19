#!/usr/bin/python
from __future__ import annotations
from pathlib import Path
from argparse import ArgumentParser
import sys

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))


from eb_macro_gen.common import PromptResult, prompt_yna
from eb_macro_gen.objects import EasyBuilderTag, EasyBuilderTagList
    
    
def main():
    argv = sys.argv
    parser = ArgumentParser("combine_tags")
    parser.add_argument("file1_csv", help="Original easy builder exported tags csv to append the tags to")
    parser.add_argument("file2_csv", help="Original easy builder exported tags csv to append the tags to")
    parser.add_argument("output_file_csv", help="The csv file to export the tags")
    parser.add_argument("-f", "--force", action="store_true", help="Non-interactive")
    
    args = parser.parse_args(argv[1:])
    
    output_file = Path(args.output_file_csv)
    file1 = Path(args.file1_csv)
    file2 = Path(args.file2_csv)
    
    ebTags = EasyBuilderTagList()
    ebTags2 = EasyBuilderTagList()
            
    if file1 is not None:
        with file1.open('r') as rd:
            ebTags.read(rd)
            
    if file2 is not None:
        with file2.open('r') as rd:
            ebTags2.read(rd)

    replace_all_tags = False
    replace_no_tags = False
    replace_all_names = False
    replace_no_names = False
    for key1, key2, tag in iter(ebTags2.map):
        tag:EasyBuilderTag
        
        if tag in ebTags:
            if key2 in ebTags.map:
                e = False
                if not (replace_all_names or replace_no_names):
                    r = prompt_yna(f"A tag with the name '{tag.Name}' already exists. Replace it?")
                    if r == PromptResult.ALL:
                        replace_all_names = True
                    if r == PromptResult.NONE:
                        replace_no_names = True
                    if r == PromptResult.YES:
                        e = True
                if (e or replace_all_names) and not replace_no_names:
                    ebTags.map.remove_from_key2(key2)
            if key1 in ebTags.map:
                e = False
                if not (replace_all_tags or replace_no_tags):
                    r = prompt_yna(f"A tag with the address '{tag.Address},{tag.Host}' already exists. Replace it ({ebTags.map.get_from_key1(key1).Name} -> {tag.Name})?")
                    if r == PromptResult.ALL:
                        replace_all_tags = True
                    if r == PromptResult.NONE:
                        replace_no_tags = True
                    if r == PromptResult.YES:
                        e = True
                if (e or replace_all_tags) and not replace_no_tags:
                    ebTags.map.remove_from_key1(key1)
        if ebTags.add(tag):
            print(f"Added {repr(tag)}")
        else:
            print(f"Skipped {repr(tag)}")
                
    with output_file.open('+w') as wr:
        for _, __, tag in iter(ebTags.map):
            tag:EasyBuilderTag
            wr.write(f"{tag.export()}\n")

if __name__ == "__main__":
    main()