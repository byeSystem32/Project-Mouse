import time
from evdev import InputDevice, categorize, ecodes, list_devices

class ControllerHandler:
    def __init__(self, hold_time=1.5, device_name="Pro Controller (IMU)"):
        self.hold_time = hold_time
        self.last_press_time = {}

        # Try to find the controller by name
        self.device = None
        for path in list_devices():
            dev = InputDevice(path)
            if device_name in dev.name:
                self.device = dev
                print(f"[DEBUG] Controller connected: {dev.name} ({path})")
                break

        if not self.device:
            raise RuntimeError("Controller not found! Check Bluetooth connection.")

    def wait_for_event(self):
        print("[DEBUG] Waiting for controller event...")
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                code = key_event.keycode
                print(f"[DEBUG] Raw controller event: {code}, state={key_event.keystate}")

                # A button (BTN_SOUTH)
                if code == "BTN_SOUTH":
                    if key_event.keystate == key_event.key_down:
                        self.last_press_time[code] = time.time()
                    elif key_event.keystate == key_event.key_up:
                        press_time = self.last_press_time.get(code, time.time())
                        held = time.time() - press_time
                        self.last_press_time[code] = None
                        event_type = "long_press" if held >= self.hold_time else "short_press"
                        print(f"[DEBUG] Controller event: {event_type} (held {held:.2f}s)")
                        return event_type

                # D-pad down = short_press
                if code == "BTN_DPAD_DOWN" and key_event.keystate == key_event.key_down:
                    print("[DEBUG] Controller D-pad down -> short_press")
                    return "short_press"

                # D-pad up = short_press (optional extra navigation)
                if code == "BTN_DPAD_UP" and key_event.keystate == key_event.key_down:
                    print("[DEBUG] Controller D-pad up -> short_press")
                    return "short_press"