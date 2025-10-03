from inputs import get_gamepad
import time

class ControllerHandler:
    def __init__(self, hold_time=1.5):
        self.hold_time = hold_time
        self.last_press_time = None
        self.held_button = None

    def wait_for_event(self):
        """
        Blocks until a mapped event occurs.
        Returns: "short_press" or "long_press"
        """
        while True:
            events = get_gamepad()
            for event in events:
                # Example: D-Pad Down -> short_press
                if event.code == "ABS_HAT0Y" and event.state == 1:
                    return "short_press"

                # Example: A button (BTN_SOUTH) -> short or long press
                if event.code == "BTN_SOUTH":
                    if event.state == 1:  # button down
                        self.last_press_time = time.time()
                    elif event.state == 0 and self.last_press_time:
                        held_time = time.time() - self.last_press_time
                        self.last_press_time = None
                        if held_time >= self.hold_time:
                            return "long_press"
                        else:
                            return "short_press"