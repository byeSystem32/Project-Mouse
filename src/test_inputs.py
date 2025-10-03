from input_handler import InputHandler
from ui import MenuUI

def main():
    ui = MenuUI()
    inputs = InputHandler(hold_time=1.5, button_pin=17)

    ui.show_message("Ready...\nPress a button")

    while True:
        event = inputs.wait_for_event()
        print(f"[DEBUG] Got event: {event}")
        ui.show_message(f"Event:\n{event}")

if __name__ == "__main__":
    main()