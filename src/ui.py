from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

class MenuUI:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)  # I2C address may differ
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.load_default()
        self.line_height = 8  # ~8px per line with default font
        self.max_lines = self.device.height // self.line_height  # 4 lines

    def clear(self):
        img = Image.new("1", (self.device.width, self.device.height))
        self.device.display(img)

    def show_message(self, text):
        """
        Display a message, auto-wrapped into max_lines.
        """
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

        lines = text.split("\n")
        for i, line in enumerate(lines[:self.max_lines]):
            y = i * self.line_height
            draw.text((0, y), line, font=self.font, fill=255)

        self.device.display(img)

    def show_menu(self, options, selected=0):
        """
        Show a vertical menu with scroll support.
        options: list of strings
        selected: index of highlighted option
        """
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

        # Calculate which window of items to show
        if selected < self.max_lines:
            start_idx = 0
        elif selected > len(options) - self.max_lines:
            start_idx = len(options) - self.max_lines
        else:
            start_idx = selected

        visible = options[start_idx:start_idx + self.max_lines]

        for i, option in enumerate(visible):
            y = i * self.line_height
            prefix = "> " if (start_idx + i) == selected else "  "
            draw.text((0, y), prefix + option, font=self.font, fill=255)

        self.device.display(img)
