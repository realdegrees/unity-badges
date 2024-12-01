import subprocess
import os

from flask import request

def calculate_font_size(caption, base_font_size=170):
    # Adjust the font size based on the length of the caption
    max_length = 20  # Maximum length for the base font size
    if len(caption) > max_length:
        # Ensure font size doesn't go below 20
        return max(base_font_size - (len(caption) - max_length) * 5, 110)
    return base_font_size


def process_caption(caption):
    caption = caption.capitalize()
    caption, _ = os.path.splitext(caption)
    return caption

def load_font(caption):
    font_name = request.args.get('font', 'impact')
    base_font_size = int(request.args.get('font_size', '190'))
    font_size = calculate_font_size(caption, base_font_size)
    font_path = os.path.join('fonts', f'{font_name}.ttf')
    return font_path, font_size
