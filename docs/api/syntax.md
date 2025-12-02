# Syntax

This part will explain the basic elements of the syntax for the macro generator.

## Macro

A macro is just a container for the code to be generated.
It can be used like so:
```python
macro = Macro("Macro name", "Macro description")

with macro:
    macro.write(
        ...
    )
```

## Variables

Here is the list of available variables:

| EasyBuilder name | eb_macro_gen name |
| ---------------- | ----------------- |
| unsigned char    | vuchar            |
| char             | vchar             |
| unsigned short   | vushort           |
| short            | vshort            |
| unsigned int     | vuint             |
| int              | vint              |
| unsigned long    | vulong            |
| long             | vlong             |
| bool             | vbool             |
| float            | vfloat            |
| double           | vdouble           |

Here is an example of how to define a variable:
```python
my_bool = vbool("my_bool", False) # A bool with a default value
# > bool my_bool = false

my_float = vfloat("my_float") # A float without a default value
# > float my_float
```

It is also possible to declare arrays:
```python
my_bool_arr = vbool_arr("my_bool_arr", 5, [False, True, 0, 1, 0])
# > bool my_bool_arr[5] = {0, 1, 0 , 1, 0}

my_float_arr = vfloat_arr("my_float_arr", 5)
# > float my_float_arr[5]
```

To use these variables, you can't simply use the `=` operator as it would actually modify the contained type. Instead, use the `set` method:
```python
with macro:
    macro.write(
        my_bool.set(1),
        my_bool.set(~my_bool),
        my_float.set(my_bool),
        my_float.set(my_int + 10),

        # Arrays are an exception since the __setitem__ method is called
        my_bool_arr[1] = 1,
    )
```

## Expressions
An expression is anything that can be turned into a value.
This includes variables, variable array items, operations, python base types (bool, int, float, str).

Here are some examples:
- `True` `False`
- `1` `2` `-1`
- `0.5`
- `my_var`
- `my_var | my_other_var` `my_var & my_other_var`
- `~my_var`
- `my_var + 1` `my_var - 1` `my_var + my_other_var`
- `my_var * 10` `my_var / 10` `my_var * my_other_var`
- `(my_var + 10) / my_other_var`
- `10 + 50`

## Keywords

### COMMENT
Usage:
```python
with macro:
    macro.write(
        COMMENT("""comment"""),
    )
```

### IF
Usage:
```python
with macro:
    macro.write(
        IF("""expression""")(
            # Body
        ).ELIF("""expression""")(
            # Body
        ).ELIF("""expression""")(
            # Body
        ).ELSE()(
            # Body
        ),
    )
```