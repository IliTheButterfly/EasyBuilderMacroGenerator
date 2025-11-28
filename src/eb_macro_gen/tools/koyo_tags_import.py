#!/usr/bin/python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from argparse import ArgumentParser
import sys

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))


from typing import Generic, Hashable, List, Optional, TypeVar, Union
from eb_macro_gen.common import DoubleKeyMap, PromptResult, smart_split, prompt_yna
from eb_macro_gen.objects import EasyBuilderTag, EasyBuilderTagList
from eb_macro_gen.plcs.koyo import KoyoTag, KoyoTagList, KOYO_EB_TYPE_MAP
    
    
def main(argv:List[str]):
    parser = ArgumentParser("koyo_tags_import")
    parser.add_argument("koyo_file_csv", help="The koyo exported 'nicknames' csv file")
    parser.add_argument("output_file_csv", help="The csv file to export the tags")
    parser.add_argument("koyo_name", help="The plcs name as set in the easy builder settings")
    parser.add_argument("-a", "--append", help="Original easy builder exported tags csv to append the tags to")
    parser.add_argument("-f", "--force", action="store_true", help="Non-interactive")
    
    args = parser.parse_args(argv[1:])
    
    koyo_file = Path(args.koyo_file_csv)
    output_file = Path(args.output_file_csv)
    append_file = None
    koyo_name:str = args.koyo_name
    
    if not koyo_file.exists():
        parser.exit(1, f"koyo_file_csv {args.koyo_file_csv} does not exist")
        
    if args.append:
        append_file = Path(args.append)
        if not append_file.exists():
            parser.exit(1, f"append file {args.append} does not exist")
        
    ebTags = EasyBuilderTagList()
            
    if append_file is not None:
        with append_file.open('r') as rd:
            ebTags.read(rd)

    koyoTags = KoyoTagList()
    with koyo_file.open('r') as rd:
        koyoTags.read(rd)
            
    replace_all_tags = False
    replace_no_tags = False
    replace_all_names = False
    replace_no_names = False
    for _, __, tag in iter(koyoTags.map):
        tag:KoyoTag
        register = ''.join(filter(lambda c: c.isalpha(), tag.Address))
        address = ''.join(filter(lambda c: c.isnumeric(), tag.Address))
        newTag = EasyBuilderTag(tag.Nickname, koyo_name, f"{register},{address}", tag.AddressComment, KOYO_EB_TYPE_MAP[tag.Data])
        if newTag in ebTags:
            if newTag.Name in ebTags.map:
                e = False
                if not (replace_all_names or replace_no_names):
                    r = prompt_yna(f"A tag with the name '{newTag.Name}' already exists. Replace it?")
                    if r == PromptResult.ALL:
                        replace_all_names = True
                    if r == PromptResult.NONE:
                        replace_no_names = True
                    if r == PromptResult.YES:
                        e = True
                if (e or replace_all_names) and not replace_no_names:
                    ebTags.map.remove_from_key2(newTag.Name)
            if f"{newTag.Address},{newTag.Host}" in ebTags.map:
                e = False
                if not (replace_all_tags or replace_no_tags):
                    r = prompt_yna(f"A tag with the address '{newTag.Address},{newTag.Host}' already exists. Replace it ({ebTags.map.get_from_key1(f"{newTag.Address},{newTag.Host}").Name} -> {newTag.Name})?")
                    if r == PromptResult.ALL:
                        replace_all_tags = True
                    if r == PromptResult.NONE:
                        replace_no_tags = True
                    if r == PromptResult.YES:
                        e = True
                if (e or replace_all_tags) and not replace_no_tags:
                    ebTags.map.remove_from_key1(f"{newTag.Address},{newTag.Host}")
        if ebTags.add(newTag):
            print(f"Added {repr(newTag)}")
        else:
            print(f"Skipped {repr(newTag)}")
                
    with output_file.open('+w') as wr:
        for _, __, tag in iter(ebTags.map):
            tag:EasyBuilderTag
            wr.write(f"{tag.export()}\n")

if __name__ == "__main__":
    main(sys.argv)