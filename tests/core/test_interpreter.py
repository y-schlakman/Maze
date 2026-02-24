import pytest
from maze.core.interpreter import Interpreter


def test_load_source_parsing():
    """Test that the interpreter correctly parses the grid, functions, and finds the start."""
    source = """
    ##,##,##
    ##,^^,## // This is a comment
    ##,AA,##

    AA-> ="Hello" // Function comment
    BB-> -=30
    """

    interpreter = Interpreter()
    interpreter.load_source(source)

    # Check grid structure
    assert len(interpreter.grid) == 3
    assert interpreter.grid[0] == ['##', '##', '##']
    assert interpreter.grid[1] == ['##', '^^', '##']
    assert interpreter.grid[2] == ['##', 'AA', '##']

    # Check functions
    assert len(interpreter.functions) == 2
    assert interpreter.functions['AA'] == '="Hello"'
    assert interpreter.functions['BB'] == '-=30'

    # Check car spawn
    assert len(interpreter.cars) == 1
    car = interpreter.cars[0]
    assert car.row == 1
    assert car.col == 1
    assert car.direction == 'D'


def test_tick_basic_movement_and_death():
    """Test that a car moves, hits a hole, and dies."""
    source = """
    ^^,..,()
    """
    interpreter = Interpreter()
    interpreter.load_source(source)

    car = interpreter.cars[0]
    car.force_direction('R')  # Force it to move right for this test

    assert interpreter.is_running() is True

    interpreter.tick()  # Moves to '..'
    assert car.col == 1
    assert len(interpreter.cars) == 1

    interpreter.tick()  # Moves to '()'
    assert car.col == 2
    assert car.is_alive is False

    # Car gets cleaned up at the end of the tick
    assert len(interpreter.cars) == 0
    assert interpreter.is_running() is False


def test_tick_out_of_bounds_death():
    """Test that a car driving off the map is destroyed."""
    source = """
    ^^
    """
    interpreter = Interpreter()
    interpreter.load_source(source)

    # Car starts facing 'D'. Next tick, it drives off the bottom edge.
    interpreter.tick()

    assert len(interpreter.cars) == 0


def test_tick_printing():
    """Test that the '>>' command returns the car's value."""
    source = """
    ^^,>>
    """
    interpreter = Interpreter()
    interpreter.load_source(source)

    car = interpreter.cars[0]
    car.force_direction('R')
    car.set_value(42)

    outputs = interpreter.tick()  # Car moves to '>>'

    assert len(outputs) == 1
    assert outputs[0] == '42'


def test_tick_splitter():
    """Test that the '<>' command clones the car."""
    source = """
    ^^,<>
    """
    interpreter = Interpreter()
    interpreter.load_source(source)

    interpreter.cars[0].force_direction('R')
    interpreter.tick()  # Car moves to '<>'

    # The original car is still alive, and a new one was added
    assert len(interpreter.cars) == 2
    assert interpreter.cars[0].row == 0 and interpreter.cars[0].col == 1
    assert interpreter.cars[1].row == 0 and interpreter.cars[1].col == 1


def test_tick_wall_replacement():
    """Test that the '--' command turns into a '##' wall."""
    source = """
    ^^,--
    """
    interpreter = Interpreter()
    interpreter.load_source(source)

    interpreter.cars[0].force_direction('R')
    interpreter.tick()  # Car moves to '--'

    assert interpreter.grid[0][1] == '##'