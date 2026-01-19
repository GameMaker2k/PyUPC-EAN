#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# IMPORTANT: Config must be set BEFORE importing Window (or any other Kivy modules that touch the window).
from kivy.config import Config

# True fullscreen at the desktop's native resolution (like your other demos)
Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "resizable", "0")
Config.set("graphics", "borderless", "0")

import random
import upcean
from PIL import Image

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget


def create_barcode():
    """Create a random barcode object with a valid checksum."""
    while True:
        b = upcean.oopfuncs.barcode()
        btype = random.choice(["upca", "upce", "ean13", "ean8", "itf14"])
        b.type = btype
        code_length = {"upca": 11, "upce": 7, "ean13": 12, "ean8": 7, "itf14": 13}[btype]
        b.code = str(random.randint(0, 10**code_length - 1)).zfill(code_length)
        if b.validate_checksum():
            break
    b.code = b.fix_checksum()
    return b


def pil_to_kivy_texture(pil_img: Image.Image) -> Texture:
    """Convert a Pillow RGBA image to a Kivy Texture."""
    img = pil_img.convert("RGBA")
    w, h = img.size
    tex = Texture.create(size=(w, h), colorfmt="rgba")
    tex.blit_buffer(img.tobytes(), colorfmt="rgba", bufferfmt="ubyte")
    tex.flip_vertical()  # Pillow top-left -> Kivy bottom-left
    return tex


def generate_barcode_texture(barcode, barcode_size=1) -> tuple[Texture, int, int]:
    """Draw barcode with upcean -> Pillow image, rotate, convert to Kivy texture."""
    barcode.size = barcode_size
    pil_img = barcode.validate_draw_barcode()[1].convert("RGBA")
    pil_img = pil_img.rotate(random.randint(0, 360), resample=Image.BICUBIC, expand=True)
    tex = pil_to_kivy_texture(pil_img)
    return tex, pil_img.size[0], pil_img.size[1]


class FlyingBarcode:
    """A lightweight "sprite" backed by a Kivy Rectangle."""

    def __init__(self, canvas, width, height, barcode_size=1):
        self.canvas = canvas
        self.barcode_size = barcode_size
        self.reset(width, height, first_time=True)

    def reset(self, width, height, first_time=False):
        self.barcode = create_barcode()
        self.texture, self.w, self.h = generate_barcode_texture(self.barcode, self.barcode_size)

        self.x = random.randint(0, max(0, width - 1))
        self.y = random.randint(0, max(0, height - 1))

        # Velocity (avoid 0,0)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

        if first_time:
            with self.canvas:
                Color(1, 1, 1, 1)  # keep barcode colors as-is
                self.rect = Rectangle(texture=self.texture, pos=(self.x, self.y), size=(self.w, self.h))
        else:
            self.rect.texture = self.texture
            self.rect.size = (self.w, self.h)
            self.rect.pos = (self.x, self.y)

    def update(self, dt, width, height):
        self.x += self.vx
        self.y += self.vy

        # If fully off-screen, respawn with a new random barcode
        if (self.x + self.w) < 0 or self.x > width or (self.y + self.h) < 0 or self.y > height:
            self.reset(width, height)
            return

        self.rect.pos = (self.x, self.y)


class BarcodeWorld(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # This is the actual fullscreen window size (desktop resolution when fullscreen='auto')
        w, h = Window.size

        self.num_barcodes = random.randint(12, 24)
        self.barcode_size = 1
        self.barcodes: list[FlyingBarcode] = []

        # Black background
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=(0, 0), size=(w, h))

        # Create barcode rectangles
        for _ in range(self.num_barcodes):
            self.barcodes.append(FlyingBarcode(self.canvas, w, h, self.barcode_size))

        Window.bind(on_resize=self._on_resize)
        Window.bind(on_key_down=self._on_key_down)

        Clock.schedule_interval(self._tick, 1.0 / 60.0)

    def _on_resize(self, window, w, h):
        self.bg.size = (w, h)

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        # ESC or 'q' quits (like your pygame versions)
        if key == 27 or (codepoint and codepoint.lower() == "q"):
            App.get_running_app().stop()
            return True
        return False

    def _tick(self, dt):
        w, h = Window.size
        for b in self.barcodes:
            b.update(dt, w, h)


class BarcodeFlybyApp(App):
    def build(self):
        self.title = f"PyUPC-EAN Demo - {getattr(upcean, '__version__', '')}"
        return BarcodeWorld()


if __name__ == "__main__":
    BarcodeFlybyApp().run()
