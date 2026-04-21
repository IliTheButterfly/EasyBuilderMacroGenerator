from src.eb_macro_gen.syntax import EVAL, vint, vint_arr


def test_reverse_operators_variable():
    a = vint("a")

    assert str(1 + a) == "1 + a"
    assert str(10 - a) == "10 - a"
    assert str(2 * a) == "2 * a"
    assert str(10 / a) == "10 / a"
    assert str(10 % a) == "10 % a"


def test_reverse_operators_variable_item():
    arr = vint_arr("arr", 3)
    item = arr[1]

    assert str(1 + item) == "1 + arr[1]"
    assert str(10 - item) == "10 - arr[1]"
    assert str(2 * item) == "2 * arr[1]"
    assert str(10 / item) == "10 / arr[1]"
    assert str(10 % item) == "10 % arr[1]"


def test_reverse_operators_expression():
    expr = EVAL("fn", 1)

    assert str(1 + expr) == "1 + fn(1)"
    assert str(10 - expr) == "10 - fn(1)"
    assert str(2 * expr) == "2 * fn(1)"
    assert str(10 / expr) == "10 / fn(1)"
    assert str(10 % expr) == "10 % fn(1)"
