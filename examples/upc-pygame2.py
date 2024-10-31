#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import random
import pygame
from PIL import Image
import PIL
import upcean

# Constants
NUM_BARCODES = 12
BARCODE_SIZE = 1
pygame.init()

# Get desktop resolution and set up display
desktop_size = pygame.display.get_desktop_sizes()[0]
WIDTH, HEIGHT = desktop_size[0] // 2, desktop_size[1] // 2  # Half desktop size for windowed mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PyUPC-EAN Demo - {upcean.__version__}")

# Print Version Information
print("Python Version: {platform.python_version()}")
print("PyGame Version: {pygame.version.vernum}")
try:
    print("Pillow Version: {Image.PILLOW_VERSION}")
except AttributeError:
    try:
        print("Pillow Version: {Image.__version__}")
    except AttributeError:
        pass
print("PyUPC-EAN Version: {upcean.__version__}")

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
    return pygame.image.fromstring(barcode_img.tobytes(), barcode_img.size, barcode_img.mode)

def random_position():
    return [random.randint(0, WIDTH), random.randint(0, HEIGHT)]

# Initialize Barcodes, Images, Positions, and Directions
barcodes = [create_barcode() for _ in range(NUM_BARCODES)]
barcode_images = [generate_barcode_image(barcode) for barcode in barcodes]
positions = [random_position() for _ in range(NUM_BARCODES)]
directions = [(random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])) for _ in range(NUM_BARCODES)]

# Animation Loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    
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

        # Draw Barcode
        screen.blit(barcode_images[i], pos)

    # Refresh Screen
    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.quit()
