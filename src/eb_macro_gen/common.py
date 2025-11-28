from enum import Enum
from typing import Generic, Hashable, List, Optional, TypeVar, Union

TK1_ = TypeVar("TK1_", bound=Hashable)
TK2_ = TypeVar("TK2_", bound=Hashable)
TV_ = TypeVar("TV_")

class DoubleKeyMap(Generic[TK1_, TK2_, TV_]):
    def __init__(self):
        self.keys1:List[TK1_] = list()
        self.keys2:List[TK2_] = list()
        self.values:List[TV_] = list()
        
    def add(self, key1:TK1_, key2:TK2_, value:TV_) -> bool:
        if key1 in self.keys1:
            return False
        if key2 in self.keys2:
            return False
        self.keys1.append(key1)
        self.keys2.append(key2)
        self.values.append(value)
        return True
        
    def remove_from_key1(self, key:TK1_):
        kh = hash(key)
        idx = None
        for i, k in enumerate(self.keys1):
            if hash(k) == kh:
                idx = i
                break
            
        if idx is not None:
            del self.keys1[idx]
            del self.keys2[idx]
            del self.values[idx]
            
    def remove_from_key2(self, key:TK2_):
        kh = hash(key)
        idx = None
        for i, k in enumerate(self.keys2):
            if hash(k) == kh:
                idx = i
                break
            
        if idx is not None:
            del self.keys1[idx]
            del self.keys2[idx]
            del self.values[idx]
        
    def get_from_key1(self, key:TK1_) -> Optional[TV_]:
        kh = hash(key)
        for i, k in enumerate(self.keys1):
            if hash(k) == kh:
                return self.values[i]
        return None
    
    def get_from_key2(self, key:TK2_) -> Optional[TV_]:
        kh = hash(key)
        for i, k in enumerate(self.keys2):
            if hash(k) == kh:
                return self.values[i]
        return None
        
    def __len__(self) -> int:
        return len(self.values)
    
    def __iter__(self):
        return zip(self.keys1, self.keys2, self.values)
    
    def __contains__(self, obj) -> bool:
        return obj in self.keys1 or obj in self.keys2 or obj in self.values


def smart_split(text: str, sep: str = ',') -> list[str]:
    parts:List[str] = []
    current:List[str] = []
    in_quotes = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '"':
            # Handle escaped double quotes ("")
            if in_quotes and i + 1 < len(text) and text[i + 1] == '"':
                current.append('"')
                i += 1
            else:
                in_quotes = not in_quotes
        elif ch == sep and not in_quotes:
            parts.append(''.join(current))
            current = []
        else:
            current.append(ch)
        i += 1

    # Append last field
    parts.append(''.join(current))

    # Strip outer quotes and unescape inner ones
    cleaned:List[str] = []
    for part in parts:
        part = part.strip()
        if len(part) >= 2 and part[0] == '"' and part[-1] == '"':
            part = part[1:-1]
        part = part.replace('""', '"')
        cleaned.append(part)
    return cleaned

class PromptResult(Enum):
    YES = 0
    NO = 1
    ALL = 2
    NONE = 3

def prompt_yna(prompt:str) -> PromptResult:
    while True:
        v = input(f"{prompt} (y[es], n[o], a[ll], none)")
        if v.lower().startswith('none'):
            return PromptResult.NONE
        if v.lower().startswith('y'):
            return PromptResult.YES
        if v.lower().startswith('n'):
            return PromptResult.NO
        if v.lower().startswith('a'):
            return PromptResult.ALL
        print("Invalid input.")
