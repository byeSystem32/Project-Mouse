from buttons import ButtonHandler
from controller import ControllerHandler

class InputHandler:
    def __init__(self, hold_time=1.5):
        self.hold_time = hold_time

        # Try controller first
        try:
            self.device = ControllerHandler(hold_time=hold_time, device_path="/dev/input/event2")
            print("[DEBUG] Using controller input (event2)")
        except Exception as e:
            print(f"[WARN] Controller not available: {e}")
            self.device = ButtonHandler(pin=23, hold_time=hold_time)
            print("[DEBUG] Using GPIO button input (GPIO23)")

    def wait_for_event(self):
        event = self.device.wait_for_event()
        print(f"[DEBUG] InputHandler -> {event}")
        return event