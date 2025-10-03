from buttons import ButtonHandler

try:
    from controller import ControllerHandler
    HAS_CONTROLLER = True
except ImportError:
    HAS_CONTROLLER = False

class InputHandler:
    def __init__(self, hold_time=1.5, button_pin=17):
        self.device = None

        if HAS_CONTROLLER:
            try:
                self.device = ControllerHandler(hold_time=hold_time)
                print("[DEBUG] Controller detected, using controller input")
            except Exception as e:
                print(f"[WARN] Controller init failed: {e}")
                self.device = None

        if self.device is None:
            self.device = ButtonHandler(pin=button_pin, hold_time=hold_time)
            print("[DEBUG] Using GPIO button input")

    def wait_for_event(self):
        event = self.device.wait_for_event()
        print(f"[DEBUG] InputHandler -> {event}")
        return event
