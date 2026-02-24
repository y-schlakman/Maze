from maze.ui.base import UserInterface


class CLI(UserInterface):
    def run(self):
        while self.interpreter.is_running():
            # Check for input state
            if self.interpreter.waiting_for_input:
                user_val = input("\n[INPUT REQUIRED] Enter value for car: ")
                self.interpreter.set_input_value(user_val)

            outputs = self.interpreter.tick()
            for out in outputs:
                self.handle_output(str(out))

        print("\n[Maze Execution Finished]")