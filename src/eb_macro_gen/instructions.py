from __future__ import annotations
from typing import Tuple
from .syntax import *

def ACOS(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the arcosine of the source.

[Usage]
`ACOS(source, result)`

[Example]
```
float source = 0.5, result

ACOS(source, result)//  result == 60
```
    """
    return CALL('ACOS', source, result)

def ADDSUM(start:VariableItem[DT], result:AnyVariable[DT], count:AnyInt) -> CALL:
    """
[Description]
Use addition to calculate checksum.

[Usage]
`ADDSUM(source[start], result, count)`

[Example]
```
char data[5] = {1, 2, 3, 4, 5}
char checksum

ADDSUM(data[0], checksum, 5)
```
    """
    return CALL('ADDSUM', start, result, count)
    
def ASCII2DEC(start:VariableItem[int], result:AnyVariable[int], count:AnyInt) -> CALL:
    """
[Description]
Convert a string to a decimal value.

[Usage]
`ASCII2DEC(source[start], result, count)`

[Example]
```
char source[4] = {'5', '6', '7', '8'}

short result
ASCII2DEC(source[0], result, 4)//  result == 5678
```
    """
    return CALL('ASCII2DEC', start, result, count)

def ASCII2DOUBLE(start:VariableItem[int], result:AnyVariable[float], count:AnyInt) -> CALL:
    """
[Description]
Convert a string to a floating value.

[Usage]
`ASCII2DOUBLE(source[start], result, count)`

[Example]
```
char source[4] = {'5', '6', '.', '8'}

double result
ASCII2DOUBLE(source[0], result, 4)//  result == 56.8
```
    """
    return CALL('ASCII2DOUBLE', start, result, count)

def ASCII2FLOAT(start:VariableItem[int], result:AnyVariable[float], count:AnyInt) -> CALL:
    """
[Description]
Convert a string to a floating value.

[Usage]
`ASCII2FLOAT(source[start], result, count)`

[Example]
```
char source[4] = {'5', '6', '.', '8'}

float result
ASCII2FLOAT(source[0], result, 4)//  result == 56.8
```
    """
    return CALL('ASCII2FLOAT', start, result, count)

def ASCII2HEX(start:VariableItem[int], result:AnyVariable[int], count:AnyInt) -> CALL:
    """
[Description]
Convert a string to a hexadecimal value.

[Usage]
`ASCII2HEX(source[start], result, count)`

[Example]
```
char source[4] = {'5', '6', '7', '8'}

short result
ASCII2HEX(source[0], result, 4)//  result == 0x5678
```
    """
    return CALL('ASCII2HEX', start, result, count)

def ASIN(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the arcsine of the source.

[Usage]
`ASIN(source, result)`

[Example]
```
float source = 0.5, result

ASIN(source, result)//  result == 30
```
    """
    return CALL('ACOS', source, result)

def ASYNC_TRIG_MACRO(macro:Union[int, EXPRESSION, Variable[int], VariableItem[int], str, LITERAL]) -> CALL:
    """
[Description]
This function will trigger the designated MACRO
and continue the next instructions.
[Usage]
```
ASYNC_TRIG_MACRO(macro_id)//  macro_id is a constant or variable
ASYNC_TRIG_MACRO("macro_name")//  macro_name is a string

ASYNC_TRIG_MACRO(5)//  execute MACRO 5
ASYNC_TRIG_MACRO("check_status")
//  if the name of macro 5 is "check_status", MACRO 5 will be triggered.
```
    """
    return CALL('ASYNC_TRIG_MACRO', ensure_string_is_literal(macro))

def ATAN(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the arctangent of the source.

[Usage]
`ATAN(source, result)`

[Example]
```
float source = 1, result

ATAN(source, result)//  result == 45
```
    """
    return CALL('ATAN', source, result)

def AVERAGE(start:VariableItem[DT], result:AnyVariable[DT], count:AnyInt) -> CALL:
    """
[Description]
Get the average value from array.

[Usage]
`AVERAGE(source[start], result, count)`

[Example]
```
int data[5] = {1, 2, 3, 4, 5}
float result

AVERAGE(data[0], result, 5)
// result = 3

AVERAGE(data[2], result, 3)
// result = 4
```
    """
    return CALL('AVERAGE', start, result, count)

def BCC(start:VariableItem[int], result:AnyVariable[int], count:AnyInt) -> CALL:
    """
[Description]
BCC (Block Check Character) uses XOR (Exclusive OR) to calculate checksum.

[Usage]
`BCC(source[start], result, count)`

[Example]
```
char source[5] = {1, 2, 3, 4, 5}
char checksum

BCC(source[0], checksum, 5)
```
    """
    return CALL('BCC', start, result, count)

def BCD2BIN(source:AnyInt, result:AnyVariable[int]) -> CALL:
    """
[Description]
Convert a BCD value to a BIN value.

[Usage]
`BIN2BCD(source, result)`

[Example]
```
short source = 0x1234, result

BIN2BCD(source, result)//  result == 1234
BCD2BIN(0x3456, result)//  result == 3456
```
    """
    return CALL('BCD2BIN', source, result)

def Beep() -> CALL:
    """
[Description]
Play beep sound.

[Usage]
`Beep()`

[Example]
```
Beep()
```
    """
    return CALL('Beep')

def BIN2BCD(source:AnyInt, result:AnyVariable[int]) -> CALL:
    """
[Description]
Convert a binary value to a BCD value.

[Usage]
`BIN2BCD(source, result)`

[Example]
```
short source = 1234, result

BIN2BCD(source, result)//  result == 0x1234
BIN2BCD(3456, result)//  result == 0x3456
```
    """
    return CALL('BIN2BCD', source, result)

def Buzzer(state:AnyVariable[int]) -> CALL:
    """
[Description]
Turn on/off the buzzer.
Require OS version 20140618 or later and simulation modes do not support this function.
[Usage]
`Buzzer(on_off)//  Turn on the buzzer if on_off is nonzero, otherwise turn off the buzzer.`

[Example]
```
char on = 1, off = 0

Buzzer(on)	//  turn on the buzzer
DELAY(1000)	//  delay 1 second
Buzzer(off)	//  turn off the buzzer
DELAY(500)	//  delay 500ms
Buzzer(1)	//  turn on the buzzer
DELAY(1000)	//  delay 1 second
Buzzer(0)	//  turn off the buzzer
```
    """
    return CALL('Buzzer', state)

def CEIL(source:AnyFloat) -> EVAL[float]:
    """
[Description]
Get the smallest integral value that is not less than input.

[Usage]
`result = CEIL(source)`

[Example]
```
float x = 3.8
int result

result = CEIL(x)
// result = 4
```
    """
    return EVAL('CEIL', source)

def COS(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the cosine of the source.

[Usage]
`COS(source, result)`

[Example]
```
float source = 60, result

COS(source, result)//  result == 0.5
COS(90, result)//  result == 0
```
    """
    return CALL('COS', source, result)

def COT(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the cotangent of the source.

[Usage]
`COT(source, result)`

[Example]
```
float source = 45, result

COT(source, result)//  result == 1
```
    """
    return CALL('COT', source, result)

def CRC(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 16-bit CRC(CRC-16/MODBUS).

[Usage]
`CRC(source[start], result, count)`

[Example]
```
char source[5] = {1, 2, 3, 4, 5}
short crc_result

CRC(source[0], crc_result, 5)
```
    """
    return CALL('CRC', start, result, count)

def CRC16_CCITT(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 16-bit CRC(CRC-16/CCITT).

[Usage]
`CRC16_CCITT(source[start], result, count)`

[Example]
```
char source[5] = "12345"
short crc_result

CRC16_CCITT(source[0], crc_result, 5)
```
    """
    return CALL('CRC16_CCITT', start, result, count)

def CRC16_CCITT_FALSE(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 16-bit CRC(CRC-16/CCITT-FALSE).

[Usage]
`CRC16_CCITT_FALSE(source[start], result, count)`

[Example]
```
char source[5] = "12345"
short crc_result

CRC16_CCITT_FALSE(source[0], crc_result, 5)
```
    """
    return CALL('CRC16_CCITT_FALSE', start, result, count)

def CRC16_X25(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 16-bit CRC(CRC-16/X25).

[Usage]
`CRC16_X25(source[start], result, count)`

[Example]
```
char source[5] = "12345"
short crc_result

CRC16_X25(source[0], crc_result, 5)
```
    """
    return CALL('CRC16_X25', start, result, count)

def CRC16_XMODEM(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 16-bit CRC(CRC-16/XMODEM).

[Usage]
`CRC16_XMODEM(source[start], result, count)`

[Example]
```
char source[5] = "12345"
short crc_result

CRC16_XMODEM(source[0], crc_result, 5)
```
    """
    return CALL('CRC16_XMODEM', start, result, count)

def CRC8(start:VariableItem[int], result:AnyVariable, count:AnyInt) -> CALL:
    """
[Description]
Get 8-bit CRC.

[Usage]
`CRC8(source[start], result, count)`

[Example]
```
char source[5] = {1, 2, 3, 4, 5}
short CRC8_result

CRC8(source[0], CRC8_result, 5)
// CRC8_result = 188
```
    """
    return CALL('CRC8', start, result, count)

def CSC(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the cosecant of the source.

[Usage]
`CSC(source, result)`

[Example]
```
float source = 30, result

CSC(source, result)//  result == 2
```
    """
    return CALL('CSC', source, result)

def CUBERT(source:AnyValue[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the cube root of the source.

[Usage]
`CUBERT(source, result)`

[Example]
```
float source = 27, result

CUBERT(source, result)//  result == 3
```
    """
    return CALL('CUBERT', source, result)

def DATE2ASCII(day_offset:AnyInt, start:VariableItem[int], count:AnyInt, separator:str = "/") -> CALL:
    """
[Description]
Convert the date (year, month and day) to a string in "YYYY/MM/DD" 
format with "day_offset" from today.

[Usage]
```
DATE2ASCII(day_offset, date[start], count) //default separator is '/' 
DATE2ASCII(day_offset, date[start], count, separator)
char result[10]

DATE2ASCII(5, result[0], 10)
//  result[0]~[9] == "2019/02/16"//  today is 2019/02/11
DATE2ASCII(5, result[0], 10, "-")
//  result[0]~[9] == "2019-02-16"//  today is 2019/02/11
```
    """
    if len(separator) > 1:
        raise ValueError("Separator must be of length 1")
    return CALL('DATE2ASCII', day_offset, start, count, f"'{separator}'")

def DATE2DEC(day_offset:AnyInt, date:AnyVariable[int]) -> CALL:
    """
[Description]
Convert the date (year, month and day) to a decimal value in "YYYYMMDD" 
format with "day_offset" from today.

[Usage]
`DATE2DEC(day_offset, date)`

[Example]
```
int day_offset = 5, date

DATE2DEC(0, date)//  date == 20190211 (today is 2019/02/11)
DATE2DEC(day_offset, date)//  date == 20190216 (20190211 + 5)
```
    """
    return CALL('DATE2DEC', day_offset, date)

def DEC2ASCII(source:AnyVariable[int], result:VariableItem[int], count:AnyInt) -> CALL:
    """
[Description]
Convert a decimal value to a string.

[Usage]
`DEC2ASCII(source, result[start], count)`

[Example]
```
short source = 5678
char result[4]

DEC2ASCII(source, result[0], 4)
//  result[0] == '5', result[1] == '6', result[2] == '7', result[3] == '8'
```
    """
    return CALL('DEC2ASCII', source, result, count)

def RecipeGetData(destination:AnyVariable, recipe_address:str, record_id:AnyVariable[int]) -> CALL:
    """
[Description]
Read data from recipe. If success, returns true, else, returns false.
The type name and item name given by recipe address specify the location of data being read.

[Usage]
`RecipeGetData(destination, recipe address, record ID)`

[Example]
```
int data=0
char str[20]
int recordID
bool result

recordID = 0
result = RecipeGetData(data, "TypeA.item_weight", recordID)
// get data from recipe "TypeA", where item name is "item_weight" and the record ID is 0.

recordID = 1
result = RecipeGetData(str[0], "TypeB.item_name", recordID)
// get data from recipe "TypeB", where item name is "item_name" and the record ID is 1.
```
    """
    return CALL('RecipeGetData', destination, ensure_string_is_literal(recipe_address), record_id)

def RecipeQuery(query:Union[str, VariableItem[int], LITERAL], destination:AnyVariable) -> EVAL:
    """
[Description]
Execute a SQL query. If success, returns true, else, returns false.
The total number of rows of query result is written to destination.

[Usage]
```
result = RecipeQuery("SELECT * FROM ...", destination)
result = RecipeQuery(source[start], destination)
```

[Example]
```
int total_row=0
char sql[100]="SELECT * FROM TypeB"
bool result

result = RecipeQuery("SELECT * FROM TypeA", total_row)
// Query "TypeA". The total number of rows of query result is written to total_row.

result = RecipeQuery(sql[0], total_row)
// Query "TypeB". The total number of rows of query result is written to total_row.
```
    """
    return EVAL('RecipeQuery', ensure_string_is_literal(query), destination)

def RecipeQueryGetData(destination:AnyVariable, recipe_address:Union[str, LITERAL], result_row:AnyVariable[int]) -> EVAL:
    """
[Description]
Read data from query result. If success, returns true, else, returns false.
The type name and item name given by recipe address specify the location of data being read.
To call this function, users need to call RecipeQuery first to obtain the query result.

[Usage]
`RecipeQueryGetData(destination, recipe address, result row no.)`

[Example]
```
int data=0
int total_row=0
int row_number=0
bool result_query
bool result_data

result_query = RecipeQuery("SELECT * FROM TypeA", total_row)
// Query "TypeA". The total number of rows of query result is written to total_row.
if (result_query) then
    for row_number=0 to total_row-1
        result_data = RecipeQueryGetData(data, "TypeA.item_weight", row_number)
    next row_number
end if
```
    """
    return EVAL('RecipeQueryGetData', destination, ensure_string_is_literal(recipe_address), result_row)

def RecipeQueryGetRecordID(destination:AnyVariable[int], result_row:AnyVariable[int]) -> EVAL:
    """
[Description]
Get the record ID from query result. If success, returns true, else, returns false.
The record ID is written to the destination.
To call this function, users need to call RecipeQuery first to obtain the query result.

[Usage]
`RecipeQueryGetRecordID(destination, result row no.)`

[Example]
```
int recordID=0
int total_row=0
int row_number=0
bool result_query
bool result_id

result_query = RecipeQuery("SELECT * FROM TypeA", total_row)
// Query "TypeA". The total number of rows of query result is written to total_row.
if (result_query) then
    for row_number=0 to total_row-1
        result_id = RecipeQueryGetRecordID(recordID, row_number)
    next row_number
end if
```
    """
    return EVAL('RecipeQueryGetRecordID', destination, result_row)

def RecipeSetData(source:AnyVariable, recipe_address:Union[str, LITERAL], record_id:AnyVariable[int]) -> EVAL:
    """
[Description]
Write data to recipe. If success, returns true, else, returns false.
The type name and item name given by recipe address specify the location of data being written.

[Usage]
`RecipeSetData(source, recipe address, record ID)`

[Example]
```
int data=99
char str[20]="abc"
int recordID
bool result

recordID = 0
result = RecipeSetData(data, "TypeA.item_weight", recordID)
// set data to recipe "TypeA", where item name is "item_weight" and the record ID is 0.

recordID = 1
result = RecipeSetData(str[0], "TypeB.item_name", recordID)
// set data to recipe "TypeB", where item name is "item_name" and the record ID is 1.
```
    """
    return EVAL('RecipeSetData', source, ensure_string_is_literal(recipe_address), record_id)

def RecipeTransactionBegin() -> CALL:
    """
[Description]
Data base begin transaction.

[Usage]
`RecipeTransactionBegin()`

[CAUTION]
When a recipe transaction begin, it will block other recipe actions until committed,
rolled back or macro ends(rolled back will be used).
Best practice is to prepare data before beginning transactions,
such as calling GetData before transactions.

[Example]
```
RecipeTransactionBegin()// begin transaction
```
    """
    return CALL('RecipeTransactionBegin')

def RecipeTransactionCommit() -> CALL:
    """
[Description]
Data base commit transaction.

[Usage]
`RecipeTransactionCommit()`

[Example]
```
RecipeTransactionBegin()// begin transaction
RecipeTransactionCommit()// commit transaction
```
    """
    return CALL('RecipeTransactionCommit')

def RecipeTransactionRollback() -> CALL:
    """
[Description]
Data base rollback transaction.

[Usage]
`RecipeTransactionRollback()`

[Example]
```
RecipeTransactionBegin()// begin transaction
RecipeTransactionRollback()// rollback transaction
```
    """
    return CALL('RecipeTransactionRollback')

def SYNC_TRIG_MACRO(macro:Union[int, EXPRESSION, Variable[int], VariableItem[int], str, LITERAL]) -> CALL:
    """
[Description]
This function will trigger the designated MACRO and wait for the end
of the execution of this designated MACRO.
[Usage]
```
SYNC_TRIG_MACRO(macro_id)//  macro_id is a constant or variable
SYNC_TRIG_MACRO("macro_name")//  macro_name is a string

SYNC_TRIG_MACRO(5)//  execute MACRO 5
SYNC_TRIG_MACRO("check_status")
//  if the name of macro 5 is "check_status", MACRO 5 will be triggered.
```
    """
    return CALL('SYNC_TRIG_MACRO', ensure_string_is_literal(macro))

def TRACE(fmt:Union[str, LITERAL], *values:AnyValue) -> CALL:
    """
[Description]
Trace the variables and send specified string to the debugger.

[Usage]
`TRACE("")`

[Example]
```
int a = 100

TRACE(" a = %d", a)
```
    """
    return CALL('TRACE', string_literal(fmt), *[ensure_string_is_literal(v) for v in values])
    
def INFO(fmt:str, *values:AnyValue) -> CALL:
    """
[Description]
Trace the variables and send specified string to the debugger.

[Usage]
`INFO("")`

[Example]
```
int a = 100

INFO(" a = %d", a)
```
    """
    return TRACE("[INFO] " + fmt, *values)

def WARN(fmt:str, *values:AnyValue) -> CALL:
    """
[Description]
Trace the variables and send specified string to the debugger.

[Usage]
`WARN("")`

[Example]
```
int a = 100

WARN(" a = %d", a)
```
    """
    return TRACE("[WARN] " + fmt, *values)

def ERROR(fmt:str, *values:AnyValue) -> CALL:
    """
[Description]
Trace the variables and send specified string to the debugger.

[Usage]
`ERROR("")`

[Example]
```
int a = 100

ERROR(" a = %d", a)
```
    """
    return TRACE("[ERROR] " + fmt, *values)

def SetData(send_data:AnyVariable, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """
    Args:
        send_data (AnyVariable): The variable from which the data will be sent
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt], optional): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        SetDataEx(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True). Defaults to 1.
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.
    
```
SetData(send_data[start], device_name, device_type, address_offset,
data_count)
or
SetData(send_data, device_name, device_type, address_offset, 1)
```

Sends data to the device. Data is defined in send_data[start]~ send_data[start +data_count - 1].
data_count is the amount of sent data. In general, send_data is an array, but if
data_count is 1, send_data can be an array or an ordinary variable. Below are
two methods to send one word data.

macro_command main()
short send_data_1[2] = { 5, 6}, send_data_2 = 5
SetData(send_data_1[0], "FATEK KB Series", RT, 5, 1)
SetData(send_data_2,      "FATEK KB Series", RT, 5, 1)
end macro_command

device_name is the device name enclosed in the double quotation marks (")
and this name has been defined in the device list of system parameters.
device_type is the device type and encoding method (binary or BCD) of the
device data. For example, if device_type is LW_BIN, it means the register is LW
and the encoding method is binary. If use BIN encoding method, "_BIN" can be

ignored.
If device_type is LW_BCD, it means the register is LW and the encoding method
is BCD.
address_offset is the address offset in the device.
For example, SetData(read_data_1[0], "FATEK KB Series", RT, 5, 1) represents
that the address offset is 5.
If address_offset uses the format -"N#AAAAA", N indicates that device's station
number is N. AAAAA represents the address offset. This format is used while
multiple devices or controllers are connected to a single serial port. For
example, SetData(read_data_1[0], "FATEK KB Series", RT, 2#5, 1) represents
that the device's station number is 2. If SetData () uses the default station
number defined in the device list, it is not necessary to define station number
in address_offset.

The number of registers actually sends to depends on both the type of the
send_data variable and the value of the number of data_count.

```
|                     |            | actual number of     |
| type of read_data   | data_count | 16-bit register read |
|---------------------+------------+----------------------|
| char (8-bit)        | 1          | 1                    |
| char (8-bit)        | 2          | 1                    |
| bool (8-bit)        | 1          | 1                    |
| bool (8-bit)        | 2          | 1                    |
| short (16-bit)      | 1          | 1                    |
| short (16-bit)      | 2          | 2                    |
| int (32-bit)        | 1          | 2                    |
| int (32-bit)        | 2          | 4                    |
| float (32-bit)      | 1          | 2                    |
| float (32-bit)      | 2          | 4                    |
```
Example

When a SetData() is executed using a 32-bit data type (int or float), the function
will automatically send int-format or float-format data to the device. For
example,

```
macro_command main()
float f = 2.6
SetData(f, "MODBUS", 6x, 2, 1)      // will send a floating point value to the
device
end macro_command
macro_command main()
int i
bool a = true
bool b[30]
short c = false
short d[50]
int e = 5
int f[10]

for i = 0 to 29
b[i] = true
next i

for i = 0 to 49
d[i] = i * 2
next i

for i = 0 to 9
f [i] = i * 3
next i

//  set the state of LB2
SetData(a, "Local HMI", LB, 2, 1)

//    set the states of LB0 ~ LB29
SetData(b[0], "Local HMI", LB, 0, 30)

//    set the value of LW-2
SetData(c, "Local HMI", LW, 2, 1)

//    set the values of LW-0 ~ LW-49
SetData(d[0], "Local HMI", LW, 0, 50)

//    set the values of LW-6 ~ LW-7,    note that the type of e is int
SetData(e, "Local HMI", LW, 6, 1)

//    set the values of LW-0 ~ LW-19
// 10 integers equal to 20 words, since each integer value occupies 2 words.
SetData(f[0], "Local HMI", LW, 0, 10)

end macro_command
```
    """
    if data_count is None:
        return CALL('SetData', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('SetData', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def SetDataEx(send_data:AnyVariable, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """Write data to a device and continue executing next command
even if no response from this device.

    Args:
        send_data (AnyVariable): The variable from which the data will be sent
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt], optional): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        SetDataEx(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True). Defaults to 1.
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.

[Usage]
`SetDataEx(desti, PLC name, device type, address, data count)`

[Example]
```
char byData[10]
short wData[6]

FILL(byData[0], 0, 10)//  set buffers to a specified value
FILL(wData[0], 0, 6)

SetDataEx(byData[0], "Local HMI", LW, 0, 10)//  send 10 bytes = 5 words
SetDataEx(wData[0], "Local HMI", LW, 0, 6)//  send 6 words
SetDataEx(wData[0], "Local HMI", "Pressure", 6
//  use user-defined tag - "Pressure" to indicate device type and address.
```
    """
    if data_count is None:
        return CALL('SetDataEx', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('SetDataEx', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetData(read_data:AnyVariable, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """
    Args:
        read_data (AnyVariable): The variable in which the data will be stored
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt], optional): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        GetData(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True). Defaults to 1.
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.

```
GetData(read_data[start], device_name, device_type, address_offset,
data_count)
or
GetData(read_data, device_name, device_type, address_offset, 1)
```

Receives data from the device. Data is stored into read_data[start]~read_data[start + data_count - 1].
data_count is the amount of received data. In general, read_data is an array,
but if data_count is 1, read_data can be an array or an ordinary variable. Below
are two methods to read one word data from the device.

macro_command main()
short read_data_1[2], read_data_2
GetData(read_data_1[0], "FATEK KB Series", RT, 5, 1)
GetData(read_data_2,      "FATEK KB Series", RT, 5, 1)
end macro_command

Device_name is the deivce name enclosed in the double quotation marks (“)
and this name has been defined in the device list of system parameters as
follows (see FATEK KB Series):

Device_type is the device type and encoding method (binary or BCD) of the
device data. For example, if device_type is LW_BIN, it means the register is LW
and the encoding method is binary. If use BIN encoding method, "_BIN" can be
ignored.
If device_type is LW_BCD, it means the register is LW and the encoding method
is BCD.
Address_offset is the address offset in the device.
For example, GetData(read_data_1[0], "FATEK KB Series", RT, 5, 1) represents
that the address offset is 5.
If address_offset uses the format -"N#AAAAA", N indicates that deivce's
station number is N. AAAAA represents the address offset. This format is used
while multiple devices or controllers are connected to a single serial port. For
example, GetData(read_data_1[0], "FATEK KB Series", RT, 2#5, 1) represents
that the deivce's station number is 2. If GetData() uses the default station
number defined in the device list as follows, it is not necessary to define station
number in address_offset.

The number of registers actually read from depends on both the type of the

read_data variable and the value of the number of data_count.

```
|                     |            | actual number of     |
| type of read_data   | data_count | 16-bit register read |
|---------------------+------------+----------------------|
| char (8-bit)        | 1          | 1                    |
| char (8-bit)        | 2          | 1                    |
| bool (8-bit)        | 1          | 1                    |
| bool (8-bit)        | 2          | 1                    |
| short (16-bit)      | 1          | 1                    |
| short (16-bit)      | 2          | 2                    |
| int (32-bit)        | 1          | 2                    |
| int (32-bit)        | 2          | 4                    |
| float (32-bit)      | 1          | 2                    |
| float (32-bit)      | 2          | 4                    |
```
Example
When a GetData() is executed using a 32-bit data type (int or float), the
function will automatically convert the data. For example,

```
macro_command main()
float f
GetData(f, "MODBUS", 6x, 2, 1)      // f will contain a floating point value
end macro_command
macro_command main()
bool a
bool b_array[30]
char c
char c_array[20]
short s
short s_array[50]
int i
int i_array[10]
float f
float f_array[15]double g[10]

//    get the state of LB2 to the variable a
GetData(a, "Local HMI", LB, 2, 1)

//    get 30 states of LB0 ~ LB29 to the variables b_array[0] ~ b_array[29]
GetData(b_array[0], "Local HMI", LB, 0, 30)

//    get lower byte of LW-0 to the variable c
//    note that char is 1 byte, and a LW address occupies 2 bytes (1 word).
Reading the first byte in a word register will get the lower byte of the word.
//    Ex: when the value in LW-0 is 0x0201, then variable c will read 0x01
GetData(c, "Local HMI", LW, 0, 1)

//    get data of LW1 ~ LW10 to the c_array[0] ~ c_array[19]

GetData(c_array[0], "Local HMI", LB, 0, 20)

//    get one word from LW-2 to the variable s
GetData(s, "Local HMI", LW, 2, 1)

//    get 50 words from LW-0 ~ LW-49 to the variables s_array[0] ~ s_array[49]
GetData(s_array[0], "Local HMI", LW, 0, 50)

//    get 2 words from LW-6 ~ LW-7 to the variable e
//    Ex: When value in LW-6 is 0x0002, in LW-7 is 0x0001, then i will read
0x00010002(65538)
//    note that int occupies 2 words (32-bit)
GetData(i, "Local HMI", LW, 6, 1)

//    get 20 words (10 integer values) from LW-0 ~ LW-19 to variables i_array[0]
~ i_array[9], note that type of i_array[10] is int.
GetData(i_array[0], "Local HMI", LW, 0, 10)

//    get data from LW-10 ~ LW-11 to the variable f
//    note that type of variable f is float.
GetData(f, "Local HMI", LW, 10, 1)

//    get 30 words (15 float variables) from LW-0 ~ LW-29 to variables f_array[0]
~ f_array[14], note that type of f_array[15] is float.
//    note that float occupies 2 words (32-bit)
GetData(f_array[0], "Local HMI", LW, 0, 15)

end macro_command
```
    """
    if data_count is None:
        return CALL('GetData', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('GetData', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetDataEx(read_data:AnyVariable, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """Read data from a device and continue executing next command even if no response from this device.
    Warning : Must use GetError() to check whether GetDataEx() succeeds
        or not before using read data.
    
    
    Args:
        read_data (AnyVariable): The variable in which the data will be stored
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt], optional): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        GetDataEx(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True). Defaults to 1.
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.

[Usage]
`GetDataEx(desti, PLC name, device type, address, data count)`

[Example]
```
char byData[10]
short wData[6], err

GetDataEx(byData[0], "Local HMI", LW, 0, 10)//  read 10 bytes = 5 words
GetDataEx(wData[0], "Local HMI", LW, 0, 6)//  read 6 words
GetDataEx(wData[0], "Local HMI", "Pressure", 6)
//  use user-defined tag - "Pressure" to indicate device type and address.
GetDataEx(wData[0], "MODBUS RTU", 4x, 1, 6)//  read 6 words

GetError(err)//  save a error code to err
if err == 0 then
    //  if err is equal to 0, it is succesful to execute GetDataEx()
    //  and wData[] is valid.
end if
```
    """
    if data_count is None:
        return CALL('GetDataEx', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('GetDataEx', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetError(error:AnyVariable[int]) -> CALL:
    """
[Description]
Description  Gets an error code.
Example
```
macro_command main()
short err
char byData[10]

GetDataEx(byData[0], "MODBUS RTU", 4x, 1, 10)// read 10 bytes

// if err is equal to 0, it is successful to execute GetDataEx()
GetErr(err)// save an error code to err

end macro_command
```
Error code:
0: Normal
1: GetDataEx error
2: SetDataEx error
    """
    return CALL('GetError', error)

def DELAY(delay:AnyInt) -> CALL:
    """
[Description]
This function suspends the execution of the current macro
for at least the specified interval (unit : ms).

[Usage]
`DELAY(delay_tme)`

[Example]
```
DELAY(100)//  delay 100ms
```
    """
    return CALL('DELAY', delay)

def MIN(arr:VariableItem[DT], result:AnyVariable[DT], count:AnyInt = 1) -> CALL:
    """
[Description]
Get the minimum value from array.

[Usage]
`MIN(source[start], result, count)`

[Example]
```
int data[5] = {1, 2, 3, 4, 5}
int result

MIN(data[0], result, 5)
// result = 1

MIN(data[1], result, 3)
// result = 2
```
    """
    return CALL('MIN', arr, result, count)

def MAX(arr:VariableItem[DT], result:AnyVariable[DT], count:AnyInt = 1) -> CALL:
    """
[Description]
Get the maximum value from array.

[Usage]
`MAX(source[start], result, count)`

[Example]
```
int data[5] = {1, 2, 3, 4, 5}
int result

MAX(data[0], result, 5)
// result = 5

MAX(data[1], result, 3)
// result = 4
```
    """
    return CALL('MAX', arr, result, count)


def StringGet(read_data:AnyVariable[int], device_name:str, address:TagAddress, data_count:Optional[AnyInt], dont_format:bool=False) -> CALL:
    """
    Args:
        read_data (AnyVariable): The variable to which the data will be read
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt]): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        StringGet(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True).
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.
    
`StringGet(read_data[start], device_name, device_type, address_offset, data_count)`

Description  Receives data from the device. The String data is stored into read_data[start]~
read_data[start + data_count - 1]. read_data must be a one-dimensional char
array.
Data_count is the number of received characters, it can be either a constant or
a variable.
Device_name is the device name enclosed in the double quotation marks (")
and this name has been defined in the device list of system parameters as
follows (see FATEK KB Series):

Device_type is the device type and encoding method (binary or BCD) of the
device data. For example, if device_type is LW_BIN, it means the register is LW
and the encoding method is binary. If use BIN encoding method, "_BIN" can be
ignored.
If device_type is LW_BCD, it means the register is LW and the encoding method
is BCD.
Address_offset is the address offset in the device.

For example, StringGet(read_data_1[0], "FATEK KB Series", RT, 5, 1) represents
that the address offset is 5.
If address_offset uses the format -"N#AAAAA", N indicates that device's
station number is N. AAAAA represents the address offset. This format is used
while multiple devices or controllers are connected to a single serial port. For
example, StringGet(read_data_1[0], "FATEK KB Series", RT, 2#5, 1) represents
that the device's station number is 2. If StringGet() uses the default station
number defined in the device list as follows, it is not necessary to define station
number in address_offset.

The number of registers actually read from depends on the value of the
number of data_count since that the read_data is restricted to char array.

```
|                   |            | actual number of     |
| type of read_data | data_count | 16-bit register read |
|-------------------+------------+----------------------|
| char (8-bit)      | 1          | 1                    |
| char (8-bit)      | 2          | 1                    |
```

1 WORD register(16-bit) equals to the size of 2 ASCII characters. According to
the above table, reading 2 ASCII characters is actually reading the content of
one 16-bit register.

Example
```
macro_command main()
    char str1[20]


    //    read 10 words from LW-0~LW-9 to the variables str1[0] to str1[19]
    //    since that 1 word can store 2 ASCII characters, reading 20 ASCII
    //    characters is actually reading 10 words of register
    StringGet(str1[0], "Local HMI", LW, 0, 20)
```
end macro_command
    """
    if data_count is None:
        return CALL('StringGet', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('StringGet', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def StringGetEx(read_data:AnyVariable[int], device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """
    Args:
        read_data (AnyVariable): The variable to which the data will be read
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt]): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        StringGetEx(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True).
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.
        
`StringGetEx (read_data[start], device_name, device_type, address_offset, data_count)`

Description  Receives data from the device and continues executing next command even if
there's no response from this device.
Descriptions of read_data, device_name, device_type, address_offset and
data_count are the same as GetData.

Example
```
macro_command main()
    char str1[20]
    short test=0

    // macro will continue executing test = 1 even if the MODBUS device is
    // not responding
    StringGetEx(str1[0], "MODBUS RTU", 4x, 0, 20)
    test = 1

    // macro will not continue executing test = 2 until MODBUS device responds
    StringGet(str1[0], "MODBUS RTU", 4x, 0, 20)
    test = 2

end macro_command
```
    """
    if data_count is None:
        return CALL('StringGetEx', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('StringGetEx', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def StringSet(send_data:AnyString, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """
    Args:
        read_data (AnyVariable): The variable from which the data will be sent
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt]): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        StringSet(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True).
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.
        
`StringSet(send_data[start], device_name, device_type, address_offset, data_count)`

Description  Sends data to the device. Data is defined in send_data[start]~ send_data[start

+ data_count - 1]. send_data must be a one-dimensional char array.
data_count is the number of sent characters, it can be either a constant or a
variable.
device_name is the device name enclosed in the double quotation marks (")
and this name has been defined in the device list of system parameters.
device_type is the device type and encoding method (binary or BCD) of the
device data. For example, if device_type is LW_BIN, it means the register is LW
and the encoding method is binary. If use BIN encoding method, "_BIN" can be
ignored.
If device_type is LW_BCD, it means the register is LW and the encoding method
is BCD.
address_offset is the address offset in the device.
For example, StringSet(read_data_1[0], "FATEK KB Series", RT, 5, 1) represents
that the address offset is 5.
If address_offset uses the format -"N#AAAAA", N indicates that device's
station number is N. AAAAA represents the address offset. This format is used
while multiple devices or controllers are connected to a single serial port. For
example, StringSet(read_data_1[0], "FATEK KB Series", RT, 2#5, 1) represents
that the device's station number is 2. If SetData () uses the default station
number defined in the device list, it is not necessary to define station number
in address_offset.

The number of registers actually sends to depends on the value of the number
of data_count, since that send_data is restricted to char array.

```
|                   |            | actual number of     |
| type of read_data | data_count | 16-bit register read |
|-------------------+------------+----------------------|
| char (8-bit)      | 1          | 1                    |
| char (8-bit)      | 2          | 1                    |
```

1 WORD register(16-bit) equals to the size of 2 ASCII characters. According to
the above table, sending 2 ASCII characters is actually writing to one 16-bit
register. The ASCII characters are stored into the WORD register from low byte
to high byte. While using the ASCII Display object to display the string data
stored in the registers, data_count must be a multiple of 2 in order to display
full string content. For example:

macro_command main()
char src1[10]="abcde"
StringSet(src1[0], "Local HMI", LW, 0, 5)
end macro_command

The ASCII Display object shows:

If data_count is an even number that is greater than or equal to the length of
the string, the content of string can be completely shown:

Example
```
macro_command main()
    char src1[10]="abcde"
    StringSet(src1[0], "Local HMI", LW, 0, 6)
end macro_command
```
```
macro_command main()

    char str1[10]="abcde"

    //    Send 3 words to LW-0~LW-2
    //    Data are being sent until the end of string is reached.
    //    Even though the value of data_count is larger than the length of string
    //    , the function will automatically stop.
    StringSet(str1[0], "Local HMI", LW, 0, 10)

end macro_command
```
    """
    if data_count is None:
        return CALL('StringSet', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('StringSet', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def StringSetEx(send_data:AnyString, device_name:str, address:TagAddress, data_count:Optional[AnyInt] = 1, dont_format:bool=False) -> CALL:
    """
    Args:
        read_data (AnyVariable): The variable from which the data will be sent
        device_name (str): The name of the device (PLC or HMI)
        address (TagAddress): An address for the tag. Can either be the tag name or "device_typ,offset" when dont_format is True
        data_count (Optional[AnyInt]): Number of bytes to read. Set this to None to omit parameter for example in the case of recipes:
        StringSetEx(var, "Local HMI", f"RECIPE, {string_literal('recipe_name.item')}", None, dont_format=True).
        dont_format (bool, optional): When False, will add '"' around address if not present. Defaults to False.
        
`StringSetEx (send_data[start], device_name, device_type, address_offset, data_count)`

Description  Sends data to the device and continues executing next command even if there's
no response from this device.
Descriptions of send_data, device_name, device_type, address_offset and
data_count are the same as StringSet.

Example
```
macro_command main()
    char str1[20]="abcde"
    short test=0

    // macro will continue executing test = 1 even if the MODBUS device is
    // not responding
    StringSetEx(str1[0], "MODBUS RTU", 4x, 0, 20)
    test = 1

    // macro will not continue executing test = 2 until MODBUS device responds
    StringSet(str1[0], "MODBUS RTU", 4x, 0, 20)
    test = 2

end macro_command
```
    """
    if data_count is None:
        return CALL('StringSetEx', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address))
    return CALL('StringSetEx', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def StringCat(source:AnyString, destination:VariableItem[int]) -> EVAL[int]:
    """
[Description]
Append source string to destination string.

[Usage]
```
result = StringCat(source[start], destination[start])
result = StringCat("source", destination[start])
```

[Example]
```
macro_command main()
    char src1[20]="abcdefghij"
    char dest1[20]="1234567890"
    bool success1
    success1= StringCat(src1[0], dest1[0])
    // success1=true, dest1="123456790abcdefghij"

    char dest2 [10]="1234567890"
    bool success2
    success2= StringCat("abcde", dest2 [0])
    // success2=false, dest2 remains the same.

    char src3[20]="abcdefghij"
    char dest3[20]
    bool success3
    success3= StringCat(src3[0], dest3[15])
    // success3=false, dest3 remains the same.
end macro_command
```
    """
    return EVAL("StringCat", source, destination)

def String2Unicode(source:AnyString, destination:VariableItem[int]) -> EVAL[int]:
    """
[Description]
Convert string into a unicode string.

[Usage]
`result = String2Unicode("source", destination[start])`


[Example]
```
char dest[20]
int result

result = String2Unicode("ab\"c\"de", dest[0]) // "result" will be set to 14.
result = String2Unicode("abcdefghijklmno", dest[0]) // "result" will be set to 20.
// "result" will be the length of converted Unicode string.
```
    """
    return EVAL("String2Unicode", source, destination)
    
def StringCompare(string1:AnyString, string2:AnyString) -> EVAL[bool]:
    """
[Description]
Do a case-sensitive comparison of two strings.

[Usage]
```
ret = StringCompare (str1[start], str2[start])
ret = StringCompare ("string1", str2[start])
ret = StringCompare (str1[start], "string2")
ret = StringCompare ("string1", "string2")
```

The two string parameters accept both static string (in the form: "string1") and
char array (in the form: str1[start]).
This function returns a Boolean indicating the result of comparison. If two
strings are identical, it returns true. Otherwise it returns false.
The ret field is optional.

[Example]
```
macro_command main()
    char a1[20]="abcde"
    char b1[20]="ABCDE"
    bool ret1
    ret1= StringCompare(a1[0], b1[0])
    // ret1=false

    char a2[20]="abcde"
    char b2[20]="abcde"
    bool ret2
    ret2= StringCompare(a2[0], b2[0])
    // ret2=true

    char a3 [20]="abcde"
    char b3[20]="abcdefg"

    bool ret3
    ret3= StringCompare(a3[0], b3[0])
    // ret3=false

end macro_command
```
    """
    return EVAL("StringCompare", string1, string2)

def StringCopy(source:AnyString, destination:AnyVariable[int]) -> EVAL[bool]:
    """
[Description]
Copies one string to another. This function copies a static string (which is
enclosed in quotes) or a string that is stored in an array to the destination
buffer.

[Usage]
```
success = StringCopy ("source", destination[start])
or
success = StringCopy (source[start], destination[start])
```

The source string parameter accepts both static string (in the form: "source")
and char array (in the form: source[start]).
destination[start] must be an one-dimensional char array.
This function returns a Boolean indicating whether the process has been
successfully completed. If so, it returns true; otherwise it returns false. If the
length of source string exceeds the max. size of destination buffer, it returns
false and the content of destination remains the same.
The success field is optional.

[Example]
```
macro_command main()
    char src1[5]="abcde"
    char dest1[5]
    bool success1
    success1 = StringCopy(src1[0], dest1[0])
    // success1=true, dest1="abcde"


    char dest2[5]
    bool success2
    success2 = StringCopy("12345", dest2[0])
    // success2=true, dest2="12345"

    char src3[10]="abcdefghij"
    char dest3[5]
    bool success3
    success3 = StringCopy(src3[0], dest3[0])
    // success3=false, dest3 remains the same.

    char src4[10]="abcdefghij"
    char dest4[5]
    bool success4
    success4 = StringCopy(src4[5], dest4[0])
    // success4=true, dest4="fghij"

end macro_command
```
    """
    return EVAL("StringCopy", source, destination)

def StringLength(source:AnyString) -> EVAL[int]:
    """
[Description]
Obtain the length of a string.

[Usage]
```
result = StringLength(source[start])
result = StringLength("source")
```

[Example]
```
char strSrc[7]="AB\"C\"DE" // AB"C"DE
int result

result = StringLength(strSrc[0]) // "result" is equal to 7
result = StringLength("1234\"5678\"90") // "result" is equal to 12
```
    """
    return EVAL("StringLength", source)