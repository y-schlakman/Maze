import pytest
from maze.core.car import Car


def test_car_initialization():
    """Test that a car initializes with the correct default and custom values."""
    # Default initialization
    car1 = Car(row=0, col=0)
    assert car1.row == 0
    assert car1.col == 0
    assert car1.direction == 'D'
    assert car1.value == 0
    assert car1.is_alive is True
    assert car1.pause_ticks == 0

    # Custom initialization
    car2 = Car(row=5, col=10, direction='R', value="Hello")
    assert car2.direction == 'R'
    assert car2.value == "Hello"


def test_car_movement():
    """Test that the car updates its coordinates correctly based on direction."""
    car = Car(row=5, col=5, direction='D')

    car.move()
    assert car.row == 6 and car.col == 5  # Moved Down

    car.force_direction('R')
    car.move()
    assert car.row == 6 and car.col == 6  # Moved Right

    car.force_direction('U')
    car.move()
    assert car.row == 5 and car.col == 6  # Moved Up

    car.force_direction('L')
    car.move()
    assert car.row == 5 and car.col == 5  # Moved Left back to start


def test_car_pause_logic():
    """Test that pausing prevents movement for the correct number of ticks."""
    car = Car(row=0, col=0, direction='D')
    car.pause(2)

    car.move()
    assert car.row == 0  # Tick 1: paused, did not move
    assert car.pause_ticks == 1

    car.move()
    assert car.row == 0  # Tick 2: paused, did not move
    assert car.pause_ticks == 0

    car.move()
    assert car.row == 1  # Tick 3: no longer paused, moved Down


def test_car_death():
    """Test that a destroyed car cannot move."""
    car = Car(row=0, col=0, direction='D')
    car.destroy()

    assert car.is_alive is False
    car.move()
    assert car.row == 0  # Should not move because it's dead


def test_car_cloning():
    """Test the <> command logic where a car duplicates itself."""
    original = Car(row=3, col=4, direction='L', value=42)
    clone = original.clone()

    # Ensure it's a new object in memory
    assert original is not clone

    # Ensure all states match
    assert clone.row == 3
    assert clone.col == 4
    assert clone.direction == 'L'
    assert clone.value == 42
    assert clone.is_alive is True


def test_car_memory_operations():
    """Test the memory manipulation commands (=, +=, -=, *=, /=)."""
    car = Car(row=0, col=0)

    car.set_value(10)
    assert car.value == 10

    car.add_value(5)
    assert car.value == 15

    car.sub_value(3)
    assert car.value == 12

    car.mul_value(2)
    assert car.value == 24

    car.div_value(4)
    assert car.value == 6.0