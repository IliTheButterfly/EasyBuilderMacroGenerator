"""Tests for eb_macro_gen.common helpers (DoubleKeyMap, smart_split)."""
from eb_macro_gen.common import DoubleKeyMap, smart_split


def test_doublekeymap_basic_add_and_get():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    assert m.add("a", 1, "alpha") is True
    assert m.get_from_key1("a") == "alpha"
    assert m.get_from_key2(1) == "alpha"
    assert len(m) == 1


def test_doublekeymap_rejects_duplicate_keys():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    assert m.add("a", 2, "other") is False
    assert m.add("b", 1, "other") is False
    assert len(m) == 1
    assert m.get_from_key1("a") == "alpha"


def test_doublekeymap_remove_from_key1_drops_both_keys():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    m.add("b", 2, "beta")
    m.remove_from_key1("a")
    assert m.get_from_key1("a") is None
    assert m.get_from_key2(1) is None
    assert m.get_from_key1("b") == "beta"
    assert len(m) == 1


def test_doublekeymap_remove_from_key2_drops_both_keys():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    m.remove_from_key2(1)
    assert m.get_from_key1("a") is None
    assert m.get_from_key2(1) is None
    assert len(m) == 0


def test_doublekeymap_remove_missing_is_noop():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    m.remove_from_key1("nope")
    m.remove_from_key2(99)
    assert len(m) == 1


def test_doublekeymap_does_not_match_on_hash_collision():
    """Equality, not hash equality, must drive lookups.

    A class whose hash collapses to a constant must still distinguish its
    instances by ``__eq__``. The previous list-walk implementation compared
    ``hash(k) == hash(key)`` and returned the wrong value on collisions.
    """

    class Colliding:
        def __init__(self, name: str) -> None:
            self.name = name

        def __hash__(self) -> int:
            return 0

        def __eq__(self, other: object) -> bool:
            return isinstance(other, Colliding) and self.name == other.name

    a = Colliding("a")
    b = Colliding("b")
    m: DoubleKeyMap[Colliding, int, str] = DoubleKeyMap()
    m.add(a, 1, "first")
    m.add(b, 2, "second")
    assert m.get_from_key1(a) == "first"
    assert m.get_from_key1(b) == "second"
    assert m.get_from_key1(Colliding("c")) is None


def test_doublekeymap_iter_yields_triples():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    m.add("b", 2, "beta")
    assert sorted(list(m)) == [("a", 1, "alpha"), ("b", 2, "beta")]


def test_doublekeymap_contains_checks_both_keys_and_values():
    m: DoubleKeyMap[str, int, str] = DoubleKeyMap()
    m.add("a", 1, "alpha")
    assert "a" in m
    assert 1 in m
    assert "alpha" in m
    assert "missing" not in m


def test_smart_split_handles_quotes_and_escapes():
    assert smart_split('a,b,c') == ['a', 'b', 'c']
    assert smart_split('a,"b,c",d') == ['a', 'b,c', 'd']
    assert smart_split('a,"he said ""hi""",b') == ['a', 'he said "hi"', 'b']
