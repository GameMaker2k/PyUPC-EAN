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

# Constants
NUM_BARCODES = 12
BARCODE_SIZE = 1
WIDTH, HEIGHT = 800, 600  # Assuming a fixed resolution for this example

# Initialize SDL2
sdl2.ext.init()
window = sdl2.ext.Window("PyUPC-EAN Demo - {}".format(upcean.__version__), size=(WIDTH, HEIGHT))
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
    barcode = upcean.oopfuncs.barcode()
    barcode_type = random.choice(["upca", "upce", "ean13", "ean8", "itf14"])
    barcode.type = barcode_type

    # Assign code based on type
    code_length = {"upca": 11, "upce": 7, "ean13": 12, "ean8": 7, "itf14": 13}[barcode_type]
    barcode.code = str(random.randint(0, 10**code_length - 1)).zfill(code_length)
    barcode.code = barcode.fix_checksum()
    return barcode

def generate_barcode_image(barcode):
    barcode.size = BARCODE_SIZE
    barcode_img = barcode.validate_draw_barcode().convert("RGBA")
    barcode_img = barcode_img.rotate(random.randint(0, 360), Image.BICUBIC, True)
    return barcode_img

def convert_pillow_to_sdl2_surface(image):
    """Converts a Pillow Image to an SDL2 Surface"""
    image_data = image.tobytes()
    surface = sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
        image_data, image.width, image.height, 32, image.width * 4, sdl2.SDL_PIXELFORMAT_RGBA32)
    return surface

def random_position():
    return [random.randint(0, WIDTH), random.randint(0, HEIGHT)]

# Initialize Barcodes, Images, Positions, and Directions
barcodes = [create_barcode() for _ in range(NUM_BARCODES)]
barcode_images = [generate_barcode_image(barcode) for barcode in barcodes]
sdl_surfaces = [convert_pillow_to_sdl2_surface(image) for image in barcode_images]
positions = [random_position() for _ in range(NUM_BARCODES)]
directions = [(random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])) for _ in range(NUM_BARCODES)]

# Renderer
renderer = sdl2.ext.Renderer(window)
running = True

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
            sdl_surfaces[i] = convert_pillow_to_sdl2_surface(barcode_images[i])

        # Convert position and draw on screen
        dst_rect = sdl2.SDL_Rect(pos[0], pos[1], barcode_images[i].width, barcode_images[i].height)
        renderer.copy(sdl_surfaces[i], None, dst_rect)

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

# Clean up and quit
for surface in sdl_surfaces:
    sdl2.SDL_FreeSurface(surface)
sdl2.ext.quit()
