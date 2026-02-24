import re
from typing import List, Dict, Optional
from maze.core.car import Car

class Interpreter:
    def __init__(self):
        self.grid: List[List[str]] = []
        self.functions: Dict[str, str] = {}
        self.cars: List[Car] = []
        self.waiting_for_input = False
        self.input_target_car: Optional[Car] = None

    @property
    def is_signal_active(self) -> bool:
        for car in self.cars:
            if car.is_alive:
                if self._get_cell(car.row, car.col) == '**':
                    return True
        return False

    def load_source(self, source_code: str):
        self.grid = []
        self.functions = {}
        self.cars = []
        lines = source_code.strip().split('\n')
        temp_grid = []
        for line in lines:
            if '//' in line: line = line.split('//')[0]
            line = line.strip()
            if not line: continue
            if '->' in line:
                parts = line.split('->', 1)
                if len(parts) == 2:
                    self.functions[parts[0].strip()] = parts[1].strip()
            else:
                temp_grid.append([cell.strip() for cell in line.split(',')])

        if temp_grid:
            max_cols = max(len(row) for row in temp_grid)
            self.grid = [row + ['##'] * (max_cols - len(row)) for row in temp_grid]

        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == '^^': self.cars.append(Car(r, c, 'D'))

    def set_input_value(self, value):
        """Called by the UI to resume the simulation."""
        if self.input_target_car:
            self.input_target_car.value = self._parse_value(str(value))
            self.waiting_for_input = False
            self.input_target_car = None

    def tick(self) -> List[str]:
        if self.waiting_for_input:
            return []

        outputs = []
        new_cars = []
        moved_status = {}

        for car in self.cars:
            c_id = id(car)
            moved_status[c_id] = False
            if not car.is_alive or car.pause_ticks > 0:
                if car.pause_ticks > 0: car.pause_ticks -= 1
                continue
            if not self._can_move_to(car.row, car.col, car.direction):
                self._resolve_collision(car)
            car.move()
            moved_status[c_id] = True

        for car in self.cars:
            c_id = id(car)
            if not car.is_alive or car.pause_ticks > 0: continue
            cell = self._get_cell(car.row, car.col)
            if cell is None or cell == '##':
                car.destroy()
                continue
            out = self._execute_cell(car, cell, new_cars, moved_status.get(c_id, False))
            if out is not None:
                outputs.append(str(out))

        self.cars.extend(new_cars)
        self.cars = [c for c in self.cars if c.is_alive]
        return outputs

    def _execute_cell(self, car, cell, new_cars, moved) -> Optional[str]:
        if cell == '()': car.destroy()
        elif cell == '>>': return car.value
        elif cell == '<<':
            self.waiting_for_input = True
            self.input_target_car = car
        elif cell == '<>':
            clone = car.clone()
            self._set_valid_direction(car, 'L')
            self._set_valid_direction(clone, 'R')
            new_cars.append(clone)
        elif cell == '--': self.grid[car.row][car.col] = '##'
        elif cell in ('%L', '%R', '%U', '%D'): car.force_direction(cell[1])
        elif cell.isdigit() and len(cell) == 2:
            if moved: car.pause(int(cell))
        elif len(cell) == 2 and cell.isalpha(): self._execute_function(car, cell)
        return None

    def _execute_function(self, car, func_name):
        cmd = self.functions.get(func_name)
        if cmd: self._run_command_string(car, cmd)

    def _run_command_string(self, car, cmd):
        cmd = cmd.strip()
        if cmd.startswith("IF"):
            m = re.match(r"IF\s+(.+?)\s+THEN\s+(.+?)\s+ELSE\s+(.+)", cmd)
            if m:
                cond, t, e = m.groups()
                if self._evaluate_condition(car, cond): self._run_command_string(car, t)
                else: self._run_command_string(car, e)
            return
        if cmd.startswith("="): car.value = self._parse_value(cmd[1:])
        elif cmd.startswith("+="): car.value += self._parse_value(cmd[2:])
        elif cmd.startswith("-="): car.value -= self._parse_value(cmd[2:])
        elif cmd.startswith("*="): car.value *= self._parse_value(cmd[2:])
        elif cmd.startswith("/="):
            v = self._parse_value(cmd[2:]); car.value = car.value / v if v != 0 else 0
        elif cmd in ('%L', '%R', '%U', '%D'): self._set_valid_direction(car, cmd[1])

    def _evaluate_condition(self, car, cond):
        cond = cond.strip()
        if cond == "**": return self.is_signal_active
        ops = ["==", "!=", ">=", "<=", ">", "<"]
        for op in ops:
            if cond.startswith(op):
                v = self._parse_value(cond[len(op):])
                try:
                    if op == "==": return car.value == v
                    if op == "!=": return car.value != v
                    if op == ">": return car.value > v
                    if op == "<": return car.value < v
                    if op == ">=": return car.value >= v
                    if op == "<=": return car.value <= v
                except: return False
        return False

    def _parse_value(self, val_str: str):
        val_str = val_str.strip()
        if (val_str.startswith('"') and val_str.endswith('"')) or \
           (val_str.startswith("'") and val_str.endswith("'")):
            return val_str[1:-1].replace("\\n", "\n")
        try:
            if '.' in val_str: return float(val_str)
            return int(val_str)
        except: return val_str

    def _set_valid_direction(self, car, pref):
        car.direction = pref
        if not self._can_move_to(car.row, car.col, car.direction): self._resolve_collision(car)

    def _resolve_collision(self, car):
        checks = {'U':['R','L','D'], 'D':['L','R','U'], 'L':['U','D','R'], 'R':['D','U','L']}
        for d in checks[car.direction]:
            if self._can_move_to(car.row, car.col, d):
                car.direction = d
                return

    def _can_move_to(self, r, c, d):
        if d == 'U': r -= 1
        elif d == 'D': r += 1
        elif d == 'L': c -= 1
        elif d == 'R': c += 1
        return self._get_cell(r, c) not in (None, '##')

    def _get_cell(self, r, c):
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[r]): return self.grid[r][c]
        return None

    def is_running(self): return len(self.cars) > 0