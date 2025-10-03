from gpiozero import Button
import time

class ButtonHandler:
    def __init__(self, pin=17, hold_time=2):
        """
        pin: GPIO pin for button
        hold_time: seconds to consider as long press
        """
        self.button = Button(pin, pull_up=True)
        self.hold_time = hold_time

    def wait_for_event(self):
        """
        Blocks until a button press event occurs.
        Returns "short_press" or "long_press".
        """
        self.button.wait_for_press()
        press_time = time.time()
        self.button.wait_for_release()
        release_time = time.time()

        held_time = release_time - press_time
        if held_time >= self.hold_time:
            return "long_press"
        else:
            return "short_press"