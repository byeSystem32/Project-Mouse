import time
from evdev import InputDevice, categorize, ecodes

class ControllerHandler:
    def __init__(self, hold_time=1.5, device_path="/dev/input/event2"):
        self.hold_time = hold_time
        self.last_press_time = {}
        self.device = InputDevice(device_path)
        print(f"[DEBUG] Controller connected: {self.device.name} ({device_path})")

    def wait_for_event(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                codes = key_event.keycode if isinstance(key_event.keycode, list) else [key_event.keycode]
                state = key_event.keystate
                print(f"[DEBUG] Controller raw event: {codes}, state={state}")

                # Only handle button pressed (state==1)
                if state != key_event.key_down:
                    continue

                # A button = select
                if "BTN_SOUTH" in codes or "BTN_A" in codes:
                    return "select"

                # B button = back
                if "BTN_EAST" in codes or "BTN_B" in codes:
                    return "back"

                # X button = down
                if "BTN_NORTH" in codes or "BTN_X" in codes:
                    return "down"

                # Y button = up
                if "BTN_WEST" in codes or "BTN_Y" in codes:
                    return "up"