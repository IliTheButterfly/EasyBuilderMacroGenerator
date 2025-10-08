from src.eb_macro_gen.objects import *

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
    macro = Macro("test_some_func", "Test the routine Statement")
    
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
    macro.write(
        SWITCH(1)(
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
        indirect.select(selected_var),
        indirect.read_from_actual(),
        INFO("Indirect value %d", indirect_var),
        indirect.read_from_indirect(),
        indirect.write_to_actual(),
        indirect.write_to_indirect(),
    )
    
    macro.end()
    macro.display()