from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

class MenuUI:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.load_default()
        self.line_height = 8
        self.max_lines = self.device.height // self.line_height
        print("[DEBUG] OLED initialized: 128x32")

    def clear(self):
        img = Image.new("1", (self.device.width, self.device.height))
        self.device.display(img)

    def show_message(self, text):
        print(f"[DEBUG] OLED show_message: {text}")
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)
        lines = text.split("\n")
        for i, line in enumerate(lines[:self.max_lines]):
            y = i * self.line_height
            draw.text((0, y), line, font=self.font, fill=255)
        self.device.display(img)

    def show_menu(self, options, selected=0):
        if not options:
            self.show_message("No options")
            return

        print(f"[DEBUG] OLED show_menu called. Options={options}, Selected={selected}")
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

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
        print(f"[DEBUG] OLED menu rendered. Visible={visible}, Highlight={options[selected]}")