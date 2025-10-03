from gpiozero import Button
import time

class ButtonHandler:
    def __init__(self, pin=17, hold_time=1.5):
        self.button = Button(pin, pull_up=True)
        self.hold_time = hold_time

    def wait_for_event(self):
        print("[DEBUG] Waiting for GPIO button event...")
        self.button.wait_for_press()
        press_time = time.time()
        self.button.wait_for_release()
        release_time = time.time()

        held = release_time - press_time
        event = "long_press" if held >= self.hold_time else "short_press"
        print(f"[DEBUG] GPIO button event: {event} (held {held:.2f}s)")
        return event
