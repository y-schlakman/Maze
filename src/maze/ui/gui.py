import sys
import tkinter as tk
from tkinter import simpledialog
from maze.ui.base import UserInterface

try:
    import pygame
except ImportError:
    pygame = None


class GUI(UserInterface):
    def __init__(self, interpreter, fps: int = 5):
        super().__init__(interpreter)
        self.fps = fps
        self.paused = True

        # Dimensions
        self.DASHBOARD_W = 220

        # Colors
        self.COLOR_BG = (20, 20, 25)
        self.COLOR_WALL = (45, 52, 54)
        self.COLOR_PATH = (223, 230, 233)
        self.COLOR_START = (0, 184, 148)
        self.COLOR_HOLE = (214, 48, 49)
        self.COLOR_CAR = (9, 132, 227)
        self.COLOR_SYMBOL = (99, 110, 114)
        self.COLOR_DASH_BG = (30, 30, 35)

    def _handle_gui_input(self):
        root = tk.Tk()
        root.withdraw()
        user_input = simpledialog.askstring("Maze Input", "Enter value for car:", parent=root)
        root.destroy()
        self.interpreter.set_input_value(user_input if user_input is not None else 0)

    def run(self):
        pygame.init()
        display_info = pygame.display.Info()

        # Calculate available width minus the dashboard space
        max_w = display_info.current_w - 100 - self.DASHBOARD_W
        max_h = display_info.current_h - 100

        grid_rows = len(self.interpreter.grid)
        grid_cols = max(len(row) for row in self.interpreter.grid) if grid_rows > 0 else 1

        self.cell_size = min(max_w // grid_cols, max_h // grid_rows, 80)
        self.cell_size = max(self.cell_size, 15)

        # Total window width includes the maze grid + dashboard
        win_w = (grid_cols * self.cell_size) + self.DASHBOARD_W
        win_h = max(grid_rows * self.cell_size, 300)  # Ensure window is at least 300px tall for the dash

        screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
        pygame.display.set_caption("Maze Debugger - [Space: Play/Pause] [S: Step]")

        self.font = pygame.font.SysFont("monospace", max(self.cell_size // 3, 10), bold=True)
        self.status_font = pygame.font.SysFont("monospace", 14, bold=True)
        clock = pygame.time.Clock()

        running = True
        while running:
            step_once = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_s and self.paused:
                        step_once = True
                    elif event.key == pygame.K_RETURN and (pygame.key.get_mods() & pygame.KMOD_ALT):
                        pygame.display.toggle_fullscreen()

            if self.interpreter.waiting_for_input:
                self._handle_gui_input()

            should_tick = (
                                      not self.paused or step_once) and self.interpreter.is_running() and not self.interpreter.waiting_for_input

            if should_tick:
                outputs = self.interpreter.tick()
                for out in outputs:
                    self.handle_output(str(out))

            # Render
            screen.fill(self.COLOR_BG)
            self._draw_grid(screen)
            self._draw_cars(screen)

            # Draw the new side panel
            maze_width = grid_cols * self.cell_size
            self._draw_dashboard(screen, maze_width)

            self._draw_status(screen, maze_width)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def _draw_grid(self, surface):
        for r, row in enumerate(self.interpreter.grid):
            for c, cell in enumerate(row):
                rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                if cell == '##':
                    pygame.draw.rect(surface, self.COLOR_WALL, rect)
                elif cell == '^^':
                    pygame.draw.rect(surface, self.COLOR_START, rect)
                elif cell == '()':
                    pygame.draw.rect(surface, self.COLOR_HOLE, rect)
                elif cell == '**':
                    color = (255, 255, 100) if self.interpreter.is_signal_active else (150, 150, 50)
                    pygame.draw.rect(surface, color, rect)
                else:
                    pygame.draw.rect(surface, self.COLOR_PATH, rect)
                    pygame.draw.rect(surface, (200, 200, 200), rect, 1)
                    if cell not in ('..', '--') and self.cell_size > 20:
                        txt = self.font.render(cell, True, self.COLOR_SYMBOL)
                        surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_cars(self, surface):
        for i, car in enumerate(self.interpreter.cars):
            center = (car.col * self.cell_size + self.cell_size // 2, car.row * self.cell_size + self.cell_size // 2)
            pygame.draw.circle(surface, self.COLOR_CAR, center, (self.cell_size * 3) // 8)

            # Draw a simple ID number on the car instead of the full value
            id_txt = self.font.render(str(i + 1), True, (255, 255, 255))
            surface.blit(id_txt, id_txt.get_rect(center=center))

    def _draw_dashboard(self, surface, start_x):
        """Renders the side panel with car values."""
        panel_rect = pygame.Rect(start_x, 0, self.DASHBOARD_W, surface.get_height())
        pygame.draw.rect(surface, self.COLOR_DASH_BG, panel_rect)

        # Add a subtle border line between maze and dashboard
        pygame.draw.line(surface, (70, 70, 80), (start_x, 0), (start_x, surface.get_height()), 2)

        # Title
        title = self.font.render("ACTIVE CARS", True, self.COLOR_START)
        surface.blit(title, (start_x + 15, 15))

        y_offset = 50
        for i, car in enumerate(self.interpreter.cars):
            # Stop drawing if we run out of vertical space
            if y_offset > surface.get_height() - 40:
                more_txt = self.status_font.render(f"...and {len(self.interpreter.cars) - i} more", True,
                                                   (150, 150, 150))
                surface.blit(more_txt, (start_x + 15, y_offset))
                break

            val_str = str(car.value)
            # Truncate string if it is too long to fit in the panel
            if len(val_str) > 12:
                val_str = val_str[:10] + ".."

            # Format: [1] Dir:R -> 55
            text = self.status_font.render(f"[{i + 1}] {car.direction} | {val_str}", True, (255, 255, 255))
            surface.blit(text, (start_x + 15, y_offset))
            y_offset += 25

    def _draw_status(self, surface, max_w):
        status_text = "PAUSED [S to Step]" if self.paused else "RUNNING [Space to Pause]"
        if not self.interpreter.is_running():
            status_text = "SIMULATION FINISHED"

        txt = self.status_font.render(status_text, True, (255, 255, 0))
        # Keep status text inside the maze boundaries, not the dashboard
        rect = txt.get_rect(bottomleft=(10, surface.get_height() - 10))

        bg_rect = rect.inflate(10, 5)
        pygame.draw.rect(surface, (0, 0, 0), bg_rect)
        surface.blit(txt, rect)