class Car:
    def __init__(self, row: int, col: int, direction: str = 'D', value: int | str = 0):
        """
        Initializes a new Car (thread) at the given position in the maze.

        :param row: The starting row (y-coordinate).
        :param col: The starting column (x-coordinate).
        :param direction: The initial direction ('U', 'D', 'L', 'R'). Defaults to 'D'.
        :param value: The initial value held by the car. Defaults to 0.
        """
        # --- Positional State ---
        self.row = row
        self.col = col
        self.direction = direction

        # --- Memory State ---
        self.value = value

        # --- Execution State ---
        self.pause_ticks = 0  # Number of ticks to wait (for 2-digit numeral commands)
        self.is_alive = True  # Becomes False when hitting a hole '()'

    def move(self):
        """Moves the car one step in its current direction, respecting pause ticks."""
        if not self.is_alive:
            return

        if self.pause_ticks > 0:
            self.pause_ticks -= 1
            return

        if self.direction == 'U':
            self.row -= 1
        elif self.direction == 'D':
            self.row += 1
        elif self.direction == 'L':
            self.col -= 1
        elif self.direction == 'R':
            self.col += 1

    def force_direction(self, new_direction: str):
        """Forces the car to go Left (%L), Right (%R), Down (%D), or Up (%U)."""
        if new_direction in ('U', 'D', 'L', 'R'):
            self.direction = new_direction

    def pause(self, ticks: int):
        """Pauses the car for a given amount of ticks."""
        self.pause_ticks = ticks

    def destroy(self):
        """Kills the car (triggered by the '()' command)."""
        self.is_alive = False

    def clone(self):
        """
        Creates a new thread/car at the current position ('<>' command).
        The new car seamlessly copies the positional and memory state.
        """
        return Car(self.row, self.col, self.direction, self.value)

    # --- Memory/Function Commands ---

    def set_value(self, val: int | str):
        """Assigns a new value to the car (=)."""
        self.value = val

    def add_value(self, val: int):
        """Adds to the car's value (+=)."""
        self.value += val

    def sub_value(self, val: int):
        """Subtracts from the car's value (-=)."""
        self.value -= val

    def mul_value(self, val: int):
        """Multiplies the car's value (*=)."""
        self.value *= val

    def div_value(self, val: int):
        """Divides the car's value (/=)."""
        self.value /= val

    def __repr__(self):
        return f"<Car at ({self.row}, {self.col}) | Dir: {self.direction} | Val: {self.value} | Paused: {self.pause_ticks} | Alive: {self.is_alive}>"