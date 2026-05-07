from enum import Enum
from typing import Dict, Generic, Hashable, Iterator, List, Optional, Tuple, TypeVar

TK1_ = TypeVar("TK1_", bound=Hashable)
TK2_ = TypeVar("TK2_", bound=Hashable)
TV_ = TypeVar("TV_")


class DoubleKeyMap(Generic[TK1_, TK2_, TV_]):
    """Bidirectional 1:1 map between two key spaces sharing a value.

    Both keys must be unique; ``add`` returns False if either collides.
    Lookups and removals are O(1) (dict-backed, equality-based).
    """

    def __init__(self) -> None:
        self._by_k1: Dict[TK1_, Tuple[TK2_, TV_]] = {}
        self._k2_to_k1: Dict[TK2_, TK1_] = {}

    def add(self, key1: TK1_, key2: TK2_, value: TV_) -> bool:
        if key1 in self._by_k1 or key2 in self._k2_to_k1:
            return False
        self._by_k1[key1] = (key2, value)
        self._k2_to_k1[key2] = key1
        return True

    def remove_from_key1(self, key: TK1_) -> None:
        entry = self._by_k1.pop(key, None)
        if entry is not None:
            self._k2_to_k1.pop(entry[0], None)

    def remove_from_key2(self, key: TK2_) -> None:
        key1 = self._k2_to_k1.pop(key, None)
        if key1 is not None:
            self._by_k1.pop(key1, None)

    def get_from_key1(self, key: TK1_) -> Optional[TV_]:
        entry = self._by_k1.get(key)
        return entry[1] if entry is not None else None

    def get_from_key2(self, key: TK2_) -> Optional[TV_]:
        key1 = self._k2_to_k1.get(key)
        if key1 is None:
            return None
        return self._by_k1[key1][1]

    def __len__(self) -> int:
        return len(self._by_k1)

    def __iter__(self) -> Iterator[Tuple[TK1_, TK2_, TV_]]:
        for k1, (k2, v) in self._by_k1.items():
            yield (k1, k2, v)

    def __contains__(self, obj: object) -> bool:
        if obj in self._by_k1 or obj in self._k2_to_k1:
            return True
        return any(v == obj for _, v in self._by_k1.values())


def smart_split(text: str, sep: str = ',') -> List[str]:
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
