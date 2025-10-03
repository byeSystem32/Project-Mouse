import os, shutil, time
from input_handler import InputHandler
from camera import Camera
from chatgpt import send_to_chatgpt
from ui import MenuUI
from motor import Motor
import wifi
import bluetooth_config

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
    print("[DEBUG] Moved temp photos to saved")


# ---------------- MENU HANDLERS ---------------- #

def test_device(ui, cam, motor):
    try:
        ui.show_message("Testing Camera...")
        filename = cam.capture(TEMP_DIR)
        print(f"[DEBUG] Test Device: Captured {filename}")
        time.sleep(1)

        ui.show_message("Testing Motor...")
        motor.buzz(duration=0.5, strength=0.8)
        print("[DEBUG] Test Device: Motor buzzed")
        time.sleep(1)

        ui.show_message("Completed!")
        print("[DEBUG] Test Device: Completed successfully")
        time.sleep(2)
    except Exception as e:
        ui.show_message("Test Failed")
        print(f"[ERROR] Test Device failed: {e}")
        time.sleep(3)


def config_settings(ui, buttons):
    config_menu = ["WiFi Config", "Bluetooth Config", "Back"]
    idx = 0

    while True:
        ui.show_menu(config_menu, selected=idx)
        event = buttons.wait_for_event()
        print(f"[DEBUG] Config menu event: {event}")

        if event == "down":
            idx = (idx + 1) % len(config_menu)
        elif event == "up":
            idx = (idx - 1) % len(config_menu)
        elif event == "select":
            choice = config_menu[idx]
            print(f"[DEBUG] Config menu selected: {choice}")

            if choice == "WiFi Config":
                config_wifi(ui, buttons)
            elif choice == "Bluetooth Config":
                bluetooth_config.run(ui, buttons)
            elif choice == "Back":
                return
        elif event == "back":
            print("[DEBUG] Back pressed -> Returning to main menu")
            return


def config_wifi(ui, buttons):
    profiles = wifi.load_profiles()
    if not profiles:
        ui.show_message("No wifi profiles")
        print("[WARN] No WiFi profiles found")
        time.sleep(2)
        return

    idx = 0
    while True:
        profile_names = [p["network_name"] for p in profiles]
        ui.show_menu(profile_names, selected=idx)

        event = buttons.wait_for_event()
        print(f"[DEBUG] WiFi config event: {event}")

        if event == "down":
            idx = (idx + 1) % len(profiles)
        elif event == "up":
            idx = (idx - 1) % len(profiles)
        elif event == "select":
            chosen = profiles[idx]
            print(f"[DEBUG] Attempting WiFi connect: {chosen}")
            success, msg = wifi.connect(chosen)
            if success:
                ui.show_message(f"Connected:\n{chosen['network_name']}")
                print("[DEBUG] WiFi connected successfully")
                time.sleep(2)
                return
            else:
                ui.show_message("Failed WiFi")
                print(f"[ERROR] WiFi failed: {msg}")
                time.sleep(2)
        elif event == "back":
            print("[DEBUG] Back pressed -> Returning to Config Settings")
            return


def photo_loop(ui, buttons, cam, motor):
    idx = 1
    while True:
        ui.show_message(f"Photo Mode\nQ{idx}")
        event = buttons.wait_for_event()
        print(f"[DEBUG] Photo loop event: {event}")

        if event == "down":
            idx += 1
        elif event == "up" and idx > 1:
            idx -= 1
        elif event == "select":
            filename = cam.capture(TEMP_DIR)
            ui.show_message(f"Saved:\nQ{idx}\n{os.path.basename(filename)}")
            print(f"[DEBUG] Photo saved: {filename}")
        elif event == "back":
            ui.show_message("Sending...")
            print("[DEBUG] Sending photos to ChatGPT...")
            result = send_to_chatgpt(TEMP_DIR)
            move_temp_to_main()
            ui.show_message(f"Result:\n{result}")
            motor.buzz(duration=0.3, strength=0.6)
            print(f"[DEBUG] ChatGPT result: {result}")


# ---------------- MAIN MENU ---------------- #

def main():
    buttons = InputHandler(hold_time=1.5)
    cam = Camera()
    ui = MenuUI()
    motor = Motor(pin=18)

    menu = ["Test Device", "Config Settings", "Start"]
    idx = 0

    print("[DEBUG] Entering main loop...")

    while True:
        ui.show_menu(menu, selected=idx)
        event = buttons.wait_for_event()
        print(f"[DEBUG] Main menu event: {event}")

        if event == "down":
            idx = (idx + 1) % len(menu)
            print(f"[DEBUG] Menu index changed to {idx}")
        elif event == "up":
            idx = (idx - 1) % len(menu)
            print(f"[DEBUG] Menu index changed to {idx}")
        elif event == "select":
            choice = menu[idx]
            print(f"[DEBUG] Menu choice selected: {choice}")

            if choice == "Test Device":
                test_device(ui, cam, motor)
            elif choice == "Config Settings":
                config_settings(ui, buttons)
            elif choice == "Start":
                ui.show_message("System Ready")
                print("[DEBUG] Entering photo loop...")
                photo_loop(ui, buttons, cam, motor)
        elif event == "back":
            print("[DEBUG] Back pressed (ignored in main menu)")


if __name__ == "__main__":
    main()