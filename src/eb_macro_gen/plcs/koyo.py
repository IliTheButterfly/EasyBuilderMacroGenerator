from __future__ import annotations
from typing import IO, Dict, Union, override
from dataclasses import dataclass
from eb_macro_gen.common import DoubleKeyMap, smart_split
from eb_macro_gen.objects import DT_EB_MAP, EB_DT_MAP, Tag, TagList

KOYO_EB_TYPE_MAP:Dict[str, str] = {
    "BIT" : "",
    "INT" : "16-bit Signed",
    "INT2" : "32-bit Signed",
    "FLOAT" : "32-bit Float",
}

EB_KOYO_TYPE_MAP = {
    "" : "BIT",
    "16-bit Signed" : "INT",
    "32-bit Signed" : "INT2",
    "32-bit Float" : "FLOAT",
}

@dataclass
class KoyoTag:
    Address:str
    Data:str
    Nickname:str
    InitialValue:Union[int, float, str]
    Retentive:bool
    AddressComment:str
    
    def to_tag(self, device_name:str) -> Tag:
        return Tag(self.Nickname, device_name, self.Address, EB_DT_MAP[KOYO_EB_TYPE_MAP[self.Data]])
    
class KoyoTagList(TagList[KoyoTag]):
    def __init__(self):
        self.map:DoubleKeyMap[str, str, KoyoTag] = DoubleKeyMap()
        
    @override
    def add(self, tag:KoyoTag) -> bool:
        return self.map.add(tag.Address, tag.Nickname, tag)
    
    @override
    def __contains__(self, tag:KoyoTag) -> bool:
        if not isinstance(tag, KoyoTag):
            return False
        return tag.Address in self.map or tag.Nickname in self.map
    
    @override
    def read(self, stream:IO):
        stream.readline() # Skip headers line
        for l in stream.readlines():
            values = smart_split(l)
            tag = KoyoTag(values[0], values[1], values[2], values[3], True if values[4] == "Yes" else False, values[5])
            self.add(tag)