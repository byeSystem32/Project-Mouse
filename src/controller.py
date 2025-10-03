import os, time
from evdev import InputDevice, categorize, ecodes, list_devices

class ControllerHandler:
    def __init__(self, hold_time=1.5, device_name="Pro Controller (IMU)"):
        self.hold_time = hold_time
        self.last_press_time = {}

        # Auto-find the controller device by name
        self.device = None
        for dev_path in list_devices():
            dev = InputDevice(dev_path)
            if device_name in dev.name:
                self.device = dev
                break

        if not self.device:
            raise RuntimeError("Controller not found! Make sure it's connected over Bluetooth.")

    def wait_for_event(self):
        """
        Blocks until a mapped controller action is detected.
        Returns 'short_press' or 'long_press'.
        """
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                code = key_event.keycode

                # Example mapping:
                # A button (BTN_SOUTH) = short/long press
                if code == "BTN_SOUTH":
                    if key_event.keystate == key_event.key_down:
                        self.last_press_time[code] = time.time()
                    elif key_event.keystate == key_event.key_up:
                        press_time = self.last_press_time.get(code, time.time())
                        held = time.time() - press_time
                        self.last_press_time[code] = None
                        if held >= self.hold_time:
                            return "long_press"
                        else:
                            return "short_press"

                # D-pad down = short_press (cycle down in menu)
                if code == "BTN_DPAD_DOWN" and key_event.keystate == key_event.key_down:
                    return "short_press"

                # D-pad up = (optional) could map to 'short_press_up' later
                if code == "BTN_DPAD_UP" and key_event.keystate == key_event.key_down:
                    return "short_press"
