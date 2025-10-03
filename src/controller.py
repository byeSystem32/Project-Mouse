from evdev import InputDevice, categorize, ecodes

class ControllerHandler:
    def __init__(self, device_path="/dev/input/event2"):
        self.device = InputDevice(device_path)
        print(f"[DEBUG] Controller connected: {self.device.name} ({device_path})")

    def wait_for_event(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                codes = key_event.keycode if isinstance(key_event.keycode, list) else [key_event.keycode]
                state = key_event.keystate

                if state != key_event.key_down:
                    continue

                print(f"[DEBUG] Controller event: {codes}")

                if "BTN_WEST" in codes or "BTN_Y" in codes:
                    return "click"
                if "BTN_SOUTH" in codes or "BTN_A" in codes:
                    return "hold"