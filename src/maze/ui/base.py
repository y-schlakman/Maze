from abc import ABC, abstractmethod
from maze.core.interpreter import Interpreter

class UserInterface(ABC):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter

    @abstractmethod
    def run(self):
        """Starts the main execution loop."""
        pass

    def handle_output(self, output: str):
        """Handles the '>>' print commands from the cars."""
        # By default, we just print to standard out without a newline,
        # as esoteric languages often build strings character by character.
        print(output, end="", flush=True)