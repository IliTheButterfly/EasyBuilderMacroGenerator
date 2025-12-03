from src.eb_macro_gen.objects import *
from src.eb_macro_gen.dynamic_drawing import *

def test_routine():
    macro = Macro("test_routine", "Test the routine Statement")
    
    macro.begin()
    step_tag = Tag("MyTag", "Local HMI", "LW, 10", DataType.S16)
    
    macro.write(
        ROUTINE("my_routine", step_tag, [
            BLOCK(
                COMMENT("A step"),
            ),
            BLOCK(
                COMMENT("Another step"),
            ),
        ])
    )
    macro.end()
    macro.display()
    
def test_some_func():
    macro = Macro("test_some_func", "Test a simple start/stop logic")
    
    macro.begin()
    motor_tag = Tag("motor_tag", "Local HMI", "LB, 7000", DataType.Bit)
    start_tag = Tag("start_tag", "Local HMI", "LB, 7001", DataType.Bit)
    stop_tag = Tag("stop_tag", "Local HMI", "LB, 7002", DataType.Bit)
    latch_tag = Tag("latch_tag", "Local HMI", "LB, 7003", DataType.Bit)
    
    motor_var = vbool("motor_var", 0)
    start_var = vbool("start_var", 0)
    stop_var = vbool("stop_var", 0)
    latch_var = vbool("latch_var", 0)
    
    macro.write(
        start_tag.read(start_var),
        stop_tag.read(stop_var),
        latch_tag.read(latch_var),
        IF(start_var == 1)(
            latch_var.set(1),
        ),
        IF(stop_var == 1)(
            latch_var.set(0),
        ),
        EMPTY(),
        motor_var.set(latch_var),
        motor_tag.write(motor_var),
        latch_tag.write(latch_var),
    )
    macro.end()
    macro.display()
    
def test_elif():
    macro = Macro("test_elif", "Test the elif Statement")
    
    macro.begin()
    macro.write(
        IF(1)(
            COMMENT("Hi"),
        ).ELIF(1)(
            COMMENT("Hello"),
        ).ELIF(1)(
            COMMENT("Yo"),
        ).ELSE()(
            COMMENT("Bye"),
        ),
    )
    
    macro.end()
    macro.display()


def test_cases():
    macro = Macro("test_cases", "Test the SWITCH Statement")
    
    macro.begin()
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
    
    macro.end()
    macro.display()
    
def test_indirect_tag():
    macro = Macro("test_elif", "Test the elif Statement")
    
    macro.begin()
    
    local_tag = Tag("local_tag", "Local HMI", "LW, 10", DataType.S16)
    
    actual_tags = [
        Tag(f"actual_tag{i}", "Local HMI", f"LW, {i+20}", DataType.S16) for i in range(10)
    ]
    
    selected_tag = Tag("selected", "Local HMI", "LW, 11", DataType.U16)
    selected_var = vushort("selected", 0)
    
    indirect_var = vshort("indirect_var", 0)
    indirect = INDIRECT_TAG(local_tag, indirect_var, actual_tags)
    
    macro.write(
        selected_tag.read(selected_var),
        selected_var.set(5),
        indirect.select(selected_var),
        indirect.read_from_actual(),
        INFO("Indirect value %d", indirect_var),
        indirect.read_from_indirect(),
        indirect.write_to_actual(),
        indirect.write_to_indirect(),
    )
    
    macro.end()
    macro.display()
    
def test_scheduler():
    macro = Macro("test_scheduler", "Test the scheduler object")
    
    macro.begin()
    task1_tag = Tag("task1_tag", "Local HMI", "LB, 10", DataType.Bit)
    task2_tag = Tag("task2_tag", "Local HMI", "LB, 11", DataType.Bit)
    
    macro.write(
        SCHEDULER(
            TASK("task1", task1_tag,
                INFO("Task1"),
            ),
            TASK("task2", task2_tag,
                INFO("Task2"),
            ),
        )
    )
    macro.end()
    macro.display()

def test_async_scheduler():
    macro = Macro("test_async_scheduler", "Test the async scheduler object")
    
    macro.begin()
    task1_tag = Tag("task1_tag", "Local HMI", "LB, 10", DataType.Bit)
    task2_tag = Tag("task2_tag", "Local HMI", "LB, 11", DataType.Bit)
    
    scheduler = ASYNC_SCHEDULER("test_async_scheduler", 50,
        TASK("task1", task1_tag,
            INFO("Task1"),
        ),
        TASK("task2", task2_tag,
            INFO("Task2"),
        ),
    )
    
    macro.write(
        scheduler,
    )
    macro.end()
    macro.display()
    
    scheduler.loop_macro(macro.name).display()
    
def test_async_routine():
    # Drawing macro
    routine_macro = Macro("async_task", "Async task")
    
    routine_macro.begin()
    
    step_tag = Tag("step_tag", "Local HMI", "LW, 40", DataType.U16)
    
    temp_var = vushort("temp_var", 0)
    
    # Drawing tags
    reset_tag = Tag("reset", "Local HMI", "LB, 40", DataType.Bit)
    shape_tag = Tag("shape", "Local HMI", "LW, 50", DataType.U16)
    x1_tag = Tag("x1", "Local HMI", "LW, 55", DataType.U16)
    y1_tag = Tag("y1", "Local HMI", "LW, 56", DataType.U16)
    x2_tag = Tag("x2", "Local HMI", "LW, 57", DataType.U16)
    y2_tag = Tag("y2", "Local HMI", "LW, 58", DataType.U16)
    
    routine = ASYNC_ROUTINE("async_task", step_tag, 100, [
        BLOCK(
            COMMENT("Clear"),
            reset_tag.write(ON),
        ),
        BLOCK(
            COMMENT("First line"),
            COMMENT("1 = line"),
            temp_var.set(1),
            shape_tag.write(temp_var),
            EMPTY(),
            
            COMMENT("Positions"),
            *[BLOCK(
                COMMENT(f"Set {tag.name}"),
                temp_var.set(value),
                tag.write(temp_var),
            )
            for tag, value in { x1_tag:15, y1_tag:10, x2_tag:30, y2_tag:35 }.items()]
        ),
        BLOCK(
            COMMENT("Second line"),
            COMMENT("1 = line"),
            temp_var.set(1),
            shape_tag.write(temp_var),
            EMPTY(),
            
            COMMENT("Positions"),
            *[BLOCK(
                COMMENT(f"Set {tag.name}"),
                temp_var.set(value),
                tag.write(temp_var),
            )
            for tag, value in { x1_tag:10, y1_tag:5, x2_tag:30, y2_tag:35 }.items()]
        ),
    ])
    
    routine_macro.write(
        routine
    )
    
    routine_macro.end()
    routine_macro.display()
    
    routine.loop_macro(routine_macro.name).display()

def test_recursive_task():
    macro1 = Macro("recursive_macro1")
    macro2 = Macro("recursive_macro2")
    
    macro1.begin()
    count_tag = Tag("count", "Local HMI", "LW, 100", DataType.U16)
    temp_var = vushort("temp", 0)
    
    macro1.write(
        DELAY(1000),
        count_tag.read(temp_var),
        temp_var.set(temp_var + 1),
        count_tag.write(temp_var),
        SYNC_TRIG_MACRO(macro2.name),
    )
    macro1.end()
    macro1.display()
    
    
    
    macro2.begin()
    
    macro2.write(
        DELAY(1000),
        count_tag.read(temp_var),
        temp_var.set(temp_var + 1),
        count_tag.write(temp_var),
        SYNC_TRIG_MACRO(macro1.name),
    )
    macro2.end()
    macro2.display()
    
def test_c_ifs():
    macro = Macro("test_c_ifs")
    
    with macro:
        var1 = vint("var1")

        for i in range(10):
            if i == 0:
                macro.write(
                    C_IF(var1 == i),
                )
            else:
                macro.write(
                    C_ELIF(var1 == i),
                )
            macro.write(
                COMMENT(f"Case {i}"),
            )
        macro.write(
            C_ELSE(),
            COMMENT("Case Else"),
            C_END_IF(),
        )
    macro.display()
    
def test_drawing():
    macro = Macro("test_drawing")
    
    
    with macro:
        reset_tag = Tag("reset", "Local HMI", "LB, 40", DataType.Bit)
        shape_tag = Tag("shape", "Local HMI", "LW, 50", DataType.U16)
        step_tag = Tag("step", "Local HMI", "LW, 49", DataType.U16)
        
        line1_enable_tag = Tag("line1_en", "Local HMI", "LB, 41", DataType.Bit)
        line1_x1_tag = Tag("line1_x1", "Local HMI", "LW, 150", DataType.U16)
        line2_x1_tag = Tag("line1_x1", "Local HMI", "LW, 152", DataType.F32)
        
        drawing = DRAWING("my_drawing", reset_tag, shape_tag, step_tag, 310, 260)
        drawing.add(LINE(line1_enable_tag, line1_x1_tag, 10, 10, 50, ArrowStyle.LARGE_TWO_SOLID, LineStyle.DASH, 0))
        drawing.add(LINE(True, line2_x1_tag, 5, 0.5, 50, ArrowStyle.ONE_HOLLOW, LineStyle.DASH_DOT_DOT, 6))
        drawing.add(CIRCLE(True, line1_x1_tag, 10, 10, ShapeStyle.SOLID, 6, 3, 2))
        macro.write(
            drawing.routine,
        )
        
        drawing.routine.loop_macro(macro.name).display()
    
    macro.display()

def test_create_tags():
    macro = Macro("heat_cool_states", "Converts the heating and cooling conditions into a word")
    
    PLC_NAME = "KOYO CLICK (Ethernet)"
    LOCAL_HMI = "Local HMI"
    
    with macro:
        steam_in = vbool("steam_in", False)
        steam_out = vbool("steam_out", False)
        cool_in = vbool("cool_in", False)
        cool_out = vbool("cool_out", False)
        steam_present = vbool("steam_present", False)
        water_present = vbool("water_present", False)
        jacket_state = vint("jacket_state", 0)
        for i in range(1, 4):
            steam_in_tag = Tag(f"F33_J{i}_steam_in", PLC_NAME, string_literal(f"F33_J{i}_steam_in"), DataType.Bit)
            steam_out_tag = Tag(f"F33_J{i}_steam_out", PLC_NAME, string_literal(f"F33_J{i}_steam_out"), DataType.Bit)
            cool_in_tag = Tag(f"F33_J{i}_cool_in", PLC_NAME, string_literal(f"F33_J{i}_cool_in"), DataType.Bit)
            cool_out_tag = Tag(f"F33_J{i}_cool_out", PLC_NAME, string_literal(f"F33_J{i}_cool_out"), DataType.Bit)
            steam_present_tag = Tag(f"F33_J{i}_steam_present", PLC_NAME, string_literal(f"F33_J{i}_steam_present"), DataType.Bit)
            water_present_tag = Tag(f"F33_J{i}_water_present", PLC_NAME, string_literal(f"F33_J{i}_water_present"), DataType.Bit)
            jacket_state_tag = Tag(f"F33_J{i}_state", LOCAL_HMI, string_literal(f"F33_J{i}_state"), DataType.Bit)
            
            macro.write(
                COMMENT(f"Jacket {i}"),
                COMMENT("Read tags"),
                steam_in_tag.read(steam_in),
                steam_out_tag.read(steam_out),
                cool_in_tag.read(cool_in),
                cool_out_tag.read(cool_out),
                steam_present_tag.read(steam_present),
                water_present_tag.read(water_present),
                EMPTY(),
                COMMENT("0: Empty, 1: Steam present, 2: Heating, 3: Water present, 4: Cooling"),
                jacket_state.set(0),
                IF(steam_in & steam_out)(
                    jacket_state.set(2),
                ).ELIF(steam_present)(
                    jacket_state.set(1),
                ).ELIF(cool_in & cool_out)(
                    jacket_state.set(4),
                ).ELIF(water_present)(
                    jacket_state.set(3),
                ),
                EMPTY(),
                COMMENT("Write tag"),
                jacket_state_tag.write(jacket_state),
            )
    macro.display()