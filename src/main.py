import os, shutil, time
from buttons import ButtonHandler
from camera import Camera
from chatgpt import send_to_chatgpt
from ui import MenuUI
from motor import Motor
import wifi   # <--- NEW

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "../photos/temp")
MAIN_DIR = os.path.join(BASE_DIR, "../photos/saved")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(MAIN_DIR, exist_ok=True)

def move_temp_to_main():
    for file in os.listdir(TEMP_DIR):
        src = os.path.join(TEMP_DIR, file)
        dst = os.path.join(MAIN_DIR, file)
        shutil.move(src, dst)

def choose_wifi(ui, buttons):
    """Dropdown wifi profile selector"""
    profiles = wifi.load_profiles()
    if not profiles:
        ui.show_message("No wifi profiles")
        time.sleep(2)
        return None

    idx = 0
    while True:
        profile = profiles[idx]
        ui.show_message(f"WiFi:\n{profile['network_name']}")

        event = buttons.wait_for_event()
        if event == "short_press":
            idx = (idx + 1) % len(profiles)
        elif event == "long_press":
            success, msg = wifi.connect(profile)
            if success:
                ui.show_message(f"Connected:\n{profile['network_name']}")
                time.sleep(2)
                return profile
            else:
                ui.show_message("Failed:\n" + msg)
                time.sleep(2)

def photo_loop(ui, buttons, cam, motor):
    """Main photo-taking loop"""
    while True:
        event = buttons.wait_for_event()

        if event == "short_press":
            filename = cam.capture(TEMP_DIR)
            ui.show_message(f"Saved:\n{os.path.basename(filename)}")

        elif event == "long_press":
            ui.show_message("Sending...")
            result = send_to_chatgpt(TEMP_DIR)

            move_temp_to_main()
            ui.show_message(f"Result:\n{result}")
            motor.buzz(duration=0.3, strength=0.6)

        time.sleep(0.1)

def main():
    buttons = ButtonHandler(pin=17, hold_time=2)
    cam = Camera()
    ui = MenuUI()
    motor = Motor(pin=18)

    ui.show_message("Choose WiFi")
    chosen = choose_wifi(ui, buttons)

    # After wifi connect, go to photo mode
    ui.show_message("System Ready")
    photo_loop(ui, buttons, cam, motor)

if __name__ == "__main__":
    main()
