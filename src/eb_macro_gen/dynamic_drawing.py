from typing import Dict
from objects import *
from enum import Enum

class Shape(Resource):
    pass

VT = TypeVar('VT', Variable[DT], VariableArray[DT])

class Drawing(Resource):
    def __init__(self, name:str, clear_tag:Tag, attribute_tag:Tag):
        super().__init__(clear_tag, attribute_tag)
        self.name = name
        self.clear_tag = clear_tag
        self.attribute_tag = attribute_tag
        self.shapes:List[Shape] = []
        self.variables:List[AnyVariable] = []
        
    def add_variable(self, var:VT[DT]) -> VT[DT]:
        self.variables.append(var)
        return var
        
    def process(self, macro) -> None:
        super().process(macro)
        
        for shape in self.shapes:
            shape.process(macro)
            
        for var in self.variables:
            var.process(macro)
    