from computer.adapter import DryRunComputer
from computer.controller import ComputerController
from computer.policy import ComputerPolicy

def test_disabled_by_default():
    c=ComputerController(DryRunComputer([]),ComputerPolicy())
    try: c.click(10,10)
    except PermissionError: pass
    else: raise AssertionError("computer control must be disabled by default")

def test_dry_run_and_coordinate_boundary():
    actions=[]
    c=ComputerController(DryRunComputer(actions),ComputerPolicy(enabled=True,max_x=100,max_y=100))
    c.click(20,30)
    assert actions==[{"action":"click","x":20,"y":30}]
    try: c.click(101,30)
    except ValueError: pass
    else: raise AssertionError("out-of-bound coordinate accepted")

def test_keyboard_allowlist():
    c=ComputerController(DryRunComputer([]),ComputerPolicy(enabled=True))
    c.press("enter")
    try: c.press("f12")
    except PermissionError: pass
    else: raise AssertionError("unsafe key accepted")

def test_emergency_stop():
    c=ComputerController(DryRunComputer([]),ComputerPolicy(enabled=True))
    c.stop()
    try: c.screenshot()
    except PermissionError: pass
    else: raise AssertionError("emergency stop bypassed")
