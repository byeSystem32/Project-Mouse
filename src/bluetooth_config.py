import subprocess, time

def run(ui, buttons):
    """
    Scan and connect to Bluetooth devices (e.g., 8BitDo).
    """
    ui.show_message("Scanning BT...")
    time.sleep(1)

    # Start scan
    scan_cmd = 'echo -e "scan on\n" | bluetoothctl'
    subprocess.Popen(scan_cmd, shell=True)

    ui.show_message("Press hold\nto stop scan")
    buttons.wait_for_event()  # user long press to stop
    subprocess.Popen('echo -e "scan off\n" | bluetoothctl', shell=True)

    # Get list of devices
    result = subprocess.run('echo -e "devices\n" | bluetoothctl', shell=True, capture_output=True, text=True)
    devices = []
    for line in result.stdout.splitlines():
        if "Device" in line:
            parts = line.split(" ", 2)
            if len(parts) >= 3:
                mac, name = parts[1], parts[2]
                devices.append((mac, name))

    if not devices:
        ui.show_message("No devices found")
        time.sleep(2)
        return

    idx = 0
    while True:
        ui.show_menu([d[1] for d in devices], selected=idx)
        event = buttons.wait_for_event()

        if event == "short_press":
            idx = (idx + 1) % len(devices)
        elif event == "long_press":
            mac, name = devices[idx]
            ui.show_message(f"Pairing:\n{name}")
            pair_cmd = f'echo -e "pair {mac}\ntrust {mac}\nconnect {mac}\n" | bluetoothctl'
            res = subprocess.run(pair_cmd, shell=True, capture_output=True, text=True)
            if "Failed" in res.stdout or "not available" in res.stdout:
                ui.show_message("Failed")
                time.sleep(2)
            else:
                ui.show_message("Connected:\n" + name)
                time.sleep(2)
                return