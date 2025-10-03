import RPi.GPIO as GPIO
import time

# Change this to your actual GPIO pin number
BUTTON_PIN = 17   # Example: GPIO17 (physical pin 11)

# Setup
GPIO.setmode(GPIO.BCM)       # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# ^ assumes button connects pin to GND when pressed

print("Press the button (Ctrl+C to quit)")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:   # Button pressed
            print("Button PRESSED")
        else:
            print("Button released")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nExiting program")

finally:
    GPIO.cleanup()
