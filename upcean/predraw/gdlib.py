# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: predraw.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
import sys
import math

try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

# Compatibility between Python 2 and 3
if sys.version_info[0] >= 3:
    xrange = range
    basestring = str
else:
    pass

class ImageResource:
    def __init__(self, image):
        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.colors = {}
        self.next_color_index = 1  # Start from 1 to match GD behavior
        self.brush = None
        self.tile = None
        self.style = None
        self.clip = None
        self.interpolation = Image.NEAREST
        self.antialias = False
        self.thickness = 1
        self.alpha_blending = True
        self.save_alpha = False

    def get_color(self, color_index):
        return self.colors.get(color_index, (0, 0, 0, 255))

    def set_brush(self, brush_image):
        self.brush = brush_image

    def set_tile(self, tile_image):
        self.tile = tile_image

    def set_style(self, style):
        self.style = style

    def set_clip(self, clip_rect):
        self.clip = clip_rect

    def set_interpolation(self, method):
        self.interpolation = method

# Constants for filters
IMG_FILTER_NEGATE = 'IMG_FILTER_NEGATE'
IMG_FILTER_GRAYSCALE = 'IMG_FILTER_GRAYSCALE'
IMG_FILTER_BRIGHTNESS = 'IMG_FILTER_BRIGHTNESS'
IMG_FILTER_CONTRAST = 'IMG_FILTER_CONTRAST'
IMG_FILTER_COLORIZE = 'IMG_FILTER_COLORIZE'
IMG_FILTER_EDGEDETECT = 'IMG_FILTER_EDGEDETECT'
IMG_FILTER_GAUSSIAN_BLUR = 'IMG_FILTER_GAUSSIAN_BLUR'
IMG_FILTER_SELECTIVE_BLUR = 'IMG_FILTER_SELECTIVE_BLUR'
IMG_FILTER_EMBOSS = 'IMG_FILTER_EMBOSS'
IMG_FILTER_MEAN_REMOVAL = 'IMG_FILTER_MEAN_REMOVAL'
IMG_FILTER_SMOOTH = 'IMG_FILTER_SMOOTH'

# Constants for flip modes
IMG_FLIP_HORIZONTAL = 'horizontal'
IMG_FLIP_VERTICAL = 'vertical'
IMG_FLIP_BOTH = 'both'

# Constants for affine transformations
IMG_AFFINE_TRANSLATE = 0
IMG_AFFINE_SCALE = 1
IMG_AFFINE_ROTATE = 2
IMG_AFFINE_SHEAR_HORIZONTAL = 3
IMG_AFFINE_SHEAR_VERTICAL = 4

def gd_info():
    """
    Retrieve information about the currently installed GD library.
    """
    return {
        'GD Version': 'Pillow ' + Image.__version__,
        'FreeType Support': 'Yes' if 'freetype2' in Image.core.__dict__ else 'No',
        'GIF Read Support': 'Yes' if 'gif' in Image.OPEN else 'No',
        'GIF Create Support': 'Yes' if 'gif' in Image.SAVE else 'No',
        'JPEG Support': 'Yes' if 'jpeg' in Image.OPEN else 'No',
        'PNG Support': 'Yes' if 'png' in Image.OPEN else 'No',
        'WBMP Support': 'Yes' if 'wbmp' in Image.OPEN else 'No',
        'XPM Support': 'No',  # Pillow does not support XPM
        'XBM Support': 'Yes' if 'xbm' in Image.OPEN else 'No',
        'WebP Support': 'Yes' if 'webp' in Image.OPEN else 'No',
    }

def getimagesize(filename):
    """
    Get the size of an image.
    """
    with Image.open(filename) as img:
        return img.size + (img.format, img.mode)

def getimagesizefromstring(image_data):
    """
    Get the size of an image from a string.
    """
    from io import BytesIO
    img = Image.open(BytesIO(image_data))
    return img.size + (img.format, img.mode)

def image_type_to_extension(image_type, include_dot=True):
    """
    Get file extension for image type.
    """
    extensions = {
        'JPEG': 'jpeg',
        'PNG': 'png',
        'GIF': 'gif',
        'BMP': 'bmp',
        'TIFF': 'tiff',
        'ICO': 'ico',
        'WEBP': 'webp',
    }
    ext = extensions.get(image_type.upper(), '')
    return ('.' if include_dot else '') + ext

def image_type_to_mime_type(image_type):
    """
    Get Mime-Type for image-type.
    """
    mime_types = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
        'BMP': 'image/bmp',
        'TIFF': 'image/tiff',
        'ICO': 'image/vnd.microsoft.icon',
        'WEBP': 'image/webp',
    }
    return mime_types.get(image_type.upper(), 'application/octet-stream')

def image2wbmp(image_res, filename=None, threshold=0):
    """
    Output image to WBMP format.
    """
    if threshold:
        image_res.image = image_res.image.convert('L').point(lambda x: 255 if x > threshold else 0, '1')
    else:
        image_res.image = image_res.image.convert('1')
    if filename:
        image_res.image.save(filename, 'WBMP')
    else:
        image_res.image.save(sys.stdout, 'WBMP')

def imageaffine(image_res, matrix, options=None):
    """
    Return an image containing the affine transformed src image.
    """
    m = (matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5])
    transformed_image = image_res.image.transform(image_res.image.size, Image.AFFINE, m)
    return ImageResource(transformed_image)

def imageaffinematrixconcat(matrix1, matrix2):
    """
    Concatenate two affine transformation matrices.
    """
    # Multiply matrices
    a = matrix1[0]*matrix2[0] + matrix1[1]*matrix2[3]
    b = matrix1[0]*matrix2[1] + matrix1[1]*matrix2[4]
    c = matrix1[0]*matrix2[2] + matrix1[1]*matrix2[5] + matrix1[2]
    d = matrix1[3]*matrix2[0] + matrix1[4]*matrix2[3]
    e = matrix1[3]*matrix2[1] + matrix1[4]*matrix2[4]
    f = matrix1[3]*matrix2[2] + matrix1[4]*matrix2[5] + matrix1[5]
    return [a, b, c, d, e, f]

def imageaffinematrixget(type, options):
    """
    Get an affine transformation matrix.
    """
    if type == IMG_AFFINE_TRANSLATE:
        return [1, 0, options.get('x', 0), 0, 1, options.get('y', 0)]
    elif type == IMG_AFFINE_SCALE:
        return [options.get('x', 1), 0, 0, 0, options.get('y', 1), 0]
    elif type == IMG_AFFINE_ROTATE:
        angle = math.radians(options)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [cos_a, sin_a, 0, -sin_a, cos_a, 0]
    elif type == IMG_AFFINE_SHEAR_HORIZONTAL:
        return [1, options, 0, 0, 1, 0]
    elif type == IMG_AFFINE_SHEAR_VERTICAL:
        return [1, 0, 0, options, 1, 0]
    else:
        return [1, 0, 0, 0, 1, 0]

def imagealphablending(image_res, blendmode):
    """
    Set the blending mode for an image.
    """
    image_res.alpha_blending = blendmode

def imageantialias(image_res, on):
    """
    Should antialias functions be used or not.
    """
    image_res.antialias = on

def imagearc(image_res, cx, cy, width, height, start, end, color_index):
    """
    Draws an arc.
    """
    color = image_res.get_color(color_index)
    bbox = [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2]
    image_res.draw.arc(bbox, start, end, fill=color, width=image_res.thickness)

def imageavif(image_res, filename=None):
    """
    Output image to AVIF format.
    """
    if filename:
        image_res.image.save(filename, 'AVIF')
    else:
        image_res.image.save(sys.stdout, 'AVIF')

def imagebmp(image_res, filename=None, compressed=True):
    """
    Output a BMP image to browser or file.
    """
    if filename:
        image_res.image.save(filename, 'BMP', compress_level=int(compressed))
    else:
        image_res.image.save(sys.stdout, 'BMP', compress_level=int(compressed))

def imagechar(image_res, font, x, y, c, color_index):
    """
    Draw a character horizontally.
    """
    color = image_res.get_color(color_index)
    font_obj = ImageFont.load_default()
    image_res.draw.text((x, y), c, font=font_obj, fill=color)

def imagecharup(image_res, font, x, y, c, color_index):
    """
    Draw a character vertically.
    """
    color = image_res.get_color(color_index)
    font_obj = ImageFont.load_default()
    char_image = Image.new('RGBA', font_obj.getsize(c))
    char_draw = ImageDraw.Draw(char_image)
    char_draw.text((0, 0), c, font=font_obj, fill=color)
    rotated_char = char_image.rotate(90, expand=1)
    image_res.image.paste(rotated_char, (x, y), rotated_char)

def imagecolorallocate(image_res, red, green, blue):
    """
    Allocate a color for an image.
    """
    color = (red, green, blue, 255)  # Default alpha is 255 (opaque)
    color_index = image_res.next_color_index
    image_res.colors[color_index] = color
    image_res.next_color_index += 1
    return color_index

def imagecolorallocatealpha(image_res, red, green, blue, alpha):
    """
    Allocate a color with alpha transparency.
    """
    # Alpha in GD is 0-127 (0 opaque, 127 transparent), in Pillow it's 0-255 (0 transparent, 255 opaque)
    alpha = int(255 - (alpha / 127.0) * 255)
    color = (red, green, blue, alpha)
    color_index = image_res.next_color_index
    image_res.colors[color_index] = color
    image_res.next_color_index += 1
    return color_index

def imagecolorat(image_res, x, y):
    """
    Get the color index of a pixel.
    """
    pixel = image_res.image.getpixel((x, y))
    for idx, color in image_res.colors.items():
        if color == pixel:
            return idx
    # If color not found, allocate it
    return imagecolorallocate(image_res, *pixel[:3])

def imagecolorclosest(image_res, red, green, blue):
    """
    Get the index of the closest color to the specified color.
    """
    min_distance = None
    closest_index = None
    for idx, color in image_res.colors.items():
        distance = ((color[0]-red)**2 + (color[1]-green)**2 + (color[2]-blue)**2)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_index = idx
    return closest_index

def imagecolorclosestalpha(image_res, red, green, blue, alpha):
    """
    Get the index of the closest color to the specified color + alpha.
    """
    min_distance = None
    closest_index = None
    for idx, color in image_res.colors.items():
        distance = ((color[0]-red)**2 + (color[1]-green)**2 +
                    (color[2]-blue)**2 + (color[3]-alpha)**2)
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_index = idx
    return closest_index

def imagecolordeallocate(image_res, color_index):
    """
    De-allocate a color for an image.
    """
    if color_index in image_res.colors:
        del image_res.colors[color_index]

def imagecolorexact(image_res, red, green, blue):
    """
    Get the index of the specified color.
    """
    for idx, color in image_res.colors.items():
        if color[:3] == (red, green, blue):
            return idx
    return -1  # No exact match

def imagecolorexactalpha(image_res, red, green, blue, alpha):
    """
    Get the index of the specified color + alpha.
    """
    for idx, color in image_res.colors.items():
        if color == (red, green, blue, alpha):
            return idx
    return -1  # No exact match

def imagecolorresolve(image_res, red, green, blue):
    """
    Get the index of the specified color or its closest possible alternative.
    """
    idx = imagecolorexact(image_res, red, green, blue)
    if idx != -1:
        return idx
    return imagecolorallocate(image_res, red, green, blue)

def imagecolorresolvealpha(image_res, red, green, blue, alpha):
    """
    Get the index of the specified color + alpha or its closest possible alternative.
    """
    idx = imagecolorexactalpha(image_res, red, green, blue, alpha)
    if idx != -1:
        return idx
    return imagecolorallocatealpha(image_res, red, green, blue, alpha)

def imagecolorset(image_res, index, red, green, blue, alpha=255):
    """
    Set the color for the specified palette index.
    """
    color = (red, green, blue, alpha)
    image_res.colors[index] = color

def imagecolorsforindex(image_res, index):
    """
    Get the colors for an index.
    """
    return image_res.colors.get(index, None)

def imagecolorstotal(image_res):
    """
    Find out the number of colors in an image's palette.
    """
    return len(image_res.colors)

def imagecolortransparent(image_res, color_index):
    """
    Define a color as transparent.
    """
    transparent_color = image_res.get_color(color_index)
    image_res.image.info['transparency'] = transparent_color

def imageconvolution(image_res, matrix, div, offset):
    """
    Apply a 3x3 convolution matrix, using coefficient and offset.
    """
    kernel = [item for sublist in matrix for item in sublist]
    kernel = [float(k) / div for k in kernel]
    image_res.image = image_res.image.filter(ImageFilter.Kernel((3, 3), kernel, scale=1, offset=offset))

def imagecopy(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h):
    """
    Copy part of an image.
    """
    box = (src_x, src_y, src_x + src_w, src_y + src_h)
    region = image_res_src.image.crop(box)
    image_res_dst.image.paste(region, (dst_x, dst_y))

def imagecopymerge(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h, pct):
    """
    Copy and merge part of an image.
    """
    box = (src_x, src_y, src_x + src_w, src_y + src_h)
    region = image_res_src.image.crop(box).convert('RGBA')
    alpha = int(255 * (pct / 100.0))
    mask = Image.new('L', region.size, alpha)
    image_res_dst.image.paste(region, (dst_x, dst_y), mask)

def imagecopymergegray(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h, pct):
    """
    Copy and merge part of an image with gray scale.
    """
    box = (src_x, src_y, src_x + src_w, src_y + src_h)
    region = image_res_src.image.crop(box).convert('L').convert('RGBA')
    alpha = int(255 * (pct / 100.0))
    mask = Image.new('L', region.size, alpha)
    image_res_dst.image.paste(region, (dst_x, dst_y), mask)

def imagecopyresized(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h):
    """
    Copy and resize part of an image.
    """
    box = (src_x, src_y, src_x + src_w, src_y + src_h)
    region = image_res_src.image.crop(box)
    region = region.resize((dst_w, dst_h), resample=Image.NEAREST)
    image_res_dst.image.paste(region, (dst_x, dst_y))

def imagecopyresampled(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h):
    """
    Copy and resize part of an image with resampling.
    """
    box = (src_x, src_y, src_x + src_w, src_y + src_h)
    region = image_res_src.image.crop(box)
    region = region.resize((dst_w, dst_h), resample=Image.ANTIALIAS)
    image_res_dst.image.paste(region, (dst_x, dst_y))

def imagecreate(width, height):
    """
    Create a new palette-based image.
    """
    im = Image.new("P", (width, height))
    return ImageResource(im)

def imagecreatetruecolor(width, height):
    """
    Create a new true color image.
    """
    im = Image.new("RGBA", (width, height))
    return ImageResource(im)

def imagecreatefromstring(image_data):
    """
    Create a new image from the image stream in the string.
    """
    from io import BytesIO
    im = Image.open(BytesIO(image_data))
    return ImageResource(im)

def imagecreatefromjpeg(filename):
    """
    Create a new image from a JPEG file.
    """
    im = Image.open(filename)
    return ImageResource(im.convert('RGB'))

def imagecreatefrompng(filename):
    """
    Create a new image from a PNG file.
    """
    im = Image.open(filename)
    return ImageResource(im.convert('RGBA'))

def imagecreatefromgif(filename):
    """
    Create a new image from a GIF file.
    """
    im = Image.open(filename)
    return ImageResource(im.convert('P'))

def imagecreatefromavif(filename):
    """
    Create a new image from an AVIF file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecreatefrombmp(filename):
    """
    Create a new image from a BMP file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecreatefromtga(filename):
    """
    Create a new image from a TGA file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecreatefromwbmp(filename):
    """
    Create a new image from a WBMP file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecreatefromwebp(filename):
    """
    Create a new image from a WebP file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecreatefromxbm(filename):
    """
    Create a new image from an XBM file.
    """
    im = Image.open(filename)
    return ImageResource(im)

def imagecrop(image_res, rect):
    """
    Crop an image to the given rectangle.
    """
    left = rect['x']
    upper = rect['y']
    right = left + rect['width']
    lower = upper + rect['height']
    cropped_image = image_res.image.crop((left, upper, right, lower))
    return ImageResource(cropped_image)

def imagecropauto(image_res, mode=0, threshold=0.5, color=None):
    """
    Crop an image automatically.
    """
    bbox = image_res.image.getbbox()
    if bbox:
        cropped_image = image_res.image.crop(bbox)
        return ImageResource(cropped_image)
    else:
        return image_res

def imagedashedline(image_res, x1, y1, x2, y2, color_index):
    """
    Draw a dashed line.
    """
    color = image_res.get_color(color_index)
    # Dashed line implementation
    total_length = math.hypot(x2 - x1, y2 - y1)
    dash_length = 5
    gap_length = 5
    dashes = int(total_length / (dash_length + gap_length))
    for i in range(dashes):
        start_ratio = (i * (dash_length + gap_length)) / total_length
        end_ratio = ((i * (dash_length + gap_length)) + dash_length) / total_length
        start_x = x1 + (x2 - x1) * start_ratio
        start_y = y1 + (y2 - y1) * start_ratio
        end_x = x1 + (x2 - x1) * end_ratio
        end_y = y1 + (y2 - y1) * end_ratio
        image_res.draw.line((start_x, start_y, end_x, end_y), fill=color, width=image_res.thickness)

def imagedestroy(image_res):
    """
    Destroy an image.
    """
    del image_res.image
    del image_res.draw
    image_res.colors.clear()

def imageellipse(image_res, cx, cy, width, height, color_index):
    """
    Draw an ellipse.
    """
    color = image_res.get_color(color_index)
    bbox = [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2]
    image_res.draw.ellipse(bbox, outline=color, width=image_res.thickness)

def imagefilledarc(image_res, cx, cy, width, height, start, end, color_index, style=None):
    """
    Draw a partial arc and fill it.
    """
    color = image_res.get_color(color_index)
    bbox = [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2]
    image_res.draw.pieslice(bbox, start, end, fill=color)

def imagefilledellipse(image_res, cx, cy, width, height, color_index):
    """
    Draw a filled ellipse.
    """
    color = image_res.get_color(color_index)
    bbox = [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2]
    image_res.draw.ellipse(bbox, fill=color)

def imagefilledrectangle(image_res, x1, y1, x2, y2, color_index):
    """
    Draw a filled rectangle.
    """
    color = image_res.get_color(color_index)
    image_res.draw.rectangle([x1, y1, x2, y2], fill=color)

def imagefill(image_res, x, y, color_index):
    """
    Flood fill.
    """
    color = image_res.get_color(color_index)
    ImageDraw.floodfill(image_res.image, (x, y), color)

def imagefilltoborder(image_res, x, y, border_color_index, color_index):
    """
    Flood fill to specific color.
    """
    border_color = image_res.get_color(border_color_index)
    fill_color = image_res.get_color(color_index)
    ImageDraw.floodfill(image_res.image, (x, y), fill_color, border=border_color)

def imagefilter(image_res, filtertype, *args):
    """
    Applies a filter to an image.
    """
    if filtertype == IMG_FILTER_NEGATE:
        image_res.image = ImageOps.invert(image_res.image)
    elif filtertype == IMG_FILTER_GRAYSCALE:
        image_res.image = ImageOps.grayscale(image_res.image)
    elif filtertype == IMG_FILTER_BRIGHTNESS:
        enhancer = ImageEnhance.Brightness(image_res.image)
        image_res.image = enhancer.enhance(args[0])
    elif filtertype == IMG_FILTER_CONTRAST:
        enhancer = ImageEnhance.Contrast(image_res.image)
        image_res.image = enhancer.enhance(args[0])
    elif filtertype == IMG_FILTER_COLORIZE:
        r, g, b, a = args
        overlay = Image.new('RGBA', image_res.image.size, (r, g, b, a))
        image_res.image = Image.alpha_composite(image_res.image.convert('RGBA'), overlay)
    elif filtertype == IMG_FILTER_EDGEDETECT:
        image_res.image = image_res.image.filter(ImageFilter.FIND_EDGES)
    elif filtertype == IMG_FILTER_GAUSSIAN_BLUR:
        image_res.image = image_res.image.filter(ImageFilter.GaussianBlur(radius=1))
    elif filtertype == IMG_FILTER_SELECTIVE_BLUR:
        image_res.image = image_res.image.filter(ImageFilter.BLUR)
    elif filtertype == IMG_FILTER_EMBOSS:
        image_res.image = image_res.image.filter(ImageFilter.EMBOSS)
    elif filtertype == IMG_FILTER_MEAN_REMOVAL:
        image_res.image = image_res.image.filter(ImageFilter.MedianFilter(size=3))
    elif filtertype == IMG_FILTER_SMOOTH:
        image_res.image = image_res.image.filter(ImageFilter.SMOOTH_MORE)
    else:
        pass  # Unsupported filter

def imageflip(image_res, mode):
    """
    Flips an image using a given mode.
    """
    if mode == IMG_FLIP_VERTICAL:
        image_res.image = image_res.image.transpose(Image.FLIP_TOP_BOTTOM)
    elif mode == IMG_FLIP_HORIZONTAL:
        image_res.image = image_res.image.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == IMG_FLIP_BOTH:
        image_res.image = image_res.image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)

def imagefontheight(font):
    """
    Get font height.
    """
    font_obj = ImageFont.load_default()
    return font_obj.getsize('M')[1]

def imagefontwidth(font):
    """
    Get font width.
    """
    font_obj = ImageFont.load_default()
    return font_obj.getsize('M')[0]

def imageftbbox(size, angle, fontfile, text):
    """
    Give the bounding box of a text using fonts via freetype2.
    """
    font = ImageFont.truetype(fontfile, size)
    return font.getbbox(text)

def imagefttext(image_res, size, angle, x, y, color_index, fontfile, text, extra_info=None):
    """
    Write text to the image using fonts using FreeType 2.
    """
    color = image_res.get_color(color_index)
    font = ImageFont.truetype(fontfile, size)
    if angle == 0:
        image_res.draw.text((x, y), text, font=font, fill=color)
    else:
        text_image = Image.new('RGBA', image_res.image.size)
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), text, font=font, fill=color)
        rotated = text_image.rotate(angle, expand=1)
        image_res.image.paste(rotated, (x, y), rotated)

def imagegammacorrect(image_res, inputgamma, outputgamma):
    """
    Apply a gamma correction to an image.
    """
    gamma = outputgamma / inputgamma
    image_res.image = ImageOps.gamma(image_res.image, gamma)

def imagegd(image_res, filename=None):
    """
    Output GD image to browser or file.
    """
    raise NotImplementedError("GD format is not supported by Pillow.")

def imagegd2(image_res, filename=None):
    """
    Output GD2 image to browser or file.
    """
    raise NotImplementedError("GD2 format is not supported by Pillow.")

def imagegetclip(image_res):
    """
    Get the clipping rectangle.
    """
    return image_res.clip

def imagegetinterpolation(image_res):
    """
    Get the interpolation method.
    """
    return image_res.interpolation

def imagegif(image_res, filename=None):
    """
    Output image to browser or file in GIF format.
    """
    if filename:
        image_res.image.save(filename, 'GIF')
    else:
        image_res.image.save(sys.stdout, 'GIF')

def imageinterlace(image_res, interlace):
    """
    Enable or disable interlace.
    """
    image_res.image.info['interlace'] = interlace

def imageistruecolor(image_res):
    """
    Finds whether an image is a truecolor image.
    """
    return image_res.image.mode in ('RGB', 'RGBA')

def imagelayereffect(image_res, effect):
    """
    Set the alpha blending flag to use layering effects.
    """
    image_res.alpha_blending = effect

def imageline(image_res, x1, y1, x2, y2, color_index):
    """
    Draw a line.
    """
    color = image_res.get_color(color_index)
    image_res.draw.line((x1, y1, x2, y2), fill=color, width=image_res.thickness)

def imageloadfont(file):
    """
    Load a new font.
    """
    try:
        font = ImageFont.load(file)
    except IOError:
        font = ImageFont.load_default()
    return font

def imageopenpolygon(image_res, points, num_points, color_index):
    """
    Draws an open polygon.
    """
    color = image_res.get_color(color_index)
    for i in range(num_points - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        image_res.draw.line((x1, y1, x2, y2), fill=color, width=image_res.thickness)

def imagepalettecopy(destination, source):
    """
    Copy the palette from one image to another.
    """
    if source.image.mode == 'P' and destination.image.mode == 'P':
        destination.image.putpalette(source.image.getpalette())

def imagepalettetotruecolor(image_res):
    """
    Converts a palette-based image to true color.
    """
    image_res.image = image_res.image.convert('RGBA')

def imagepng(image_res, filename=None):
    """
    Output a PNG image to either the browser or a file.
    """
    if filename:
        image_res.image.save(filename, "PNG")
    else:
        image_res.image.save(sys.stdout, "PNG")

def imagepolygon(image_res, points, num_points, color_index):
    """
    Draws a polygon.
    """
    color = image_res.get_color(color_index)
    image_res.draw.polygon(points, outline=color)

def imagerectangle(image_res, x1, y1, x2, y2, color_index):
    """
    Draw a rectangle.
    """
    color = image_res.get_color(color_index)
    image_res.draw.rectangle([x1, y1, x2, y2], outline=color, width=image_res.thickness)

def imageresolution(image_res, res_x=None, res_y=None):
    """
    Get or set the resolution of the image.
    """
    if res_x is None and res_y is None:
        return image_res.image.info.get('dpi', (72, 72))
    else:
        image_res.image.info['dpi'] = (res_x, res_y)
        return True

def imagerotate(image_res, angle, bgd_color_index=0):
    """
    Rotate an image with a given angle.
    """
    bgd_color = image_res.get_color(bgd_color_index)
    image_res.image = image_res.image.rotate(angle, expand=1, fillcolor=bgd_color)
    image_res.draw = ImageDraw.Draw(image_res.image)

def imagesavealpha(image_res, saveflag):
    """
    Whether to retain full alpha channel information when saving images.
    """
    image_res.save_alpha = saveflag

def imagescale(image_res, new_width, new_height=None, mode=Image.NEAREST):
    """
    Scale an image using the given new width and height.
    """
    if new_height is None:
        width_percent = (new_width / float(image_res.image.size[0]))
        new_height = int((float(image_res.image.size[1]) * float(width_percent)))
    image_res.image = image_res.image.resize((new_width, new_height), resample=mode)
    image_res.draw = ImageDraw.Draw(image_res.image)
    return image_res

def imagesetbrush(image_res, brush):
    """
    Set the brush image for line drawing.
    """
    image_res.set_brush(brush)

def imagesetclip(image_res, x1, y1, x2, y2):
    """
    Set the clipping rectangle.
    """
    image_res.set_clip((x1, y1, x2, y2))

def imagesetinterpolation(image_res, method):
    """
    Set the interpolation method.
    """
    image_res.set_interpolation(method)

def imagesetpixel(image_res, x, y, color_index):
    """
    Set a single pixel.
    """
    color = image_res.get_color(color_index)
    image_res.image.putpixel((x, y), color)

def imagesetstyle(image_res, style):
    """
    Set the style for line drawing.
    """
    image_res.set_style(style)

def imagesetthickness(image_res, thickness):
    """
    Set the thickness for line drawing.
    """
    image_res.thickness = thickness

def imagesettile(image_res, tile):
    """
    Set the tile image for filling.
    """
    image_res.set_tile(tile)

def imagestring(image_res, font, x, y, string, color_index):
    """
    Draw a string horizontally.
    """
    color = image_res.get_color(color_index)
    font_obj = ImageFont.load_default()
    image_res.draw.text((x, y), string, font=font_obj, fill=color)

def imagestringup(image_res, font, x, y, string, color_index):
    """
    Draw a string vertically.
    """
    color = image_res.get_color(color_index)
    font_obj = ImageFont.load_default()
    text_image = Image.new('RGBA', font_obj.getsize(string))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), string, font=font_obj, fill=color)
    rotated_text = text_image.rotate(90, expand=1)
    image_res.image.paste(rotated_text, (x, y), rotated_text)

def imagesx(image_res):
    """
    Get image width.
    """
    return image_res.image.width

def imagesy(image_res):
    """
    Get image height.
    """
    return image_res.image.height

def imagetruecolortopalette(image_res, dither, ncolors):
    """
    Convert a true color image to a palette image.
    """
    image_res.image = image_res.image.convert('P', palette=Image.ADAPTIVE, colors=ncolors)

def imagettfbbox(size, angle, fontfile, text):
    """
    Give the bounding box of a text using TrueType fonts.
    """
    font = ImageFont.truetype(fontfile, size)
    return font.getbbox(text)

def imagettftext(image_res, size, angle, x, y, color_index, fontfile, text):
    """
    Write text to the image using TrueType fonts.
    """
    color = image_res.get_color(color_index)
    font = ImageFont.truetype(fontfile, size)
    if angle == 0:
        image_res.draw.text((x, y), text, font=font, fill=color)
    else:
        text_image = Image.new('RGBA', image_res.image.size)
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), text, font=font, fill=color)
        rotated = text_image.rotate(angle, expand=1)
        image_res.image.paste(rotated, (x, y), rotated)

def imagetypes():
    """
    Return the image types supported.
    """
    supported = 0
    if 'gif' in Image.OPEN:
        supported |= 1  # IMG_GIF
    if 'jpeg' in Image.OPEN:
        supported |= 2  # IMG_JPG
    if 'png' in Image.OPEN:
        supported |= 4  # IMG_PNG
    if 'wbmp' in Image.OPEN:
        supported |= 8  # IMG_WBMP
    if 'xbm' in Image.OPEN:
        supported |= 16  # IMG_XPM
    return supported

def imagewbmp(image_res, filename=None):
    """
    Output image to browser or file in WBMP format.
    """
    if filename:
        image_res.image.save(filename, 'WBMP')
    else:
        image_res.image.save(sys.stdout, 'WBMP')

def imagewebp(image_res, filename=None):
    """
    Output a WebP image to browser or file.
    """
    if filename:
        image_res.image.save(filename, 'WEBP')
    else:
        image_res.image.save(sys.stdout, 'WEBP')

def imagexbm(image_res, filename=None):
    """
    Output an XBM image to browser or file.
    """
    if filename:
        image_res.image.save(filename, 'XBM')
    else:
        image_res.image.save(sys.stdout, 'XBM')

def iptcembed(iptcdata, jpeg_file_name, spool=0):
    """
    Embeds binary IPTC data into a JPEG image.
    """
    raise NotImplementedError("IPTC embedding is not supported by Pillow.")

def iptcparse(iptc_block):
    """
    Parse a binary IPTC block into single tags.
    """
    raise NotImplementedError("IPTC parsing is not supported by Pillow.")

def jpeg2wbmp(jpegname, wbmpname, dest_height, dest_width, threshold):
    """
    Convert JPEG image file to WBMP image file.
    """
    im = Image.open(jpegname)
    im = im.resize((dest_width, dest_height))
    if threshold:
        im = im.convert('L').point(lambda x: 255 if x > threshold else 0, '1')
    else:
        im = im.convert('1')
    im.save(wbmpname, 'WBMP')

def png2wbmp(pngname, wbmpname, dest_height, dest_width, threshold):
    """
    Convert PNG image file to WBMP image file.
    """
    im = Image.open(pngname)
    im = im.resize((dest_width, dest_height))
    if threshold:
        im = im.convert('L').point(lambda x: 255 if x > threshold else 0, '1')
    else:
        im = im.convert('1')
    im.save(wbmpname, 'WBMP')
