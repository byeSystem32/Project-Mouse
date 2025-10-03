from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

class MenuUI:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)  # I2C default for SSD1306
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.load_default()
        self.line_height = 8  # default font is ~8px tall
        self.max_lines = self.device.height // self.line_height  # 32px / 8px = 4 lines
        print("[DEBUG] OLED initialized: 128x32")

    def clear(self):
        """Clear the OLED screen"""
        print("[DEBUG] OLED clear() called")
        img = Image.new("1", (self.device.width, self.device.height))
        self.device.display(img)

    def show_message(self, text):
        """
        Display a message on the OLED.
        Splits text into multiple lines if needed.
        """
        print(f"[DEBUG] OLED show_message: {text}")
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

        lines = text.split("\n")
        for i, line in enumerate(lines[:self.max_lines]):  # max 4 lines
            y = i * self.line_height
            draw.text((0, y), line, font=self.font, fill=255)

        self.device.display(img)

    def show_menu(self, options, selected=0):
        """
        Display a scrolling menu with selector arrow (">").
        options: list of strings
        selected: index of highlighted option
        """
        if not options:
            self.show_message("No options")
            return

        print(f"[DEBUG] OLED show_menu called. Options={options}, Selected={selected}")

        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

        # Determine the visible window of items (scrolling)
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