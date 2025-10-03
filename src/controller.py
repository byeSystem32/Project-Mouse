import time
from evdev import InputDevice, categorize, ecodes, list_devices

class ControllerHandler:
    def __init__(self, hold_time=1.5, device_name="Pro Controller"):
        self.hold_time = hold_time
        self.last_press_time = {}
        self.device = None

        # Find controller device by name
        for path in list_devices():
            dev = InputDevice(path)
            if device_name in dev.name:
                self.device = dev
                print(f"[DEBUG] Controller connected: {dev.name} ({path})")
                break

        if not self.device:
            raise RuntimeError("Controller not found! Check Bluetooth connection.")

    def wait_for_event(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                codes = key_event.keycode if isinstance(key_event.keycode, list) else [key_event.keycode]
                state = key_event.keystate
                print(f"[DEBUG] Controller raw event: {codes}, state={state}")

                # Only react on button press (state == 1)
                if state != key_event.key_down:
                    continue

                # A button (BTN_SOUTH) → select
                if "BTN_SOUTH" in codes or "BTN_A" in codes:
                    press_time = time.time()
                    self.last_press_time["BTN_SOUTH"] = press_time
                    return "select"

                # B button (BTN_EAST) → back
                if "BTN_EAST" in codes or "BTN_B" in codes:
                    return "back"

                # X button (BTN_NORTH) → down
                if "BTN_NORTH" in codes or "BTN_X" in codes:
                    return "down"

                # Y button (BTN_WEST) → up
                if "BTN_WEST" in codes or "BTN_Y" in codes:
                    return "up"