from __future__ import annotations
from typing import Dict
from src.eb_macro_gen.instructions import *

class DataType(Enum):
    Bit = 0
    Undesignated = 1
    BCD16 = 2
    BCD32 = 3
    U16 = 4
    S16 = 5
    U32 = 6
    S32 = 7
    U64 = 8
    S64 = 9
    F32 = 10
    F64 = 11
    
class Tag(Resource):
    def __init__(self, name:str, device_name:str, address:str, dtype:DataType):
        super().__init__()
        self.name = name
        self.device_name = device_name
        self.address = address
        self.dtype = dtype
        
    def read(self, result:AnyVariable, count:AnyInt = 1) -> STATEMENT:
        # TODO Add type verification
        if isinstance(count, int) and count != 1 and isinstance(result, Variable):
            raise TypeError(f"Cannot read multiple values into non-array variable {result}")
        res = GetData(result, self.device_name, self.address, count, dont_format=True)
        res.resources.add(self)
        return res
    
    def write(self, var: AnyVariable, count:AnyInt = 1) -> STATEMENT:
        # TODO Add type verification
        if isinstance(count, int) and count != 1 and isinstance(var, Variable):
            raise TypeError(f"Cannot write multiple values from non-array variable {var}")
        res = SetData(var, self.device_name, self.address, count, True)
        res.resources.add(self)
        return res
    
    @property
    def address_num(self) -> Optional[int]:
        try:
            return int(self.address.split(',')[1])
        except:
            return None
        
    @property
    def address_register(self) -> str:
        try:
            return self.address.split(',')[0]
        except:
            return None
    
    def __hash__(self) -> int:
        return hash(f"{self.device_name}/{self.address}")
    
class ROUTINE(BLOCK):
    def __init__(self, name:str, step_tag:Tag, steps:List[STATEMENT]):
        super().__init__()
        self.step_tag = step_tag
        self.step_var = Variable(f"{name}_step", "short", 0)
        self.statements.extend([
            COMMENT(f"---------- START ROUTINE {name} ----------"),
            COMMENT("Get current step"),
            self.step_tag.read(self.step_var),
            EMPTY(),
        ])
        
        statement = None
        for i, step in enumerate(steps):
            if i == 0:
                statement = IF(self.step_var == 0)(
                    COMMENT("Step 0"),
                    step
                )
                continue
            
            statement = statement.ELIF(self.step_var == i)(
                COMMENT(f"Step {i}"),
                step
            )
        self.statements.append(statement)
        
        self.statements.extend([
            EMPTY(),
            COMMENT("Increment step"),
            self.step_var.set(self.step_var + 1),
            EMPTY(),
            IF(self.step_var >= len(steps))(
                COMMENT("Reset"),
                self.step_var.set(0),
            ),
            EMPTY(),
            COMMENT("Writing step"),
            self.step_tag.write(self.step_var),
            EMPTY(),
            COMMENT(f"---------- END ROUTINE {name} ----------"),
            EMPTY(),
        ])
        
class ASYNC_ROUTINE(BLOCK):
    def __init__(self, name:str, step_tag:Tag, delay:AnyInt, steps:List[STATEMENT]):
        super().__init__()
        self.name = name
        self.step_tag = step_tag
        self.delay = delay
        self.step_var = Variable(f"{name}_step", "short", 0)
        self.statements.extend([
            COMMENT(f"---------- START ROUTINE {name} ----------"),
            COMMENT("Get current step"),
            self.step_tag.read(self.step_var),
            EMPTY(),
        ])
        
        statement = None
        for i, step in enumerate(steps):
            if i == 0:
                statement = IF(self.step_var == 0)(
                    COMMENT("Step 0"),
                    step
                )
                continue
            
            statement = statement.ELIF(self.step_var == i)(
                COMMENT(f"Step {i}"),
                step
            )
        self.statements.append(statement)
        
        self.statements.extend([
            EMPTY(),
            COMMENT("Increment step"),
            self.step_var.set(self.step_var + 1),
            EMPTY(),
            IF(self.step_var < len(steps))(
                self.step_tag.write(self.step_var),
                ASYNC_TRIG_MACRO(f"{name}_loop"),
            ).ELSE()(
                COMMENT("Reset"),
                self.step_var.set(0),
                self.step_tag.write(self.step_var),
            ),
            EMPTY(),
            COMMENT(f"---------- END ROUTINE {name} ----------"),
            EMPTY(),
            
        ])
        
    def loop_macro(self, macro_name:str) -> Macro:
        loop_macro = Macro(f"{self.name}_loop", f"Loop for the {self.name} async routine")
        with loop_macro as macro:
            macro.write(
                COMMENT("Call original macro"),
                DELAY(self.delay),
                ASYNC_TRIG_MACRO(macro_name),
            )
        return loop_macro

        
ON = vbool("on", True)
OFF = vbool("off", False)

class TASK(STATEMENT):
    def __init__(self, name:str, command_tag:Tag, body:STATEMENT):
        super().__init__(command_tag, body)
        self.name = name
        self.command_tag = command_tag
        self.command_var = vbool("p_task_cmd", False)
        self.body = BLOCK(
            COMMENT(f"========== START TASK {name} =========="),
            self.command_tag.read(self.command_var),
            IF(self.command_var)(
                body,
                EMPTY(),
                COMMENT("Done"),
                self.disable(),
                SCHEDULER.done_var.set(True),
            ),
            COMMENT(f"========== END TASK {name} =========="),
        )
        self.resources.add(self.body)
    
    def bake(self, macro:Macro):
        self.body.bake(macro)
    
    def enable(self) -> STATEMENT:
        return self.command_tag.write(ON)
        
    def disable(self) -> STATEMENT:
        return self.command_tag.write(OFF)
    
class SCHEDULER(STATEMENT):
    done_var = vbool("p_scheduler_done", False)
    def __init__(self, *tasks:TASK):
        super().__init__(*tasks)
        self.tasks:Dict[str, TASK] = {task.name : task for task in tasks}
        
        self.body = BLOCK(
            COMMENT("********** START SCHEDULER **********"),
            *[BLOCK(
                IF(~self.done_var)(
                    task,
                ),
            ) for task in self.tasks.values()],
            COMMENT("********** END SCHEDULER **********"),
        )
        self.resources.add(self.body)
        
    def bake(self, macro:Macro):
        self.body.bake(macro)
        
class ASYNC_SCHEDULER(STATEMENT):
    done_var = vbool("p_scheduler_done", False)
    def __init__(self, name:str, delay:AnyInt, *tasks:TASK):
        super().__init__(*tasks)
        self.name = name
        self.delay = delay
        self.tasks:Dict[str, TASK] = {task.name : task for task in tasks}
        
        self.body = BLOCK(
            COMMENT(f"********** START SCHEDULER {self.name} **********"),
            *[BLOCK(
                IF(~self.done_var)(
                    task,
                ),
            ) for task in self.tasks.values()],
            ASYNC_TRIG_MACRO(f"{self.name}_loop"),
            COMMENT(f"********** END SCHEDULER {self.name} **********"),
        )
        self.resources.add(self.body)
        
    def bake(self, macro:Macro):
        self.body.bake(macro)
        
    def loop_macro(self, macro_name:str) -> Macro:
        loop_macro = Macro(f"{self.name}_loop", f"Loop for the {self.name} scheduler")
        with loop_macro as macro:
            macro.write(
                COMMENT("Call original macro"),
                DELAY(self.delay),
                ASYNC_TRIG_MACRO(macro_name),
            )
        return loop_macro
    
class INDIRECT_TAG(Resource):
    def __init__(self, indirect_tag:Tag, indirect_var:AnyVariable, actual_tags:List[Tag]):
        super().__init__(indirect_tag, indirect_var, *actual_tags)
        self.indirect_tag = indirect_tag
        self.actual_tags = actual_tags
        self.indirect_var = indirect_var
        self.selected_var = vint(f"{indirect_tag.name}_selection", 0)
        
    def select(self, index:AnyInt) -> STATEMENT:
        return self.selected_var.set(index)
    
    # TODO Find better names
    def read_from_indirect(self) -> STATEMENT:
        return self.indirect_tag.read(self.indirect_var)
    
    def write_to_indirect(self) -> STATEMENT:
        return self.indirect_tag.write(self.indirect_var)
    
    def read_from_actual(self) -> STATEMENT:
        return BLOCK(
            COMMENT(f"Reading indirect tag {self.indirect_tag.name} from actual"),
            SWITCH(self.selected_var)(
                *[CASE(i)(tag.read(self.indirect_var)) for i, tag in enumerate(self.actual_tags)]
            )
        )
    
    def write_to_actual(self) -> STATEMENT:
        return BLOCK(
            COMMENT(f"Writing indirect tag {self.indirect_tag.name} to actual"),
            SWITCH(self.selected_var)(
                *[CASE(i)(tag.write(self.indirect_var)) for i, tag in enumerate(self.actual_tags)]
            )
        )
        