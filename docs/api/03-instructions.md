# Instructions

Instructions are calls to the EasyBuilder macro standard functions.

Currently, not all instructions are available since it has been fairly time consuming to add copy them from the EasyBuilder Pro app.

Similarly, the documentation for them is limited but it is fairly similar to the one available in the app.

Nevertheless, here is the documentation of most common instructions.


## Instructions

### GetData
Usage:
```python
GetData(read_data:AnyVariable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False)
```
- `read_data`: Must be a `Variable` or a `VariableItem` [see more](02-syntax.md#variables). The data will be read from the device and written to this variable and the following elements (if applicable).
- `device_name`: A string of the name of the device to read from.
- `address`: Either a string wrapped in `"` or using `string_literal(value)` unless `dont_format` is False. It can also be a `tuple` of `(str, int)` to give the exact address of the tag.
- `dont_format`: When `False`, ensures that if a string is provided, it is wrapped in `"`. This can be set to `True` when a special address encoding is required (for example, some PLCs have special formatting of their addresses). When `True`, the address string will be left unchanged and simply forwarded to the call.

Examples:
```python
GetData(my_var, "Local HMI", ("LB", 20))
GetData(my_var, "Local HMI", "LB,20", 1, True)
# Both above are equivalent
# > GetData(my_var, "Local HMI", LB,20, 1)

GetData(my_var, "Local HMI", "my_tag")
GetData(my_var, "Local HMI", string_literal("my_tag"), 1, True)
# Both above are equivalent
# > GetData(my_var, "Local HMI", "my_tag", 1)

GetData(my_var, "Remote PLC", "DB1.Value", 1, True)
# > GetData(my_var, "Remote PLC", DB1.Value, 1)

GetData(my_arr[1], "Local HMI", ("LB", 20), 10)
# > GetData(my_arr[1], "Local HMI", LB,20, 10)
```


### SetData
Usage:
```python
SetData(send_data:AnyVariable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False)
```
- `send_data`: Must be a `Variable` or a `VariableItem` [see more](02-syntax.md#variables). The data will be read to this variable and the following elements (if applicable) and sent to the device.
- `device_name`: A string of the name of the device to write to.
- `address`: Either a string wrapped in `"` or using `string_literal(value)` unless `dont_format` is False. It can also be a `tuple` of `(str, int)` to give the exact address of the tag.
- `dont_format`: When `False`, ensures that if a string is provided, it is wrapped in `"`. This can be set to `True` when a special address encoding is required (for example, some PLCs have special formatting of their addresses). When `True`, the address string will be left unchanged and simply forwarded to the call.

Examples:
```python
SetData(my_var, "Local HMI", ("LB", 20))
SetData(my_var, "Local HMI", "LB,20", 1, True)
# Both above are equivalent
# > SetData(my_var, "Local HMI", LB,20, 1)

SetData(my_var, "Local HMI", "my_tag")
SetData(my_var, "Local HMI", string_literal("my_tag"), 1, True)
# Both above are equivalent
# > SetData(my_var, "Local HMI", "my_tag", 1)

SetData(my_var, "Remote PLC", "DB1.Value", 1, True)
# > SetData(my_var, "Remote PLC", DB1.Value, 1)

SetData(my_arr[1], "Local HMI", ("LB", 20), 10)
# > SetData(my_arr[1], "Local HMI", LB,20, 10)
```

|[Previous](02-syntax.md) | [Index](../index.md) | [Next](04-how-does-it-work.md) |
|:-|:-:|-:|