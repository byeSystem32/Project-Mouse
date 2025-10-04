from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageOps

class MenuUI:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, width=128, height=32)
        self.font = ImageFont.load_default()
        self.line_height = 8
        self.max_lines = self.device.height // self.line_height
        print("[DEBUG] OLED initialized (flipped 180)")

    def clear(self):
        img = Image.new("1", (self.device.width, self.device.height))
        img = ImageOps.flip(ImageOps.mirror(img))
        self.device.display(img)

    def _render_text(self, lines):
        """Helper to render flipped bottom-right text"""
        img = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(img)

        # Shift text up by 2px so bottom isn't cut off
        offset_y = -2

        # Draw from bottom up
        for i, line in enumerate(reversed(lines[-self.max_lines:])):
            y = self.device.height - (i + 1) * self.line_height + offset_y
            bbox = draw.textbbox((0, 0), line, font=self.font)
            w = bbox[2] - bbox[0]
            x = self.device.width - w  # right aligned
            draw.text((x, y), line, font=self.font, fill=255)

        # Flip 180° before sending
        img = ImageOps.flip(ImageOps.mirror(img))
        self.device.display(img)

    def show_message(self, text):
        print(f"[DEBUG] OLED show_message: {text}")
        lines = text.split("\n")
        self._render_text(lines)

    def show_menu(self, options, selected=0):
        if not options:
            self.show_message("No options")
            return

        print(f"[DEBUG] OLED show_menu called. Options={options}, Selected={selected}")
        lines = []
        for i, option in enumerate(options):
            prefix = "> " if i == selected else "  "
            lines.append(prefix + option)

        self._render_text(lines)