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

SCREEN_TIMEOUT = 10  # seconds of inactivity before OLED turns off

def move_temp_to_main():
    for file in os.listdir(TEMP_DIR):
        src = os.path.join(TEMP_DIR, file)
        dst = os.path.join(MAIN_DIR, file)
        shutil.move(src, dst)
    print("[DEBUG] Moved temp photos to saved")

# ---------------- MENU HANDLERS ---------------- #

def test_device(ui, cam, motor):
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

def config_settings(ui, buttons, motor):
    config_menu = ["WiFi Config", "Bluetooth Config", "Back"]
    idx = 0
    last_active = time.time()
    screen_on = True

    while True:
        if screen_on:
            ui.show_menu(config_menu, selected=idx)

        event = buttons.wait_for_event()
        last_active = time.time()

        if not screen_on:
            screen_on = True
            ui.show_menu(config_menu, selected=idx)
            continue

        if event == "click":
            idx = (idx + 1) % len(config_menu)
            ui.show_menu(config_menu, selected=idx)

        elif event == "hold":
            choice = config_menu[idx]
            ui.show_message(f"Selected:\n{choice}")
            print(f"[DEBUG] Config menu selected: {choice}")
            time.sleep(0.5)
            if choice == "WiFi Config":
                config_wifi(ui, buttons)
            elif choice == "Bluetooth Config":
                bluetooth_config.run(ui, buttons)
            elif choice == "Back":
                return

        # Auto turn off
        if screen_on and (time.time() - last_active > SCREEN_TIMEOUT):
            ui.clear()
            screen_on = False
            print("[DEBUG] Screen auto-off in Config")

def config_wifi(ui, buttons):
    profiles = wifi.load_profiles()
    if not profiles:
        ui.show_message("No wifi profiles")
        print("[WARN] No WiFi profiles found")
        time.sleep(2)
        return

    idx = 0
    last_active = time.time()
    screen_on = True

    while True:
        if screen_on:
            profile_names = [p["network_name"] for p in profiles]
            ui.show_menu(profile_names, selected=idx)

        event = buttons.wait_for_event()
        last_active = time.time()

        if not screen_on:
            screen_on = True
            ui.show_menu(profile_names, selected=idx)
            continue

        if event == "click":
            idx = (idx + 1) % len(profiles)
            ui.show_menu(profile_names, selected=idx)

        elif event == "hold":
            chosen = profiles[idx]
            success, msg = wifi.connect(chosen)
            if success:
                ui.show_message(f"Connected:\n{chosen['network_name']}")
                time.sleep(2)
                return
            else:
                ui.show_message("Failed WiFi")
                time.sleep(2)

        if screen_on and (time.time() - last_active > SCREEN_TIMEOUT):
            ui.clear()
            screen_on = False
            print("[DEBUG] Screen auto-off in WiFi config")

def photo_loop(ui, buttons, cam, motor):
    last_active = time.time()
    screen_on = True

    while True:
        if screen_on:
            ui.show_message("Photo Mode")

        event = buttons.wait_for_event()
        last_active = time.time()

        if not screen_on:
            screen_on = True
            ui.show_message("Photo Mode")
            continue

        if event == "click":
            filename = cam.capture(TEMP_DIR)
            ui.show_message(f"Saved:\n{os.path.basename(filename)}")
            motor.buzz(duration=0.2, strength=0.5)
            print(f"[DEBUG] Photo saved: {filename}")

        elif event == "hold":
            ui.show_message("Sending...")
            result = send_to_chatgpt(TEMP_DIR)
            move_temp_to_main()
            ui.show_message(f"Result:\n{result}")
            motor.buzz(duration=0.4, strength=0.7)

            # Wait until user presses click
            while True:
                next_event = buttons.wait_for_event()
                last_active = time.time()
                if next_event == "click":
                    ui.show_message("Photo Mode")
                    break
                elif not screen_on:
                    screen_on = True
                    ui.show_message(f"Result:\n{result}")

        if screen_on and (time.time() - last_active > SCREEN_TIMEOUT):
            ui.clear()
            screen_on = False
            print("[DEBUG] Screen auto-off in Photo Mode")

# ---------------- MAIN MENU ---------------- #

def main():
    buttons = InputHandler(hold_time=2.0)
    cam = Camera()
    ui = MenuUI()
    motor = Motor(pin=18)

    menu = ["Test Device", "Config Settings", "Start"]
    idx = 0
    last_active = time.time()
    screen_on = True

    print("[DEBUG] Entering main loop...")

    while True:
        if screen_on:
            ui.show_menu(menu, selected=idx)

        event = buttons.wait_for_event()
        last_active = time.time()

        if not screen_on:
            screen_on = True
            ui.show_menu(menu, selected=idx)
            continue

        if event == "click":
            idx = (idx + 1) % len(menu)
            ui.show_menu(menu, selected=idx)

        elif event == "hold":
            choice = menu[idx]
            ui.show_message(f"Selected:\n{choice}")
            time.sleep(0.5)
            if choice == "Test Device":
                test_device(ui, cam, motor)
            elif choice == "Config Settings":
                config_settings(ui, buttons, motor)
            elif choice == "Start":
                ui.show_message("System Ready")
                photo_loop(ui, buttons, cam, motor)

        if screen_on and (time.time() - last_active > SCREEN_TIMEOUT):
            ui.clear()
            screen_on = False
            print("[DEBUG] Screen auto-off in Main Menu")

if __name__ == "__main__":
    main()