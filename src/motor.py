from gpiozero import PWMOutputDevice
import time

class Motor:
    def __init__(self, pin=18):
        self.vib = PWMOutputDevice(pin)

    def buzz(self, duration=0.3, strength=0.8):
        """Trigger vibration motor"""
        self.vib.value = strength
        time.sleep(duration)
        self.vib.off()
