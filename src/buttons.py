from gpiozero import Button
import time

class ButtonHandler:
    def __init__(self, pin=17, hold_time=2.0, double_time=0.4):
        self.button = Button(pin, pull_up=True)
        self.hold_time = hold_time
        self.double_time = double_time
        self.last_click_time = 0

    def wait_for_event(self):
        self.button.wait_for_press()
        press_time = time.time()
        self.button.wait_for_release()
        release_time = time.time()

        held = release_time - press_time

        # Check hold
        if held >= self.hold_time:
            print(f"[DEBUG] GPIO long hold detected ({held:.2f}s)")
            return "hold"

        # Check double click
        now = time.time()
        if now - self.last_click_time <= self.double_time:
            self.last_click_time = 0
            print("[DEBUG] GPIO double click detected")
            return "double"

        self.last_click_time = now
        print(f"[DEBUG] GPIO single click detected ({held:.2f}s)")
        return "click"