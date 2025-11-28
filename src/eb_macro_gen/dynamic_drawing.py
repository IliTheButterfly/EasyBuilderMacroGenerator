from __future__ import annotations
from typing import Dict
from .objects import *
from enum import IntEnum

VT = TypeVar('VT', Variable[DT], VariableArray[DT])

class ShapeType(IntEnum):
    NONE = 0
    LINE = 1
    RECTANGLE = 2
    CIRCLE = 3
    DOT = 4
    ELLIPSE = 5
    ELLIPSE_FROM_RECTANGLE = 6
    ARC = 7
    PIE = 8
    MOVE_ORIGIN = 21
    
class ArrowStyle(IntEnum):
    NONE = 0
    ONE_HOLLOW = 1
    TWO_HOLLOW = 2
    ONE_SOLID = 3
    TWO_SOLID = 4
    SMALL = 0
    LARGE = 10
    LARGE_ONE_HOLLOW = 11
    LARGE_TWO_HOLLOW = 12
    LARGE_ONE_SOLID = 13
    LARGE_TWO_SOLID = 14
    
class LineStyle(IntEnum):
    SOLID = 0
    DASH = 1
    DOT = 2
    DASH_DOT = 3
    DASH_DOT_DOT = 4
    
class ShapeStyle(IntEnum):
    HOLLOW = 0
    SOLID = 1
    
class ShapeOffset(IntEnum):
    SHAPE = 0
    ARROW_STYLE = 1
    SHAPE_STYLE = 1
    LINE_STYLE = 2
    FILL_STYLE = 2
    INNER_COLOR = 3
    INTERIROR_PATTERN_COLOR = 4
    X1 = 5
    Y1 = 6
    X2 = 7
    RADIUS = 7
    RX = 7
    Y2 = 8
    START_DEGREE = 8
    RY = 8
    END_DEGREE = 9

class ShapeParamUnit(IntEnum):
    PIXELS = 0
    PERCENT = 1
    
class ShapeParamType(IntEnum):
    X = 0
    Y = 1

class ShapeParam(Resource):
    temp_float = vfloat("p_drawing_param_float_temp", 0)
    temp_int = vushort("p_drawing_param_int_temp", 0)
    def __init__(self, value:Union[AnyFloat, AnyInt, Tag]):
        super().__init__(value)
        if is_int(value):
            self.unit = ShapeParamUnit.PIXELS
        elif is_float(value):
            self.unit = ShapeParamUnit.PERCENT
        else:
            raise TypeError("value must be either an int, a float, a variable of either int or float or a tag of int or float")
        self._value = value
        
    def read(self, drawing:DRAWING, destination:Union[AnyVariable[int], Tag], param_type:ShapeParamType) -> STATEMENT:
        def as_int(v):
            if isinstance(v, float):
                return int(v)
            return v
        if self.unit == ShapeParamUnit.PIXELS:
            if isinstance(destination, Tag):
                return BLOCK(
                    self._value.read(self.temp_int) if isinstance(self._value, Tag) else self.temp_int.set(self._value),
                    destination.write(self.temp_int),
                )
            else:
                return self._value.read(destination) if isinstance(self._value, Tag) else destination.set(self._value)
        else:
            max_val = drawing.width if param_type == ShapeParamType.X else drawing.height
            if isinstance(destination, Tag):
                if isinstance(self._value, Tag):
                    if isinstance(max_val, Tag):
                        return BLOCK(
                            COMMENT("Read max val"),
                            max_val.read(self.temp_int),
                            COMMENT("Read value"),
                            self._value.read(self.temp_float),
                            COMMENT("Calculate pixels"),
                            self.temp_int.set(as_int(self.temp_float * self.temp_int)),
                            COMMENT("Write pixels"),
                            destination.write(self.temp_int),
                        )
                    else:
                        return BLOCK(
                            COMMENT("Read value"),
                            self._value.read(self.temp_float),
                            COMMENT("Calculate pixels"),
                            self.temp_int.set(as_int(self.temp_float * max_val)),
                            COMMENT("Write pixels"),
                            destination.write(self.temp_int),
                        )
                else:
                    if isinstance(max_val, Tag):
                        return BLOCK(
                            COMMENT("Read max val"),
                            max_val.read(self.temp_int),
                            COMMENT("Calculate pixels"),
                            self.temp_int.set(as_int(self._value * self.temp_int)),
                            COMMENT("Write pixels"),
                            destination.write(self.temp_int),
                        )
                    else:
                        return BLOCK(
                            COMMENT("Calculate pixels"),
                            self.temp_int.set(as_int(self._value * max_val)),
                            COMMENT("Write pixels"),
                            destination.write(self.temp_int),
                        )
            else:
                if isinstance(self._value, Tag):
                    if isinstance(max_val, Tag):
                        return BLOCK(
                            COMMENT("Read max val"),
                            max_val.read(self.temp_int),
                            COMMENT("Read value"),
                            self._value.read(self.temp_float),
                            COMMENT("Calculate pixels"),
                            destination.set(as_int(self.temp_float * self.temp_int)),
                        )
                    else:
                        return BLOCK(
                            COMMENT("Read value"),
                            self._value.read(self.temp_float),
                            COMMENT("Calculate pixels"),
                            destination.set(as_int(self.temp_float * max_val)),
                        )
                else:
                    if isinstance(max_val, Tag):
                        return BLOCK(
                            COMMENT("Read max val"),
                            max_val.read(self.temp_int),
                            COMMENT("Calculate pixels"),
                            destination.set(as_int(self._value * self.temp_int)),
                        )
                    else:
                        return BLOCK(
                            COMMENT("Calculate pixels"),
                            destination.set(as_int(self._value * max_val)),
                        )
        
class SHAPE(Resource):
    enabled_var = vbool("p_shape_enabled", False)
    temp_var = vushort("p_shape_temp", 0)
    def __init__(self):
        super().__init__()
    
    def draw(self, drawing:DRAWING) -> STATEMENT:...
    
    def _read_val(self, v:Union[Tag, AnyInt]) -> STATEMENT:
        return v.read(self.temp_var) if isinstance(v, Tag) else self.temp_var.set(v)
    
    def set_param(self, drawing:DRAWING, offset:ShapeOffset, value:Union[Tag, AnyInt, ShapeParam]) -> STATEMENT:
        drawing_tag = Tag(offset.name, drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num + offset}", DataType.U16)
        offset_name = '/'.join(item[0] for item in filter(lambda v : v[1].value == offset.value, ShapeOffset._member_map_.items()))
        if isinstance(value, ShapeParam):
            return BLOCK(
                COMMENT(offset_name),
                value.read(drawing, drawing_tag, ShapeParamType.X if 'X' in offset_name else ShapeParamType.Y),
            )
        if isinstance(value, Tag):
            return BLOCK(
                COMMENT(offset_name),
                value.read(self.temp_var),
                drawing_tag.write(self.temp_var),
            )
        if isinstance(value, (Variable, VariableItem)):
            return BLOCK(
                COMMENT(offset_name),
                drawing_tag.write(value)
            )
        return BLOCK(
            COMMENT(offset_name),
            self.temp_var.set(value),
            drawing_tag.write(self.temp_var),
        )
        
class DRAWING(Resource):
    def __init__(self, name:str, clear_tag:Tag, attribute_tag:Tag, step_tag:Tag, width:Union[Tag, AnyInt], height:Union[Tag, AnyInt]):
        super().__init__(clear_tag, attribute_tag)
        self.name = name
        self.clear_tag = clear_tag
        self.attribute_tag = attribute_tag
        self.step_tag = step_tag
        self.width = width
        self.height = height
        self.shapes:List[SHAPE] = []
        self._routine:Optional[ASYNC_SCHEDULER] = None
        
    @property
    def routine(self) -> ASYNC_ROUTINE:
        self._routine = ASYNC_ROUTINE(self.name, self.step_tag, 200, [
            BLOCK(
                COMMENT("Clear drawing"),
                self.clear_tag.write(ON),
            ),
            *[shape.draw(self) for shape in self.shapes],
        ])
        return self._routine
        
    def process(self, macro) -> None:
        super().process(macro)
        
        for shape in self.shapes:
            shape.process(macro)
            
    def add(self, shape:SHAPE):
        self.shapes.append(shape)
            
class LINE(SHAPE):
    def __init__(self, 
                 enable:Union[AnyBool, Tag], 
                 x1:Union[AnyInt, AnyFloat, Tag], 
                 y1:Union[AnyInt, AnyFloat, Tag], 
                 x2:Union[AnyInt, AnyFloat, Tag], 
                 y2:Union[AnyInt, AnyFloat, Tag], 
                 arrow_style:Union[ArrowStyle, AnyInt, Tag] = ArrowStyle.NONE,
                 line_style:LineStyle = LineStyle.SOLID,
                 color:Union[AnyInt, Tag] = 0):
        super().__init__()
        self.enable = enable
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.arrow_style = arrow_style
        self.line_style = line_style
        self.color = color
        
    def draw(self, drawing:DRAWING) -> STATEMENT:
        block = BLOCK(
            self.set_param(drawing, ShapeOffset.SHAPE, ShapeType.LINE),
            self.set_param(drawing, ShapeOffset.ARROW_STYLE, self.arrow_style),
            self.set_param(drawing, ShapeOffset.LINE_STYLE, self.line_style),
            self.set_param(drawing, ShapeOffset.INNER_COLOR, self.color),
            self.set_param(drawing, ShapeOffset.X1, ShapeParam(self.x1)),
            self.set_param(drawing, ShapeOffset.Y1, ShapeParam(self.y1)),
            self.set_param(drawing, ShapeOffset.X2, ShapeParam(self.x2)),
            self.set_param(drawing, ShapeOffset.Y2, ShapeParam(self.y2)),
        )
        if isinstance(self.enable, (bool, int)):
            # Optimize if enable is a constant
            if self.enable:
                return block
            else:
                return BLOCK()
        else:
            return BLOCK(
                self.enable.read(self.enabled_var) if isinstance(self.enable, Tag) else self.enabled_var.set(self.enable),
                IF(self.enabled_var)(
                    block
                )
            )
        

class CIRCLE(SHAPE):
    def __init__(self,
                 enable:Union[AnyBool, Tag], 
                 x:Union[AnyInt, AnyFloat, Tag], 
                 y:Union[AnyInt, AnyFloat, Tag], 
                 r:Union[AnyInt, Tag],
                 shape_style:Union[ShapeStyle, AnyInt, Tag] = ShapeStyle.HOLLOW,
                 inner_color:Union[AnyInt, Tag] = 0,
                 fill_style:Union[AnyInt, Tag] = 0,
                 interior_pattern_color:Union[AnyInt, Tag] = 0):
        super().__init__()
        self.enable = enable
        self.x = x
        self.y = y
        self.r = r
        self.shape_style = shape_style
        self.inner_color = inner_color
        self.fill_style = fill_style
        self.interior_pattern_color = interior_pattern_color
    
    def draw(self, drawing):
        block = BLOCK(
            self.set_param(drawing, ShapeOffset.SHAPE, ShapeType.CIRCLE),
            self.set_param(drawing, ShapeOffset.SHAPE_STYLE, self.shape_style),
            self.set_param(drawing, ShapeOffset.FILL_STYLE, self.fill_style),
            self.set_param(drawing, ShapeOffset.INNER_COLOR, self.inner_color),
            self.set_param(drawing, ShapeOffset.INTERIROR_PATTERN_COLOR, self.interior_pattern_color),
            self.set_param(drawing, ShapeOffset.X1, ShapeParam(self.x)),
            self.set_param(drawing, ShapeOffset.Y1, ShapeParam(self.y)),
            self.set_param(drawing, ShapeOffset.RADIUS, self.r),
        )
        if isinstance(self.enable, (bool, int)):
            # Optimize if enable is a constant
            if self.enable:
                return block
            else:
                return BLOCK()
        else:
            return BLOCK(
                self.enable.read(self.enabled_var) if isinstance(self.enable, Tag) else self.enabled_var.set(self.enable),
                IF(self.enabled_var)(
                    block
                )
            )
        
        
        