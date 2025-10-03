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

def config_settings(ui, buttons, motor, screen_on):
    config_menu = ["WiFi Config", "Bluetooth Config", "Back"]
    idx = 0

    while True:
        if screen_on:
            ui.show_menu(config_menu, selected=idx)

        event = buttons.wait_for_event()
        print(f"[DEBUG] Config menu event: {event}")

        if event == "double":
            screen_on = not screen_on
            if not screen_on:
                ui.clear()
                print("[DEBUG] Screen turned off")
            else:
                ui.show_menu(config_menu, selected=idx)
                print("[DEBUG] Screen turned on")

        elif event == "click" and screen_on:
            idx = (idx + 1) % len(config_menu)
            ui.show_menu(config_menu, selected=idx)

        elif event == "hold" and screen_on:
            choice = config_menu[idx]
            ui.show_message(f"Selected:\n{choice}")
            print(f"[DEBUG] Config menu selected: {choice}")
            time.sleep(0.5)
            if choice == "WiFi Config":
                config_wifi(ui, buttons, screen_on)
            elif choice == "Bluetooth Config":
                bluetooth_config.run(ui, buttons)
            elif choice == "Back":
                return screen_on

def config_wifi(ui, buttons, screen_on):
    profiles = wifi.load_profiles()
    if not profiles:
        if screen_on:
            ui.show_message("No wifi profiles")
        print("[WARN] No WiFi profiles found")
        time.sleep(2)
        return

    idx = 0
    while True:
        if screen_on:
            profile_names = [p["network_name"] for p in profiles]
            ui.show_menu(profile_names, selected=idx)

        event = buttons.wait_for_event()
        print(f"[DEBUG] WiFi config event: {event}")

        if event == "double":
            screen_on = not screen_on
            if not screen_on:
                ui.clear()
                print("[DEBUG] Screen turned off")
            else:
                ui.show_menu(profile_names, selected=idx)
                print("[DEBUG] Screen turned on")

        elif event == "click" and screen_on:
            idx = (idx + 1) % len(profiles)
            ui.show_menu(profile_names, selected=idx)

        elif event == "hold" and screen_on:
            chosen = profiles[idx]
            print(f"[DEBUG] Attempting WiFi connect: {chosen}")
            success, msg = wifi.connect(chosen)
            if success:
                ui.show_message(f"Connected:\n{chosen['network_name']}")
                print("[DEBUG] WiFi connected successfully")
                time.sleep(2)
                return screen_on
            else:
                ui.show_message("Failed WiFi")
                print(f"[ERROR] WiFi failed: {msg}")
                time.sleep(2)

def photo_loop(ui, buttons, cam, motor, screen_on):
    while True:
        if screen_on:
            ui.show_message("Photo Mode")

        event = buttons.wait_for_event()
        print(f"[DEBUG] Photo loop event: {event}")

        if event == "double":
            screen_on = not screen_on
            if not screen_on:
                ui.clear()
                print("[DEBUG] Screen turned off")
            else:
                ui.show_message("Photo Mode")
                print("[DEBUG] Screen turned on")

        elif event == "click" and screen_on:
            filename = cam.capture(TEMP_DIR)
            ui.show_message(f"Saved:\n{os.path.basename(filename)}")
            motor.buzz(duration=0.2, strength=0.5)  # feedback on photo
            print(f"[DEBUG] Photo saved: {filename}")

        elif event == "hold" and screen_on:
            ui.show_message("Sending...")
            print("[DEBUG] Sending photos to ChatGPT...")
            result = send_to_chatgpt(TEMP_DIR)
            move_temp_to_main()
            ui.show_message(f"Result:\n{result}")
            motor.buzz(duration=0.4, strength=0.7)  # feedback on response
            print(f"[DEBUG] ChatGPT result: {result}")

            # Wait until user clicks to continue
            while True:
                next_event = buttons.wait_for_event()
                if next_event == "click":
                    ui.show_message("Photo Mode")
                    print("[DEBUG] User acknowledged result")
                    break
                elif next_event == "double":
                    screen_on = not screen_on
                    if not screen_on:
                        ui.clear()
                        print("[DEBUG] Screen turned off (while result showing)")
                    else:
                        ui.show_message(f"Result:\n{result}")
                        print("[DEBUG] Screen turned on (showing result again)")

        # Return updated state
        return screen_on

# ---------------- MAIN MENU ---------------- #

def main():
    buttons = InputHandler(hold_time=2.0)
    cam = Camera()
    ui = MenuUI()
    motor = Motor(pin=18)

    menu = ["Test Device", "Config Settings", "Start"]
    idx = 0
    screen_on = True

    print("[DEBUG] Entering main loop...")

    while True:
        if screen_on:
            ui.show_menu(menu, selected=idx)

        event = buttons.wait_for_event()
        print(f"[DEBUG] Main menu event: {event}")

        if event == "double":
            screen_on = not screen_on
            if not screen_on:
                ui.clear()
                print("[DEBUG] Screen turned off")
            else:
                ui.show_menu(menu, selected=idx)
                print("[DEBUG] Screen turned on")

        elif event == "click" and screen_on:
            idx = (idx + 1) % len(menu)
            ui.show_menu(menu, selected=idx)
            print(f"[DEBUG] Menu index changed to {idx}")

        elif event == "hold" and screen_on:
            choice = menu[idx]
            ui.show_message(f"Selected:\n{choice}")
            print(f"[DEBUG] Menu choice selected: {choice}")
            time.sleep(0.5)
            if choice == "Test Device":
                test_device(ui, cam, motor)
            elif choice == "Config Settings":
                screen_on = config_settings(ui, buttons, motor, screen_on)
            elif choice == "Start":
                ui.show_message("System Ready")
                print("[DEBUG] Entering photo loop...")
                screen_on = photo_loop(ui, buttons, cam, motor, screen_on)

if __name__ == "__main__":
    main()