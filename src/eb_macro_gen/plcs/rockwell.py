from __future__ import annotations
from hmi_instructions import *

class TON(STATEMENT):
    def __init__(self, timer:TIMER):
        self.timer = timer
        super().__init__(timer)
        self.body = IF(self.timer.EN)(
            IF(~self.timer.TT & ~self.timer.DN)(
                self.timer.ACC.set(0),
                self.timer.TT.set(True),
                self.timer.DN.set(False),
            ),
            IF(~self.timer.DN & self.timer.ACC <= self.timer.PRE)(
                self.timer.ACC.set(self.timer.ACC + 100)
            ).ELSE()(
                self.timer.DN.set(True),
                self.timer.TT.set(False)
            )
        ).ELSE()(
            self.timer.DN.set(False),
            self.timer.ACC.set(0),
            self.timer.TT.set(False),
        )
    
    def bake(self, macro:Macro):
        self.body.bake(macro)
        
    def process(self, macro:Macro):
        self.body.process(macro)

class TIMER(Resource):
    def __init__(self, name:str, plc_name:str):
        self.name = name
        self.plc_name = plc_name
        self.EN = vbool(f'{name}_EN')
        self.TT = vbool(f'{name}_TT')
        self.DN = vbool(f'{name}_DN')
        self.PRE = vint(f'{name}_PRE')
        self.ACC = vint(f'{name}_ACC')
        super().__init__(self.EN, self.TT, self.DN, self.PRE, self.ACC)
        
    def GetData(self, address:str) -> List[STATEMENT]:
        return [
            *[GetData(var, self.plc_name, f'{address}.{suffix}') for var, suffix in {
                self.EN : 'EN',
                self.TT : 'TT',
                self.DN : 'DN',
                self.PRE : 'PRE',
                self.ACC : 'ACC',
            }.items()]
        ]
        
    def SetData(self, address:str) -> List[STATEMENT]:
        return [
            *[SetData(var, self.plc_name, f'{address}.{suffix}') for var, suffix in {
                self.EN : 'EN',
                self.TT : 'TT',
                self.DN : 'DN',
                self.PRE : 'PRE',
                self.ACC : 'ACC',
            }.items()]
        ]
        
    def TON(self) -> TON:
        return TON(self)