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

For an in depth dive into variables, [see this](04-how-does-it-work.md#variables)
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
This includes variables, variable array items, operations, python base types (`bool`, `int`, `float`, `str`).

A more detailed description can be found [here](04-how-does-it-work.md#expressions).

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
- Some [instructions](03-instructions.md), more specifically, [evals](04-how-does-it-work.md#evals)

## Statements
A Statement is an single (or a collection) of macro statements. Contrarily to expressions, statements do not evaluate to a value, they only evaluate to macro instructions.

## Keywords

### COMMENT
Usage:
```python
with macro:
    macro.write(
        COMMENT("""comment"""),
    )
```

### IF/ELIF/ELSE
This is the natural implementation of the `IF` statements. It provides a mostly intuitive method for creating conditional structures.

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

### C_IF/C_ELIF/C_ELSE/C_END_IF
This is a custom implementation for `IF` statements. It provides more fine-tuned control over the `IF` statements. It does come with the risk of forgetting to add `C_END_IF` to close to opened if.

Usage:
```python
with macro:
    macro.write(
        C_IF("""expression"""),
        ...
        C_END_IF(),
    )

    macro.write(
        C_IF("""expression"""),
        ...
        C_ELIF("""expression"""),
        ...
        C_END_IF(),
    )

    macro.write(
        C_IF("""expression"""),
        ...
        C_ELIF("""expression"""),
        ...
        C_ELSE(),
        ...
        C_END_IF(),
    )

    macro.write(
        C_IF("""expression"""),
        ...
        C_ELSE(),
        ...
        C_END_IF(),
    )
```

Example:
```python
with macro:
    var1 = vint("var1")

    for i in range(10):
        if i == 0:
            macro.write(
                C_IF(var1 == i),
            )
        else:
            macro.write(
                C_ELIF(var1 == 1),
            )
        macro.write(
            ...
        )
    macro.write(
        C_ELSE(),
        ...
        C_END_IF(),
    )
```

### SWITCH
A switch case structure.

Usage:
```python
with macro:
    short_var = vshort("short_var", 0)
    macro.write(
        SWITCH(short_var)(
            CASE(0)(
                COMMENT("Hi"),
            ),
            CASE(1)(
                COMMENT("Hello"),
            ),
        )
    )
```

### BLOCK
A container for a collection of statements. It is often useful to inline a collection of statements.

Usage:
```python
with macro:
    macro.write(
        BLOCK(
            ...
        )
    )
```

Example:
```python
with macro:
    macro.write(
        *[BLOCK(
            COMMENT(f"Statement {i}"),
            EMPTY(),
        ) for i in range(10)],
    )
```

|[Previous](01-getting-started.md) | [Index](../index.md) | [Next](03-instructions.md) |
|:-|:-:|-:|