from gpiozero import Button
import time

class ButtonHandler:
    def __init__(self, pin=17, hold_time=2.0):
        self.button = Button(pin, pull_up=True)
        self.hold_time = hold_time

    def wait_for_event(self):
        self.button.wait_for_press()
        press_time = time.time()
        self.button.wait_for_release()
        release_time = time.time()

        held = release_time - press_time
        if held >= self.hold_time:
            print(f"[DEBUG] GPIO long hold detected ({held:.2f}s)")
            return "hold"
        else:
            print(f"[DEBUG] GPIO single click detected ({held:.2f}s)")
            return "click"