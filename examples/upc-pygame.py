#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import platform
import pygame
import random
from PIL import Image, ImageDraw
import upcean

# Constants
NUM_BARCODES = 12
BARCODE_SIZE = 1
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Initialize Pygame and Display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyUPC-EAN Demo - {}".format(upcean.__version__))
pygame.display.toggle_fullscreen()

# Print Version Information
print("Python Version: {}".format(platform.python_version()))
print("PyGame Version: {}".format(pygame.version.vernum))
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
    barcode_img = barcode.validate_draw_barcode()[1].convert("RGBA")
    barcode_img = barcode_img.rotate(random.randint(0, 360), Image.BICUBIC, True)
    return pygame.image.fromstring(barcode_img.tobytes(), barcode_img.size, barcode_img.mode)

def random_position():
    return pygame.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 0, 0)

# Initialize Barcodes, Images, Positions, and Directions
barcodes = [create_barcode() for _ in range(NUM_BARCODES)]
barcode_images = [generate_barcode_image(barcode) for barcode in barcodes]
positions = [random_position() for _ in range(NUM_BARCODES)]
directions = [(random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])) for _ in range(NUM_BARCODES)]

# Animation Loop
running = True
while running:
    screen.fill((0, 0, 0))
    
    for i in range(NUM_BARCODES):
        # Update Position
        pos = positions[i]
        dx, dy = directions[i]
        pos.move_ip(dx, dy)

        # Reset if barcode moves out of bounds
        if pos.left < 0 or pos.right > WIDTH or pos.top < 0 or pos.bottom > HEIGHT:
            positions[i] = random_position()
            directions[i] = (random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2]))
            barcodes[i] = create_barcode()
            barcode_images[i] = generate_barcode_image(barcodes[i])

        # Draw Barcode
        screen.blit(barcode_images[i], positions[i])

    # Refresh Screen
    pygame.display.flip()
    pygame.time.delay(10)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in {pygame.K_ESCAPE, pygame.K_q}):
            running = False
