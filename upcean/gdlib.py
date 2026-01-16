# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: predraw.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

'''
Advanced GD-like wrapper on top of Pillow (PIL fork).

Goals vs your current version:
- Keep Python 2 + 3 support.
- Fix stdout saving (binary-safe).
- Fix Pillow deprecations (ANTIALIAS -> Resampling.* when available).
- Make imagefilter() robust for RGBA (invert preserves alpha).
- Make color handling safer across modes (P/RGB/RGBA/L/1).
- Make clipping actually apply (optional but implemented for most drawing ops).
- Make antialias meaningful for common primitives (draw at higher scale then downsample).
- Make font parameters respected (built-in fonts still map to a default; TTF supported).
- Make affine matrix API consistent and less error-prone.

Notes:
- This is still an emulation layer; exact PHP-GD behavior is not always possible in Pillow.
- Some GD features (brush/tile/style) are partially supported; you can extend further.

Copyright:
  Based on your original predraw.py structure.
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import math

from PIL import (
    Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
)

# -------------------------
# Py2 / Py3 compatibility
# -------------------------

PY3 = sys.version_info[0] >= 3

try:
    xrange
except NameError:
    xrange = range

try:
    basestring
except NameError:
    basestring = str

try:
    from io import BytesIO, StringIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO


def _stdout_binary():
    """
    Return a binary file-like object for stdout.
    Python 3: sys.stdout.buffer
    Python 2: sys.stdout (already byte-oriented)
    """
    if PY3 and hasattr(sys.stdout, "buffer"):
        return sys.stdout.buffer
    return sys.stdout


# Pillow resampling compatibility
try:
    # Pillow >= 9
    _RESAMPLING = Image.Resampling
    RESAMPLE_NEAREST = _RESAMPLING.NEAREST
    RESAMPLE_BILINEAR = _RESAMPLING.BILINEAR
    RESAMPLE_BICUBIC = _RESAMPLING.BICUBIC
    RESAMPLE_LANCZOS = _RESAMPLING.LANCZOS
except Exception:
    # Older Pillow
    RESAMPLE_NEAREST = getattr(Image, "NEAREST", 0)
    RESAMPLE_BILINEAR = getattr(Image, "BILINEAR", 2)
    RESAMPLE_BICUBIC = getattr(Image, "BICUBIC", 3)
    # Image.ANTIALIAS historically == LANCZOS
    RESAMPLE_LANCZOS = getattr(Image, "ANTIALIAS", 1)

# -------------------------
# GD-like constants
# -------------------------

# Filters
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

# Flip modes
IMG_FLIP_HORIZONTAL = 'horizontal'
IMG_FLIP_VERTICAL = 'vertical'
IMG_FLIP_BOTH = 'both'

# Affine types
IMG_AFFINE_TRANSLATE = 0
IMG_AFFINE_SCALE = 1
IMG_AFFINE_ROTATE = 2
IMG_AFFINE_SHEAR_HORIZONTAL = 3
IMG_AFFINE_SHEAR_VERTICAL = 4


# -------------------------
# Utilities
# -------------------------

def _clamp_int(v, lo, hi):
    try:
        v = int(v)
    except Exception:
        v = lo
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def _ensure_rgba(im):
    if im.mode == "RGBA":
        return im
    return im.convert("RGBA")


def _invert_preserve_alpha(im):
    """
    Pillow's ImageOps.invert doesn't work on RGBA directly the way we'd want
    (and may error on some modes). This inverts RGB and keeps alpha.
    """
    rgba = _ensure_rgba(im)
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))
    inv = ImageOps.invert(rgb)
    r2, g2, b2 = inv.split()
    return Image.merge("RGBA", (r2, g2, b2, a))


def _normalize_pixel_tuple(pixel, want_alpha=True):
    """
    Normalize a getpixel() result across modes.
    Returns (r,g,b,a) if want_alpha else (r,g,b).
    """
    if isinstance(pixel, int):
        # L or P may return int
        r = g = b = pixel
        a = 255
        return (r, g, b, a) if want_alpha else (r, g, b)

    if len(pixel) == 2:
        # LA
        l, a = pixel
        return (l, l, l, a) if want_alpha else (l, l, l)

    if len(pixel) == 3:
        r, g, b = pixel
        a = 255
        return (r, g, b, a) if want_alpha else (r, g, b)

    if len(pixel) >= 4:
        r, g, b, a = pixel[:4]
        return (r, g, b, a) if want_alpha else (r, g, b)

    # fallback
    return (0, 0, 0, 255) if want_alpha else (0, 0, 0)


def _rect_intersect(r1, r2):
    """
    r = (x1,y1,x2,y2) inclusive/exclusive doesn't matter as long as consistent.
    We'll treat as (left, top, right, bottom) where right/bottom are *exclusive-ish*.
    """
    if r1 is None:
        return r2
    if r2 is None:
        return r1
    x1 = max(r1[0], r2[0])
    y1 = max(r1[1], r2[1])
    x2 = min(r1[2], r2[2])
    y2 = min(r1[3], r2[3])
    if x2 <= x1 or y2 <= y1:
        return (0, 0, 0, 0)
    return (x1, y1, x2, y2)


def _clip_to_image(im, clip):
    if clip is None:
        return None
    w, h = im.size
    x1, y1, x2, y2 = clip
    x1 = _clamp_int(x1, 0, w)
    y1 = _clamp_int(y1, 0, h)
    x2 = _clamp_int(x2, 0, w)
    y2 = _clamp_int(y2, 0, h)
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)


def _parse_colorize_args(args):
    """
    Your original expected (r,g,b,a). Keep that.
    """
    if len(args) >= 4:
        r, g, b, a = args[:4]
        return (_clamp_int(r, 0, 255),
                _clamp_int(g, 0, 255),
                _clamp_int(b, 0, 255),
                _clamp_int(a, 0, 255))
    # fallback
    return (0, 0, 0, 0)


# -------------------------
# Core resource wrapper
# -------------------------

class ImageResource(object):
    """
    GD-like image resource wrapper.
    """

    def __init__(self, image):
        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.colors = {}
        self.next_color_index = 1  # match GD-ish behavior

        # Optional GD-like state
        self.brush = None
        self.tile = None
        self.style = None
        self.clip = None

        # Rendering preferences
        self.interpolation = RESAMPLE_NEAREST
        self.antialias = False
        self.aa_scale = 4  # draw scale when antialias enabled
        self.thickness = 1

        self.alpha_blending = True
        self.save_alpha = False

    def _refresh_draw(self):
        self.draw = ImageDraw.Draw(self.image)

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

    def get_clip_rect(self):
        return _clip_to_image(self.image, self.clip)

    def _apply_clip_mask(self):
        """
        Create an 'L' mask (white in clip, black outside) or None if no clip.
        """
        clip = self.get_clip_rect()
        if clip is None:
            return None
        w, h = self.image.size
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        md.rectangle([clip[0], clip[1], clip[2], clip[3]], fill=255)
        return mask

    def _draw_with_optional_aa(self, draw_fn):
        """
        If antialias is enabled, draw on a larger RGBA canvas, then downsample.
        This gives smoother edges for shapes/lines at the cost of speed.

        draw_fn takes (img, draw) and performs drawing operations on it.
        """
        if not self.antialias:
            draw_fn(self.image, self.draw)
            return

        scale = int(self.aa_scale) if int(self.aa_scale) >= 2 else 2
        base = _ensure_rgba(self.image)
        w, h = base.size
        big = base.resize((w * scale, h * scale), resample=RESAMPLE_NEAREST)

        big_draw = ImageDraw.Draw(big)

        # Temporarily scale clip and thickness
        old_thick = self.thickness
        thick = max(1, int(old_thick) * scale)

        def draw_scaled(img, dr):
            # expose a thin wrapper for thickness scaling
            return draw_fn(img, dr, scale, thick)

        draw_scaled(big, big_draw)

        # Downsample with LANCZOS for smoothing
        small = big.resize((w, h), resample=RESAMPLE_LANCZOS)

        # If original wasn't RGBA, convert back carefully
        # (for simplicity, we keep RGBA; callers often expect alpha anyway)
        self.image = small
        self._refresh_draw()


# -------------------------
# GD-like API
# -------------------------

def gd_info():
    """
    Info about "GD" here is really Pillow capabilities.
    """
    # FreeType support detection is not super reliable across Pillow builds;
    # but ImageFont.truetype generally works if freetype is present.
    has_freetype = True
    try:
        ImageFont.truetype
    except Exception:
        has_freetype = False

    return {
        'GD Version': 'Pillow ' + getattr(Image, "__version__", "unknown"),
        'FreeType Support': 'Yes' if has_freetype else 'No',
        'GIF Read Support': 'Yes' if 'gif' in Image.OPEN else 'No',
        'GIF Create Support': 'Yes' if 'gif' in Image.SAVE else 'No',
        'JPEG Support': 'Yes' if 'jpeg' in Image.OPEN else 'No',
        'PNG Support': 'Yes' if 'png' in Image.OPEN else 'No',
        'WBMP Support': 'Yes' if 'wbmp' in Image.OPEN else 'No',
        'XPM Support': 'No',
        'XBM Support': 'Yes' if 'xbm' in Image.OPEN else 'No',
        'WebP Support': 'Yes' if 'webp' in Image.OPEN else 'No',
    }


def getimagesize(filename):
    with Image.open(filename) as img:
        return img.size + (img.format, img.mode)


def getimagesizefromstring(image_data):
    img = Image.open(BytesIO(image_data))
    return img.size + (img.format, img.mode)


def image_type_to_extension(image_type, include_dot=True):
    extensions = {
        'JPEG': 'jpeg',
        'JPG': 'jpeg',
        'PNG': 'png',
        'GIF': 'gif',
        'BMP': 'bmp',
        'TIFF': 'tiff',
        'ICO': 'ico',
        'WEBP': 'webp',
        'AVIF': 'avif',
        'WBMP': 'wbmp',
        'XBM': 'xbm',
    }
    ext = extensions.get(str(image_type).upper(), '')
    return ('.' if include_dot else '') + ext


def image_type_to_mime_type(image_type):
    mime_types = {
        'JPEG': 'image/jpeg',
        'JPG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
        'BMP': 'image/bmp',
        'TIFF': 'image/tiff',
        'ICO': 'image/vnd.microsoft.icon',
        'WEBP': 'image/webp',
        'AVIF': 'image/avif',
        'WBMP': 'image/vnd.wap.wbmp',
        'XBM': 'image/x-xbitmap',
    }
    return mime_types.get(str(image_type).upper(), 'application/octet-stream')


# -------------------------
# Create / Load
# -------------------------

def imagecreate(width, height):
    # Palette image (P) similar to GD palette images
    im = Image.new("P", (int(width), int(height)))
    return ImageResource(im)


def imagecreatetruecolor(width, height):
    im = Image.new("RGBA", (int(width), int(height)))
    return ImageResource(im)


def imagecreatefromstring(image_data):
    im = Image.open(BytesIO(image_data))
    return ImageResource(im)


def imagecreatefromjpeg(filename):
    im = Image.open(filename)
    return ImageResource(im.convert('RGB'))


def imagecreatefrompng(filename):
    im = Image.open(filename)
    # Preserve alpha if present
    if im.mode not in ("RGBA", "LA"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGBA")
    return ImageResource(im)


def imagecreatefromgif(filename):
    im = Image.open(filename)
    # Keep palette where possible; GD-ish
    return ImageResource(im.convert('P'))


def imagecreatefromwebp(filename):
    im = Image.open(filename)
    return ImageResource(im)


def imagecreatefrombmp(filename):
    im = Image.open(filename)
    return ImageResource(im)


def imagecreatefromwbmp(filename):
    im = Image.open(filename)
    return ImageResource(im)


def imagecreatefromxbm(filename):
    im = Image.open(filename)
    return ImageResource(im)


def imagecreatefromtga(filename):
    im = Image.open(filename)
    return ImageResource(im)


def imagecreatefromavif(filename):
    im = Image.open(filename)
    return ImageResource(im)


# -------------------------
# Color allocation
# -------------------------

def imagecolorallocate(image_res, red, green, blue):
    red = _clamp_int(red, 0, 255)
    green = _clamp_int(green, 0, 255)
    blue = _clamp_int(blue, 0, 255)
    color = (red, green, blue, 255)
    idx = image_res.next_color_index
    image_res.colors[idx] = color
    image_res.next_color_index += 1
    return idx


def imagecolorallocatealpha(image_res, red, green, blue, alpha):
    """
    GD alpha: 0 opaque .. 127 transparent
    Pillow alpha: 0 transparent .. 255 opaque
    """
    red = _clamp_int(red, 0, 255)
    green = _clamp_int(green, 0, 255)
    blue = _clamp_int(blue, 0, 255)
    alpha = _clamp_int(alpha, 0, 127)
    pillow_a = int(255 - (alpha / 127.0) * 255)
    color = (red, green, blue, _clamp_int(pillow_a, 0, 255))
    idx = image_res.next_color_index
    image_res.colors[idx] = color
    image_res.next_color_index += 1
    return idx


def imagecolorat(image_res, x, y):
    pixel = image_res.image.getpixel((int(x), int(y)))
    px = _normalize_pixel_tuple(pixel, want_alpha=True)
    # Look for exact match
    for idx, c in image_res.colors.items():
        if tuple(c) == tuple(px):
            return idx
    # Allocate new (ignores alpha if you want GD palette behavior; here we keep alpha as opaque allocation)
    return imagecolorallocate(image_res, px[0], px[1], px[2])


def imagecolordeallocate(image_res, color_index):
    if color_index in image_res.colors:
        del image_res.colors[color_index]


def imagecolorexact(image_res, red, green, blue):
    red = _clamp_int(red, 0, 255)
    green = _clamp_int(green, 0, 255)
    blue = _clamp_int(blue, 0, 255)
    for idx, c in image_res.colors.items():
        if c[:3] == (red, green, blue):
            return idx
    return -1


def imagecolorexactalpha(image_res, red, green, blue, alpha):
    red = _clamp_int(red, 0, 255)
    green = _clamp_int(green, 0, 255)
    blue = _clamp_int(blue, 0, 255)
    alpha = _clamp_int(alpha, 0, 255)
    for idx, c in image_res.colors.items():
        if tuple(c) == (red, green, blue, alpha):
            return idx
    return -1


def imagecolorresolve(image_res, red, green, blue):
    idx = imagecolorexact(image_res, red, green, blue)
    if idx != -1:
        return idx
    return imagecolorallocate(image_res, red, green, blue)


def imagecolorresolvealpha(image_res, red, green, blue, alpha):
    idx = imagecolorexactalpha(image_res, red, green, blue, alpha)
    if idx != -1:
        return idx
    # alpha here is Pillow alpha already (0..255) for this helper
    return imagecolorallocatealpha(image_res, red, green, blue, int(127 - (alpha / 255.0) * 127))


def imagecolorset(image_res, index, red, green, blue, alpha=255):
    image_res.colors[int(index)] = (
        _clamp_int(red, 0, 255),
        _clamp_int(green, 0, 255),
        _clamp_int(blue, 0, 255),
        _clamp_int(alpha, 0, 255),
    )


def imagecolorsforindex(image_res, index):
    return image_res.colors.get(int(index), None)


def imagecolorstotal(image_res):
    return len(image_res.colors)


def imagecolortransparent(image_res, color_index):
    # Pillow uses 'transparency' in info for some formats, but true transparency is format-specific.
    # We store it to be used on save where possible.
    image_res.image.info['transparency'] = image_res.get_color(color_index)


# -------------------------
# Drawing helpers (clip + optional AA)
# -------------------------

def imagesetclip(image_res, x1, y1, x2, y2):
    image_res.set_clip((int(x1), int(y1), int(x2), int(y2)))


def imagegetclip(image_res):
    return image_res.clip


def imagesetthickness(image_res, thickness):
    image_res.thickness = max(1, int(thickness))


def imageantialias(image_res, on):
    image_res.antialias = bool(on)


def imagealphablending(image_res, blendmode):
    image_res.alpha_blending = bool(blendmode)


def imagesavealpha(image_res, saveflag):
    image_res.save_alpha = bool(saveflag)


def _compose_paste(dst_im, src_im, xy, mask=None, alpha_blending=True):
    """
    Paste helper that respects alpha_blending flag.
    - If alpha_blending True: alpha composite (for RGBA)
    - Else: hard paste (overwrite)
    """
    x, y = xy
    if not alpha_blending:
        dst_im.paste(src_im, (x, y), mask)
        return dst_im

    # Alpha blend using compositing when possible
    dst_rgba = _ensure_rgba(dst_im)
    src_rgba = _ensure_rgba(src_im)

    # Create a temporary layer the size of dst for correct composite
    layer = Image.new("RGBA", dst_rgba.size, (0, 0, 0, 0))
    layer.paste(src_rgba, (x, y), mask if mask is not None else src_rgba)

    out = Image.alpha_composite(dst_rgba, layer)
    return out


def imageline(image_res, x1, y1, x2, y2, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()

    def draw_fn(img, dr, scale=1, thick=None):
        t = thick if thick is not None else image_res.thickness
        xx1, yy1, xx2, yy2 = int(x1)*scale, int(y1)*scale, int(x2)*scale, int(y2)*scale
        dr.line((xx1, yy1, xx2, yy2), fill=color, width=int(t))

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    # Draw on temp then clip-composite back
    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, image_res.thickness)

    # apply clip
    tmp.putalpha(ImageChops.multiply(tmp.split()[-1], clip_mask)) if 'ImageChops' in globals() else None
    # If ImageChops wasn't imported, fallback: paste with mask
    if 'ImageChops' not in globals():
        out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    else:
        out = Image.alpha_composite(base, tmp)
    image_res.image = out
    image_res._refresh_draw()


def imagerectangle(image_res, x1, y1, x2, y2, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()

    def draw_fn(img, dr, scale=1, thick=None):
        t = thick if thick is not None else image_res.thickness
        dr.rectangle([int(x1)*scale, int(y1)*scale, int(x2)*scale, int(y2)*scale],
                     outline=color, width=int(t))

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, image_res.thickness)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imagefilledrectangle(image_res, x1, y1, x2, y2, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()

    def draw_fn(img, dr, scale=1, thick=None):
        dr.rectangle([int(x1)*scale, int(y1)*scale, int(x2)*scale, int(y2)*scale],
                     fill=color)

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, None)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imageellipse(image_res, cx, cy, width, height, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()
    cx, cy, width, height = int(cx), int(cy), int(width), int(height)

    def draw_fn(img, dr, scale=1, thick=None):
        t = thick if thick is not None else image_res.thickness
        bbox = [ (cx - width // 2)*scale, (cy - height // 2)*scale,
                 (cx + width // 2)*scale, (cy + height // 2)*scale ]
        dr.ellipse(bbox, outline=color, width=int(t))

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, image_res.thickness)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imagefilledellipse(image_res, cx, cy, width, height, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()
    cx, cy, width, height = int(cx), int(cy), int(width), int(height)

    def draw_fn(img, dr, scale=1, thick=None):
        bbox = [ (cx - width // 2)*scale, (cy - height // 2)*scale,
                 (cx + width // 2)*scale, (cy + height // 2)*scale ]
        dr.ellipse(bbox, fill=color)

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, None)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imagearc(image_res, cx, cy, width, height, start, end, color_index):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()
    cx, cy, width, height = int(cx), int(cy), int(width), int(height)

    def draw_fn(img, dr, scale=1, thick=None):
        t = thick if thick is not None else image_res.thickness
        bbox = [ (cx - width // 2)*scale, (cy - height // 2)*scale,
                 (cx + width // 2)*scale, (cy + height // 2)*scale ]
        dr.arc(bbox, float(start), float(end), fill=color, width=int(t))

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, image_res.thickness)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imagefilledarc(image_res, cx, cy, width, height, start, end, color_index, style=None):
    color = image_res.get_color(color_index)
    clip_mask = image_res._apply_clip_mask()
    cx, cy, width, height = int(cx), int(cy), int(width), int(height)

    def draw_fn(img, dr, scale=1, thick=None):
        bbox = [ (cx - width // 2)*scale, (cy - height // 2)*scale,
                 (cx + width // 2)*scale, (cy + height // 2)*scale ]
        dr.pieslice(bbox, float(start), float(end), fill=color)

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, None)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


def imagepolygon(image_res, points, num_points, color_index):
    color = image_res.get_color(color_index)
    pts = [(int(x), int(y)) for (x, y) in points[:int(num_points)]]
    clip_mask = image_res._apply_clip_mask()

    def draw_fn(img, dr, scale=1, thick=None):
        p2 = [(x*scale, y*scale) for (x, y) in pts]
        dr.polygon(p2, outline=color)

    if clip_mask is None:
        image_res._draw_with_optional_aa(draw_fn)
        return

    base = _ensure_rgba(image_res.image)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    draw_fn(tmp, tmp_draw, 1, None)
    out = _compose_paste(base, tmp, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
    image_res.image = out
    image_res._refresh_draw()


# -------------------------
# Copy / Merge / Resize
# -------------------------

def imagecopy(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h):
    box = (int(src_x), int(src_y), int(src_x) + int(src_w), int(src_y) + int(src_h))
    region = image_res_src.image.crop(box)
    image_res_dst.image.paste(region, (int(dst_x), int(dst_y)))
    image_res_dst._refresh_draw()


def imagecopymerge(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h, pct):
    box = (int(src_x), int(src_y), int(src_x) + int(src_w), int(src_y) + int(src_h))
    region = _ensure_rgba(image_res_src.image.crop(box))
    alpha = _clamp_int(int(255 * (float(pct) / 100.0)), 0, 255)
    mask = Image.new('L', region.size, alpha)

    base = _ensure_rgba(image_res_dst.image)
    out = _compose_paste(base, region, (int(dst_x), int(dst_y)), mask=mask, alpha_blending=image_res_dst.alpha_blending)
    image_res_dst.image = out
    image_res_dst._refresh_draw()


def imagecopymergegray(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, src_w, src_h, pct):
    box = (int(src_x), int(src_y), int(src_x) + int(src_w), int(src_y) + int(src_h))
    region = image_res_src.image.crop(box).convert('L').convert('RGBA')
    alpha = _clamp_int(int(255 * (float(pct) / 100.0)), 0, 255)
    mask = Image.new('L', region.size, alpha)

    base = _ensure_rgba(image_res_dst.image)
    out = _compose_paste(base, region, (int(dst_x), int(dst_y)), mask=mask, alpha_blending=image_res_dst.alpha_blending)
    image_res_dst.image = out
    image_res_dst._refresh_draw()


def imagecopyresized(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h):
    box = (int(src_x), int(src_y), int(src_x) + int(src_w), int(src_y) + int(src_h))
    region = image_res_src.image.crop(box).resize((int(dst_w), int(dst_h)), resample=RESAMPLE_NEAREST)
    image_res_dst.image.paste(region, (int(dst_x), int(dst_y)))
    image_res_dst._refresh_draw()


def imagecopyresampled(image_res_dst, image_res_src, dst_x, dst_y, src_x, src_y, dst_w, dst_h, src_w, src_h):
    box = (int(src_x), int(src_y), int(src_x) + int(src_w), int(src_y) + int(src_h))
    region = image_res_src.image.crop(box).resize((int(dst_w), int(dst_h)), resample=RESAMPLE_LANCZOS)
    image_res_dst.image.paste(region, (int(dst_x), int(dst_y)))
    image_res_dst._refresh_draw()


def imagescale(image_res, new_width, new_height=None, mode=None):
    if mode is None:
        mode = image_res.interpolation
    new_width = int(new_width)
    if new_height is None:
        w, h = image_res.image.size
        if w == 0:
            new_height = h
        else:
            new_height = int(round((float(new_width) / float(w)) * h))
    new_height = int(new_height)
    image_res.image = image_res.image.resize((new_width, new_height), resample=mode)
    image_res._refresh_draw()
    return image_res


# -------------------------
# Crop / Auto crop
# -------------------------

def imagecrop(image_res, rect):
    left = int(rect.get('x', 0))
    upper = int(rect.get('y', 0))
    right = left + int(rect.get('width', 0))
    lower = upper + int(rect.get('height', 0))
    cropped = image_res.image.crop((left, upper, right, lower))
    return ImageResource(cropped)


def imagecropauto(image_res, mode=0, threshold=0.5, color=None):
    bbox = image_res.image.getbbox()
    if bbox:
        return ImageResource(image_res.image.crop(bbox))
    return image_res


# -------------------------
# Filters
# -------------------------

def imagefilter(image_res, filtertype, *args):
    im = image_res.image

    if filtertype == IMG_FILTER_NEGATE:
        image_res.image = _invert_preserve_alpha(im)

    elif filtertype == IMG_FILTER_GRAYSCALE:
        # keep alpha if present
        rgba = _ensure_rgba(im)
        r, g, b, a = rgba.split()
        gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
        image_res.image = Image.merge("RGBA", (gray, gray, gray, a))

    elif filtertype == IMG_FILTER_BRIGHTNESS:
        factor = float(args[0]) if args else 1.0
        image_res.image = ImageEnhance.Brightness(_ensure_rgba(im)).enhance(factor)

    elif filtertype == IMG_FILTER_CONTRAST:
        factor = float(args[0]) if args else 1.0
        image_res.image = ImageEnhance.Contrast(_ensure_rgba(im)).enhance(factor)

    elif filtertype == IMG_FILTER_COLORIZE:
        r, g, b, a = _parse_colorize_args(args)
        base = _ensure_rgba(im)
        overlay = Image.new('RGBA', base.size, (r, g, b, a))
        image_res.image = Image.alpha_composite(base, overlay)

    elif filtertype == IMG_FILTER_EDGEDETECT:
        image_res.image = im.filter(ImageFilter.FIND_EDGES)

    elif filtertype == IMG_FILTER_GAUSSIAN_BLUR:
        radius = float(args[0]) if args else 1.0
        image_res.image = im.filter(ImageFilter.GaussianBlur(radius=radius))

    elif filtertype == IMG_FILTER_SELECTIVE_BLUR:
        image_res.image = im.filter(ImageFilter.BLUR)

    elif filtertype == IMG_FILTER_EMBOSS:
        image_res.image = im.filter(ImageFilter.EMBOSS)

    elif filtertype == IMG_FILTER_MEAN_REMOVAL:
        image_res.image = im.filter(ImageFilter.MedianFilter(size=3))

    elif filtertype == IMG_FILTER_SMOOTH:
        image_res.image = im.filter(ImageFilter.SMOOTH_MORE)

    # refresh draw after modifications
    image_res._refresh_draw()


# -------------------------
# Flip / Rotate
# -------------------------

def imageflip(image_res, mode):
    if mode == IMG_FLIP_VERTICAL:
        image_res.image = image_res.image.transpose(Image.FLIP_TOP_BOTTOM)
    elif mode == IMG_FLIP_HORIZONTAL:
        image_res.image = image_res.image.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == IMG_FLIP_BOTH:
        image_res.image = image_res.image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
    image_res._refresh_draw()


def imagerotate(image_res, angle, bgd_color_index=0):
    bg = image_res.get_color(bgd_color_index)
    # Pillow expects fillcolor to match mode
    im = image_res.image
    if im.mode in ("RGBA", "RGB"):
        fill = bg[:4] if im.mode == "RGBA" else bg[:3]
    else:
        # convert to RGBA to preserve alpha rotation
        im = _ensure_rgba(im)
        fill = bg[:4]
    image_res.image = im.rotate(float(angle), expand=1, resample=RESAMPLE_BICUBIC, fillcolor=fill)
    image_res._refresh_draw()


# -------------------------
# Text (better font handling)
# -------------------------

def _load_font(font, size=12):
    """
    Accept:
    - a PIL ImageFont instance -> return it
    - a path (basestring) -> truetype(path, size)
    - None / otherwise -> load_default()
    """
    if font is None:
        return ImageFont.load_default()
    # PIL font object?
    if hasattr(font, "getbbox") or hasattr(font, "getsize"):
        return font
    if isinstance(font, basestring):
        try:
            return ImageFont.truetype(font, int(size))
        except Exception:
            return ImageFont.load_default()
    return ImageFont.load_default()


def imageftbbox(size, angle, fontfile, text):
    f = _load_font(fontfile, size=size)
    # Pillow getbbox gives (x0,y0,x1,y1)
    try:
        return f.getbbox(text)
    except Exception:
        # fallback (older Pillow)
        w, h = f.getsize(text)
        return (0, 0, w, h)


def imagefttext(image_res, size, angle, x, y, color_index, fontfile, text, extra_info=None):
    color = image_res.get_color(color_index)
    font = _load_font(fontfile, size=size)

    base = _ensure_rgba(image_res.image)
    clip_mask = image_res._apply_clip_mask()

    ang = float(angle)
    if ang == 0.0:
        tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        td.text((int(x), int(y)), text, font=font, fill=color)
        if clip_mask is None:
            image_res.image = _compose_paste(base, tmp, (0, 0), mask=tmp.split()[-1], alpha_blending=image_res.alpha_blending)
        else:
            # combine text alpha with clip mask
            text_alpha = tmp.split()[-1]
            combined = ImageChops.multiply(text_alpha, clip_mask) if 'ImageChops' in globals() else clip_mask
            image_res.image = _compose_paste(base, tmp, (0, 0), mask=combined, alpha_blending=image_res.alpha_blending)
    else:
        # Render tight text then rotate, so positioning is less weird.
        try:
            bbox = font.getbbox(text)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except Exception:
            tw, th = font.getsize(text)

        txt = Image.new("RGBA", (max(1, tw), max(1, th)), (0, 0, 0, 0))
        td = ImageDraw.Draw(txt)
        td.text((0, 0), text, font=font, fill=color)
        rot = txt.rotate(ang, expand=1, resample=RESAMPLE_BICUBIC)

        if clip_mask is None:
            image_res.image = _compose_paste(base, rot, (int(x), int(y)), mask=rot.split()[-1], alpha_blending=image_res.alpha_blending)
        else:
            # paste then clip via mask at full-canvas level
            layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
            layer.paste(rot, (int(x), int(y)), rot)
            out = _compose_paste(base, layer, (0, 0), mask=clip_mask, alpha_blending=image_res.alpha_blending)
            image_res.image = out

    image_res._refresh_draw()
    return None


# Basic GD-ish string functions: keep simple default font
def imagestring(image_res, font, x, y, string, color_index):
    color = image_res.get_color(color_index)
    f = _load_font(font, size=12)
    image_res.draw.text((int(x), int(y)), string, font=f, fill=color)


def imagestringup(image_res, font, x, y, string, color_index):
    color = image_res.get_color(color_index)
    f = _load_font(font, size=12)
    try:
        bbox = f.getbbox(string)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        tw, th = f.getsize(string)
    txt = Image.new("RGBA", (max(1, tw), max(1, th)), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)
    td.text((0, 0), string, font=f, fill=color)
    rot = txt.rotate(90, expand=1, resample=RESAMPLE_BICUBIC)
    base = _ensure_rgba(image_res.image)
    image_res.image = _compose_paste(base, rot, (int(x), int(y)), mask=rot, alpha_blending=image_res.alpha_blending)
    image_res._refresh_draw()


# -------------------------
# Affine transforms
# -------------------------

def imageaffinematrixget(type_, options):
    """
    Consistent API:
    - translate: options is dict {'x':..., 'y':...}
    - scale: options is dict {'x':..., 'y':...}
    - rotate: options is dict {'angle': degrees} OR a numeric angle (degrees)
    - shear: options is dict {'factor':...} OR numeric factor
    Returns [a,b,c,d,e,f]
    """
    if type_ == IMG_AFFINE_TRANSLATE:
        if isinstance(options, dict):
            tx = float(options.get('x', 0.0))
            ty = float(options.get('y', 0.0))
        else:
            tx, ty = 0.0, 0.0
        return [1, 0, tx, 0, 1, ty]

    if type_ == IMG_AFFINE_SCALE:
        if isinstance(options, dict):
            sx = float(options.get('x', 1.0))
            sy = float(options.get('y', 1.0))
        else:
            sx, sy = 1.0, 1.0
        return [sx, 0, 0, 0, sy, 0]

    if type_ == IMG_AFFINE_ROTATE:
        if isinstance(options, dict):
            deg = float(options.get('angle', 0.0))
        else:
            deg = float(options)
        ang = math.radians(deg)
        c = math.cos(ang)
        s = math.sin(ang)
        return [c, s, 0, -s, c, 0]

    if type_ == IMG_AFFINE_SHEAR_HORIZONTAL:
        factor = float(options.get('factor', 0.0)) if isinstance(options, dict) else float(options)
        return [1, factor, 0, 0, 1, 0]

    if type_ == IMG_AFFINE_SHEAR_VERTICAL:
        factor = float(options.get('factor', 0.0)) if isinstance(options, dict) else float(options)
        return [1, 0, 0, factor, 1, 0]

    return [1, 0, 0, 0, 1, 0]


def imageaffinematrixconcat(m1, m2):
    a = m1[0]*m2[0] + m1[1]*m2[3]
    b = m1[0]*m2[1] + m1[1]*m2[4]
    c = m1[0]*m2[2] + m1[1]*m2[5] + m1[2]
    d = m1[3]*m2[0] + m1[4]*m2[3]
    e = m1[3]*m2[1] + m1[4]*m2[4]
    f = m1[3]*m2[2] + m1[4]*m2[5] + m1[5]
    return [a, b, c, d, e, f]


def imageaffine(image_res, matrix, options=None):
    """
    Pillow affine expects (a,b,c,d,e,f).
    """
    m = (float(matrix[0]), float(matrix[1]), float(matrix[2]),
         float(matrix[3]), float(matrix[4]), float(matrix[5]))
    out = image_res.image.transform(image_res.image.size, Image.AFFINE, m, resample=image_res.interpolation)
    return ImageResource(out)


# -------------------------
# Save / output functions (fixed stdout + alpha)
# -------------------------

def _save(image_res, fmt, filename=None, **kwargs):
    im = image_res.image

    # If not saving alpha, flatten if RGBA (GD often discards alpha depending on settings)
    if im.mode == "RGBA" and not image_res.save_alpha and fmt.upper() in ("JPEG", "BMP"):
        # flatten onto white background
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg

    if filename:
        im.save(filename, fmt, **kwargs)
    else:
        im.save(_stdout_binary(), fmt, **kwargs)


def imagepng(image_res, filename=None):
    _save(image_res, "PNG", filename=filename)


def imagegif(image_res, filename=None):
    _save(image_res, "GIF", filename=filename)


def imagewebp(image_res, filename=None):
    _save(image_res, "WEBP", filename=filename)


def imagebmp(image_res, filename=None, compressed=True):
    # Pillow BMP doesn't support "compress_level" like PNG; it uses "compression" in some builds.
    # We'll try to map compressed flag lightly.
    kwargs = {}
    if not compressed:
        kwargs["compression"] = "raw"
    _save(image_res, "BMP", filename=filename, **kwargs)


def imagewbmp(image_res, filename=None):
    _save(image_res, "WBMP", filename=filename)


def imageavif(image_res, filename=None):
    _save(image_res, "AVIF", filename=filename)


def imagexbm(image_res, filename=None):
    _save(image_res, "XBM", filename=filename)


def image2wbmp(image_res, filename=None, threshold=0):
    im = image_res.image
    if threshold:
        thr = int(threshold)
        im = im.convert('L').point(lambda x: 255 if x > thr else 0, '1')
    else:
        im = im.convert('1')
    if filename:
        im.save(filename, 'WBMP')
    else:
        im.save(_stdout_binary(), 'WBMP')


# -------------------------
# Misc
# -------------------------

def imagesx(image_res):
    return image_res.image.size[0]


def imagesy(image_res):
    return image_res.image.size[1]


def imageistruecolor(image_res):
    return image_res.image.mode in ('RGB', 'RGBA')


def imageinterlace(image_res, interlace):
    image_res.image.info['interlace'] = bool(interlace)


def imagesetinterpolation(image_res, method):
    image_res.set_interpolation(method)


def imagegetinterpolation(image_res):
    return image_res.interpolation


def imageresolution(image_res, res_x=None, res_y=None):
    if res_x is None and res_y is None:
        return image_res.image.info.get('dpi', (72, 72))
    image_res.image.info['dpi'] = (int(res_x), int(res_y))
    return True


def imagedestroy(image_res):
    try:
        del image_res.draw
    except Exception:
        pass
    try:
        del image_res.image
    except Exception:
        pass
    try:
        image_res.colors.clear()
    except Exception:
        pass


# -------------------------
# Optional: TTF helpers to keep names
# -------------------------

def imagettfbbox(size, angle, fontfile, text):
    return imageftbbox(size, angle, fontfile, text)


def imagettftext(image_res, size, angle, x, y, color_index, fontfile, text):
    return imagefttext(image_res, size, angle, x, y, color_index, fontfile, text)


# -------------------------
# Still not implemented (GD/GD2/IPTC)
# -------------------------

def imagegd(image_res, filename=None):
    raise NotImplementedError("GD format is not supported by Pillow.")


def imagegd2(image_res, filename=None):
    raise NotImplementedError("GD2 format is not supported by Pillow.")


def iptcembed(iptcdata, jpeg_file_name, spool=0):
    raise NotImplementedError("IPTC embedding is not supported by Pillow.")


def iptcparse(iptc_block):
    raise NotImplementedError("IPTC parsing is not supported by Pillow.")
