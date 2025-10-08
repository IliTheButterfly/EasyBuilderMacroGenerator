from __future__ import annotations
from typing import Tuple
from .syntax import *

def ACOS(source:AnyVariable[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
The result is equal to the arcosine of the source.

[Usage]
ACOS(source, result)

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
ADDSUM(source[start], result, count)

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
ASCII2DEC(source[start], result, count)

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
ASCII2DOUBLE(source[start], result, count)

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
ASCII2FLOAT(source[start], result, count)

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
ASCII2HEX(source[start], result, count)

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
ASIN(source, result)

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
ATAN(source, result)

[Example]
```
float source = 1, result

ATAN(source, result)//  result == 45
```
    """
    return CALL('ATAN', source, result)

def AVERAGE(start:VariableItem[DT], result:AnyVariable[DT]) -> CALL:
    """
[Description]
Get the average value from array.

[Usage]
AVERAGE(source[start], result, count)

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
    return CALL('AVERAGE', start, result)

def BCC(start:VariableItem[int], result:AnyVariable[int], count:AnyInt) -> CALL:
    """
[Description]
BCC (Block Check Character) uses XOR (Exclusive OR) to calculate checksum.

[Usage]
BCC(source[start], result, count)

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
BIN2BCD(source, result)

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
```
Beep()

[Example]
Beep()
```
    """
    return CALL('Beep')

def BIN2BCD(source:AnyInt, result:AnyVariable[int]) -> CALL:
    """
[Description]
Convert a binary value to a BCD value.

[Usage]
BIN2BCD(source, result)

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
Buzzer(on_off)//  Turn on the buzzer if on_off is nonzero, otherwise turn off the buzzer.

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

def CEIL(source:AnyFloat) -> EVAL:
    """
[Description]
Get the smallest integral value that is not less than input.

[Usage]
result = CEIL(source)

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
COS(source, result)

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
COT(source, result)

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
CRC(source[start], result, count)

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
CRC16_CCITT(source[start], result, count)

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
CRC16_CCITT_FALSE(source[start], result, count)

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
CRC16_X25(source[start], result, count)

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
CRC16_XMODEM(source[start], result, count)

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
CRC8(source[start], result, count)

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
CSC(source, result)

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
CUBERT(source, result)

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
DATE2DEC(day_offset, date)

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
DEC2ASCII(source, result[start], count)

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
RecipeGetData(destination, recipe address, record ID)

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
result = RecipeQuery("SELECT * FROM ...", destination)
result = RecipeQuery(source[start], destination)

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
RecipeQueryGetData(destination, recipe address, result row no.)

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
RecipeQueryGetRecordID(destination, result row no.)

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
RecipeSetData(source, recipe address, record ID)

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
RecipeTransactionBegin()

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
RecipeTransactionCommit()

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
RecipeTransactionRollback()

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
TRACE("")

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
INFO("")

[Example]
```
int a = 100

INFO(" a = %d", a)
```
    """
    return TRACE("[INFO] " + fmt, *values)

def INFO(fmt:str, *values:AnyValue) -> CALL:
    """
[Description]
Trace the variables and send specified string to the debugger.

[Usage]
INFO("")

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
WARN("")

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
ERROR("")

[Example]
```
int a = 100

ERROR(" a = %d", a)
```
    """
    return TRACE("[ERROR] " + fmt, *values)

def SetData(send_data:AnyVariable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False) -> CALL:
    """
[Description]
Write data to a device and stop script execution if no response from this device.

[Usage]
SetData(desti, PLC name, device type, address, data count)

[Example]
```
char byData[10]
short wData[6]

FILL(byData[0], 0, 10)//  set buffers to a specified value
FILL(wData[0], 0, 6)

SetData(byData[0], "Local HMI", LW, 0, 10)//  send 10 bytes = 5 words
SetData(wData[0], "Local HMI", LW, 0, 6)//  send 6 words
SetData(wData[0], "Local HMI", "Pressure", 6
//  use user-defined tag - "Pressure" to indicate device type and address.
```
    """
    return CALL('SetData', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def SetDataEx(send_data:AnyVariable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False) -> CALL:
    """
[Description]
Write data to a device and continue executing next command
even if no response from this device.

[Usage]
SetDataEx(desti, PLC name, device type, address, data count)

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
    return CALL('SetDataEx', send_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetData(read_data:AnyVariable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False) -> CALL:
    """
[Description]
Read data from a device.

[Usage]
GetData(desti, PLC name, device type, address, data count)

[Example]
```
char byData[10]
short wData[6]

GetData(byData[0], "Local HMI", LW, 0, 10)//  read 10 bytes = 5 words
GetData(wData[0], "Local HMI", LW, 0, 6)//  read 6 words
GetData(wData[0], "Local HMI", "Pressure", 6)
//  use user-defined tag - "Pressure" to indicate device type and address.
```
    """
    return CALL('GetData', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetDataEx(read_data:Variable, device_name:str, address:TagAddress, data_count:AnyInt = 1, dont_format:bool=False) -> CALL:
    """
[Description]
Read data from a device and continue executing next command
even if no response from this device.

Warning : Must use GetError() to check whether GetDataEx() succeeds
        or not before using read data.

[Usage]
GetDataEx(desti, PLC name, device type, address, data count)

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
    return CALL('GetDataEx', read_data, string_literal(device_name), address if dont_format else ensure_string_is_literal(address), data_count)

def GetError(error:AnyVariable[int]) -> CALL:
    """
[Description]
Get a error code.

[Usage]
GetError(err)

[Example]
```
short err
char byData[10]

GetDataEx(byData[0], "MODBUS RTU", 4x, 1, 10)//  read 10 bytes = 5 words

//  Must use GetError() to check whether GetDataEx() succeeds 
//  or not before using byData[].
GetError(err)//  save a error code to err
if err == 0 then
    //  if err is equal to 0, it is succesful to execute GetDataEx()
    //  and byData[] is valid.
end if
```
    """
    return CALL('GetError', error)

def DELAY(delay:AnyInt) -> CALL:
    """
[Description]
This function suspends the execution of the current macro
for at least the specified interval (unit : ms).

[Usage]
DELAY(delay_tme)

[Example]
```
DELAY(100)//  delay 100ms
```
    """
    return CALL('DELAY', delay)

def MIN(arr:VariableItem[DT], result:VariableItem[DT], count:AnyInt = 1) -> CALL:
    """
[Description]
Get the minimum value from array.

[Usage]
MIN(source[start], result, count)

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

def MAX(arr:VariableItem[DT], result:VariableItem[DT], count:AnyInt = 1) -> CALL:
    """
[Description]
Get the maximum value from array.

[Usage]
MAX(source[start], result, count)

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
