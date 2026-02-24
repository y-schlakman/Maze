# src/maze/__main__.py

import argparse
import sys
import os
from maze.core.interpreter import Interpreter
from maze.ui.cli import CLI
from maze.ui.gui import GUI


def main():
    parser = argparse.ArgumentParser(description="Maze Esolang Interpreter")
    parser.add_argument("filepath", help="Path to the .mz source file")
    parser.add_argument("--gui", action="store_true", help="Run with the visual debugger")
    parser.add_argument("--fps", type=int, default=5, help="Simulation speed (ticks per second) in GUI mode")

    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        sys.exit(1)

    with open(args.filepath, 'r') as f:
        source_code = f.read()

    interpreter = Interpreter()
    interpreter.load_source(source_code)

    if args.gui:
        ui = GUI(interpreter, fps=args.fps)
    else:
        ui = CLI(interpreter)

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nExecution aborted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()