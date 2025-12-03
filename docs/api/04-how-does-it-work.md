# How does it work?

In order to see how everything works, you should take a look at [syntax.py](../../src/eb_macro_gen/syntax.py). But in case it's a bit overwhelming, here is an explanation of the core principles.

## Resources
`Resource` is the base class for every element that can be contained in a `Macro`.

A `Resource` is composed of a few elements:
- `resources`: A set of other resources used by this resource.
- `_id`: An integer used to differentiate between subclasses that don't override `__hash__` (for example `STATEMENT`).
- `__hash__`: Need to be implemented to allow being contained in a `set`. This also prevents resources from being processed more than once.
- `process(self, macro:Macro)`: A method that gets called by the containing macro before converting its `STATEMENT`s into strings.

## Statements
A `STATEMENT` is a `Resource` that acts as an actual EasyBuilder Pro macro statement or, in some cases, a collection of statements.

A `STATEMENT` is defines a few methods:
- `__str__`: This is called by the `bake` method to actually convert the statement into its macro representation.
- `bake(self, macro:Macro)`: Writes to the `Macro`'s buffer.

## Expressions
An `EXPRESSION` is a `Resource` that represents any operation that can be evaluated into a value.

More information can be found [here](02-syntax.md#expressions).

It defines `__str__` which is used to get the macro code representation of the expression.

It also overloads most python operators for ease of use. That means that you can create python expressions and the result would be an expression representing the chain of expressions provided. For example:
```python
var1 = vbool("var1")
var2 = vint("var2")
var3 = vint("var3")

with macro:
    macro.write(
        IF((True | var1) & (var2 > 10) & (var3 != (5 + var2)))(
            ...
        )
        # > if (1 or var1) and (var2 > 10) and (var3 <> (5 + var2)) then
        # >     ...
        # > end if
    )
```

## Assignments
An `ASSIGNMENT` is a `STATEMENT` that represents the assignment of an `EXPRESSION` to a `Variable`.

## Calls
A `CALL` is a `STATEMENT` that represents a function call, mostly used to define the [instructions](03-instructions.md).

## Evals
An `EVAL` is similar to a `CALL` except it is actually an `EXPRESSION`. It is also mostly used to define the [instructions](03-instructions.md).

## Variables
`Variable`s are described a bit [here](02-syntax.md#variables), but here is a more detailed explanation. A `Variable` is a `Resource` but it has its own way to be contained in a `Macro`. `Macro` actually has a storage specifically for variables in order to define variables at the beginning of the macro. This is possible thanks to the `process` method. At process-time, the variables are added to the `Macro`s variable `set`

|[Previous](03-instructions.md) | [Index](../index.md) | [Next]() |
|:-|:-:|-:|