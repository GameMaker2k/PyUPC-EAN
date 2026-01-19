#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import platform
import random
import sdl2
import sdl2.ext
from PIL import Image
import PIL
import upcean
import ctypes

# Constants
NUM_BARCODES = random.randint(12, 24)
BARCODE_SIZE = 1
# Initialize SDL2
sdl2.ext.init()

# Get desktop (maximum) resolution
mode = sdl2.SDL_DisplayMode()
sdl2.SDL_GetDesktopDisplayMode(0, mode)

WIDTH, HEIGHT = mode.w, mode.h

window = sdl2.ext.Window(
    "PyUPC-EAN Demo",
    flags=sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP,
    size=(WIDTH, HEIGHT)
)
window.show()

# Print Version Information
print("Python Version: {}".format(platform.python_version()))
try:
    print("Pillow Version: {}".format(Image.PILLOW_VERSION))
except AttributeError:
    try:
        print("Pillow Version: {}".format(PIL.__version__))
    except AttributeError:
        pass
print("PyUPC-EAN Version: {}".format(upcean.__version__))

# Barcode and Position Initialization Functions
def create_barcode():
    while(True):
        barcode = upcean.oopfuncs.barcode()
        barcode_type = random.choice(["upca", "upce", "ean13", "ean8", "itf14"])
        barcode.type = barcode_type
        # Assign code based on type
        code_length = {"upca": 11, "upce": 7, "ean13": 12, "ean8": 7, "itf14": 13}[barcode_type]
        barcode.code = str(random.randint(0, 10**code_length - 1)).zfill(code_length)
        if(barcode.validate_checksum()):
            break;
    barcode.code = barcode.fix_checksum()
    return barcode

def generate_barcode_image(barcode):
    barcode.size = BARCODE_SIZE
    barcode_img = barcode.validate_draw_barcode()[1].convert("RGBA")
    barcode_img = barcode_img.rotate(random.randint(0, 360), Image.BICUBIC, True)
    return barcode_img

def pillow_to_sdl_texture(renderer: sdl2.ext.Renderer, pil_img):
    img = pil_img.convert("RGBA")
    w, h = img.size
    pitch = w * 4

    buf = ctypes.create_string_buffer(img.tobytes())
    surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
        buf, w, h, 32, pitch, sdl2.SDL_PIXELFORMAT_RGBA32
    )
    if not surface:
        raise RuntimeError(sdl2.SDL_GetError().decode())

    # NOTE: Texture wants (renderer, surface)
    tex = sdl2.ext.Texture(renderer, surface)

    sdl2.SDL_FreeSurface(surface)
    return tex

def random_position():
    return [random.randint(0, WIDTH), random.randint(0, HEIGHT)]

# Renderer
renderer = sdl2.ext.Renderer(window)
running = True

# Initialize Barcodes, Images, Positions, and Directions
barcodes = [create_barcode() for _ in range(NUM_BARCODES)]
barcode_images = [generate_barcode_image(barcode) for barcode in barcodes]
sdl_textures = [pillow_to_sdl_texture(renderer, image) for image in barcode_images]
positions = [random_position() for _ in range(NUM_BARCODES)]
directions = [(random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])) for _ in range(NUM_BARCODES)]

# Animation Loop
while running:
    renderer.clear(0)  # Clear with black background

    # Update and Draw Barcodes
    for i in range(NUM_BARCODES):
        # Update Position
        pos = positions[i]
        dx, dy = directions[i]
        pos[0] += dx
        pos[1] += dy

        # Reset if barcode moves out of bounds
        if pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
            positions[i] = random_position()
            directions[i] = (random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2]))
            barcodes[i] = create_barcode()
            barcode_images[i] = generate_barcode_image(barcodes[i])
            sdl_textures[i] = pillow_to_sdl_texture(renderer, barcode_images[i])

        # Convert position and draw on screen
        dst_rect = sdl2.SDL_Rect(pos[0], pos[1], barcode_images[i].width, barcode_images[i].height)
        renderer.copy(sdl_textures[i], None, dst_rect)

    # Present the renderer
    renderer.present()
    sdl2.SDL_Delay(10)  # Delay for smooth animation

    # Event Handling
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym in {sdl2.SDLK_ESCAPE, sdl2.SDLK_q}:
                running = False

sdl2.ext.quit()
