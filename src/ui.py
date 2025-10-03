from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

class MenuUI:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)
        self.font = ImageFont.load_default()

    def show_message(self, text):
        """Display a message on OLED"""
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=self.font, fill=255)
        self.device.display(img)
