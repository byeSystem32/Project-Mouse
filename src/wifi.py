import os, json, subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WIFI_DIR = os.path.join(BASE_DIR, "../profiles/wifi_profiles")

def load_profiles():
    """Load wifi profile JSON files into a list of dicts"""
    profiles = []
    for file in os.listdir(WIFI_DIR):
        if file.endswith(".json"):
            with open(os.path.join(WIFI_DIR, file), "r") as f:
                data = json.load(f)
                profiles.append(data)
    return profiles

def connect(profile):
    """Connect to wifi using nmcli"""
    ssid = profile["ssid"]
    password = profile["password"]

    cmd = ["nmcli", "dev", "wifi", "connect", ssid, "password", password]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return result.returncode == 0, result.stderr if result.stderr else result.stdout
