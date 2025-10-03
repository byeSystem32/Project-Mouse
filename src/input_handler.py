import time

# Import GPIO button handler
from buttons import ButtonHandler

# Try to import evdev (controller support)
try:
    from controller import ControllerHandler
    HAS_CONTROLLER = True
except ImportError:
    HAS_CONTROLLER = False


class InputHandler:
    def __init__(self, hold_time=1.5, button_pin=17):
        """
        Unified input handler. Supports both GPIO button and controller.
        """
        self.device = None

        if HAS_CONTROLLER:
            try:
                self.device = ControllerHandler(hold_time=hold_time)
                print("[INFO] Using controller for input")
            except Exception as e:
                print(f"[WARN] Controller not available: {e}")
                self.device = None

        if self.device is None:
            self.device = ButtonHandler(pin=button_pin, hold_time=hold_time)
            print("[INFO] Using GPIO button for input")

    def wait_for_event(self):
        return self.device.wait_for_event()