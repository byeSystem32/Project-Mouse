import os, shutil, time
from buttons import ButtonHandler
from camera import Camera
from chatgpt import send_to_chatgpt
from ui import MenuUI
from motor import Motor
import wifi

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

# ---------------- MENU HANDLERS ---------------- #

def test_device(ui, cam, motor):
    """Tests camera + motor"""
    try:
        ui.show_message("Testing Camera...")
        filename = cam.capture(TEMP_DIR)
        time.sleep(1)

        ui.show_message("Testing Motor...")
        motor.buzz(duration=0.5, strength=0.8)
        time.sleep(1)

        ui.show_message("Completed!")
        time.sleep(2)
    except Exception as e:
        ui.show_message("Test Failed:\n" + str(e))
        time.sleep(3)

def config_wifi(ui, buttons):
    """WiFi profile selector"""
    profiles = wifi.load_profiles()
    if not profiles:
        ui.show_message("No wifi profiles")
        time.sleep(2)
        return

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
                return
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

# ---------------- MAIN MENU ---------------- #

def main():
    buttons = ButtonHandler(pin=17, hold_time=2)
    cam = Camera()
    ui = MenuUI()
    motor = Motor(pin=18)

    menu = ["Test Device", "Config WiFi", "Start"]
    idx = 0

    while True:
        ui.show_message(f"> {menu[idx]}")  # ">" = indicator

        event = buttons.wait_for_event()
        if event == "short_press":
            idx = (idx + 1) % len(menu)

        elif event == "long_press":
            choice = menu[idx]

            if choice == "Test Device":
                test_device(ui, cam, motor)

            elif choice == "Config WiFi":
                config_wifi(ui, buttons)

            elif choice == "Start":
                ui.show_message("System Ready")
                photo_loop(ui, buttons, cam, motor)

if __name__ == "__main__":
    main()
