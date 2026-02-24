# Maze Esolang Interpreter

A robust Python interpreter and visual interactive debugger for **Maze**, a 2D esoteric programming language where execution flow is determined by "cars" navigating a grid of ASCII walls and paths.

*This project was built as a fun little vibe coding mini-project to showcase the power and unique nature of the Maze concept.*

This project provides both a blazing-fast CLI execution environment and a feature-rich graphical debugger powered by Pygame Community Edition (`pygame-ce`), making it easy to build, step through, and understand complex Turing-complete Maze programs.

**Original Language Credit:** Maze was originally conceived by the Esolang community. Read the full language specification on the [Esolang Wiki](https://esolangs.org/wiki/Maze).

---

## 🚀 Features

* **Fully Compliant Interpreter:** Supports all standard Maze instructions, including cloning (`<>`), conditional branching (`IF THEN ELSE`), arithmetic (`+=`, `/=`), and global signal broadcasting (`**`).
* **Visual GUI Debugger:** Watch your cars navigate the grid in real-time.
* **Step-by-Step Execution:** Pause the simulation and advance frame-by-frame to debug complex race-conditions (like those found in Fibonacci sequence generators).
* **Live Dashboard:** Monitor the exact values and directional states of all active cars dynamically.
* **Interactive Prompts:** Fully supports the `<<` input command via terminal or GUI dialogs.

---

## 📦 Installation

Ensure you have Python 3.8+ installed. You can install the package directly from the source code.

1. Clone or download this repository.
2. Navigate to the project root directory (where `pyproject.toml` is located).
3. Run the following command to install the package and its dependencies (it will automatically install `pygame-ce`):

```bash
pip install .

```

*Tip: Use `pip install -e .` if you plan to modify the source code so your changes update instantly.*

---

## 🕹️ Usage

Installing the package registers the `maze` command globally on your system.

### Command Line Interface (CLI)

To run a Maze script quietly in the terminal:

```bash
maze my_script.mz

```

### Graphical User Interface (GUI)

To launch the visual debugger, append the `--gui` flag:

```bash
maze my_script.mz --gui

```

**GUI Controls:**

* `Spacebar`: Toggle Play/Pause. (The simulation starts paused by default).
* `S`: Step forward exactly one tick (must be paused).
* `Alt + Enter`: Toggle Fullscreen.

**Additional Flags:**

* `--fps <number>`: Control the execution speed in GUI mode (default is 5). Example: `maze file.mz --gui --fps 15`

---

## 🧠 Code Architecture

This project strictly separates the logic engine from the rendering layers:

* **`core.interpreter`**: The heart of the engine. It utilizes a two-phase tick system (Phase 1: Movement, Phase 2: Instruction Execution) to ensure accurate synchronization of global signals (`**`) and pause states.
* **`core.car`**: The lightweight data structure representing an execution pointer.
* **`ui.gui` & `ui.cli**`: The presentation layers. The GUI is built dynamically to scale and fit any maze size to your monitor's resolution.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.