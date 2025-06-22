from PIL import Image, ImageDraw, ImageFont
import upcean.encode as upca
import os

def get_ocrb_font_path():
    try:
        import importlib.resources as resources
        return os.path.join(resources.files("upcean.fonts"), "OCRB.otf")
    except ImportError:
        pass
    try:
        import pkg_resources
        return pkg_resources.resource_filename("upcean.fonts", "OCRB.otf")
    except ImportError:
        pass
    fallback = os.path.dirname(__file__)
    return os.path.join(fallback, "upcean", "fonts", "OCRB.otf")

def generate_barcode_test_image():
    codes = {
        "Valid UPC-A": "123456789012",
        "Invalid UPC-A": "123456789014",   # Wrong check digit
        "Fixed UPC-A": "123456789014",     # Will be auto-corrected
    }

    barcodes = {
        "Valid UPC-A": upca.draw_upca_barcode(codes["Valid UPC-A"], 5, imageoutlib="pillow")[1],
        "Invalid UPC-A": upca.draw_upca_barcode(codes["Invalid UPC-A"], 5, imageoutlib="pillow")[1],
        "Fixed UPC-A": upca.fix_draw_upca_barcode(codes["Fixed UPC-A"], 5, imageoutlib="pillow")[1],
    }

    spacing = 20
    image_width = 600
    image_height = sum(img.height + spacing for img in barcodes.values()) + spacing

    output = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(output)

    y = spacing
    font_path = get_ocrb_font_path()
    try:
        font = ImageFont.truetype(font_path, 18)
    except:
        font = ImageFont.load_default()

    for label, img in barcodes.items():
        draw.text((10, y - 20), label, fill="black", font=font)
        output.paste(img, (10, y))
        y += img.height + spacing

    output.save("upca_test_sheet.png")
    print("Test sheet saved as upca_test_sheet.png")

generate_barcode_test_image()
