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
        if held >= self.hold_time:
            print(f"[DEBUG] GPIO button long press (select) held {held:.2f}s")
            return "select"
        else:
            print(f"[DEBUG] GPIO button short press (down) held {held:.2f}s")
            return "down"