from __future__ import annotations
from typing import Dict
from src.eb_macro_gen.objects import *
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
    
class SHAPE(Resource):
    enabled_var = vbool("p_shape_enabled", False)
    def __init__(self):
        super().__init__()
    
    def draw(self, drawing:DRAWING) -> STATEMENT:...

class DRAWING(Resource):
    def __init__(self, name:str, clear_tag:Tag, attribute_tag:Tag, step_tag:Tag):
        super().__init__(clear_tag, attribute_tag)
        self.name = name
        self.clear_tag = clear_tag
        self.attribute_tag = attribute_tag
        self.step_tag = step_tag
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
    LINE_ID = 0
    def __init__(self, 
                 enable:Union[AnyBool, Tag], 
                 x1:Union[AnyInt, Tag], 
                 y1:Union[AnyInt, Tag], 
                 x2:Union[AnyInt, Tag], 
                 y2:Union[AnyInt, Tag], 
                 arrow_style:Union[ArrowStyle, AnyInt, Tag] = ArrowStyle.NONE,
                 line_style:LineStyle = LineStyle.SOLID,
                 color:Union[AnyInt, Tag] = 0):
        super().__init__()
        self.line_id = LINE.LINE_ID
        LINE.LINE_ID += 1
        self.enable = enable
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.arrow_style = arrow_style
        self.line_style = line_style
        self.color = color
        
    def draw(self, drawing:DRAWING) -> STATEMENT:
        temp_var = vushort("temp_val", 0)
        read_val = lambda v: v.read(temp_var) if isinstance(v, Tag) else temp_var.set(int(v))
        
        task = BLOCK(
            self.enable.read(self.enabled_var) if isinstance(self.enable, Tag) else temp_var.set(self.enable),
            IF(self.enabled_var)(
                *[BLOCK(
                    read_val(line_value),
                    drawing_tag.write(temp_var),
                )
                for drawing_tag, line_value in {
                    Tag("shape", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num}", DataType.U16): ShapeType.LINE,
                    Tag("arrow_style", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+1}", DataType.U16): self.arrow_style,
                    Tag("line_style", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+2}", DataType.U16): self.line_style,
                    Tag("color", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+3}", DataType.U16): self.color,
                    Tag("x1", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+5}", DataType.U16): self.x1,
                    Tag("y1", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+6}", DataType.U16): self.y1,
                    Tag("x2", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+7}", DataType.U16): self.x2,
                    Tag("y2", drawing.attribute_tag.device_name, f"{drawing.attribute_tag.address_register}, {drawing.attribute_tag.address_num+8}", DataType.U16): self.y2,
                }.items()]
            )
        )
        
        return task
        
        