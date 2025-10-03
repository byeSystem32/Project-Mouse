from buttons import ButtonHandler
from controller import ControllerHandler

class InputHandler:
    def __init__(self, hold_time=2.0):
        try:
            self.device = ControllerHandler(device_path="/dev/input/event2")
            print("[DEBUG] Using controller input (event2)")
        except Exception as e:
            print(f"[WARN] Controller not available: {e}")
            self.device = ButtonHandler(pin=17, hold_time=hold_time)
            print("[DEBUG] Using GPIO button input (GPIO17)")

    def wait_for_event(self):
        event = self.device.wait_for_event()
        print(f"[DEBUG] InputHandler -> {event}")
        return event