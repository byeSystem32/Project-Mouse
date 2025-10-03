from picamera2 import Picamera2
import os, datetime

class Camera:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.start()

    def capture(self, folder):
        os.makedirs(folder, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
        filename = os.path.join(folder, ts)
        self.cam.capture_file(filename)
        return filename
