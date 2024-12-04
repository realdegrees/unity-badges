from typing import Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
from typing import List
from util.table import Table, Cell
from util.text import get_text_dimensions

font = ImageFont.truetype(os.path.join("fonts", "arial.ttf"), 24)
padding = 2


def draw_badge(label: str, content: List[List[Cell]], header_color, footer_color, body_color, footer_height=5, max_col_width=1000, padding=5, corner_radius=8) -> Image:
    label = label if len(label) < 200 else "Label too long (200)"
    
    content = content if content and len(content) > 0 else [
        [Cell("|" + len(label) * " " + "None" + len(label) * " " + "|")]]
    
    table = Table(content, font, max_col_width, padding)

    badge_width = table.get_width()

    header_content_width, header_content_height, label = get_text_dimensions(
        font, badge_width, label)
    header_height = header_content_height + padding
    badge_height = table.get_height() + footer_height + header_height

    # Create the badge image
    image = Image.new("RGBA", (badge_width, badge_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the body with a subtle gradient
    base_color = ImageColor.getrgb(body_color)
    gradient_intensity = 20  # Adjust this value to change the intensity of the gradient
    for x in range(badge_width):
        gradient_color = (
            int(base_color[0] + (gradient_intensity * x / badge_width)),
            int(base_color[1] + (gradient_intensity * x / badge_width)),
            int(base_color[2] + (gradient_intensity * x / badge_width)),
            255,
        )
        draw.line([(x, header_height), (x, badge_height +
                  header_height)], fill=gradient_color)

    # Draw the footer with a gradient
    base_color = ImageColor.getrgb(footer_color)
    gradient_intensity = 20  # Adjust this value to change the intensity of the gradient
    for x in range(badge_width):
        gradient_color = (
            int(base_color[0] + (gradient_intensity * x / badge_width)),
            int(base_color[1] + (gradient_intensity * x / badge_width)),
            int(base_color[2] + (gradient_intensity * x / badge_width)),
            255,
        )
        draw.line([(x, badge_height - footer_height),
                  (x, badge_height)], fill=gradient_color)

    # Draw the header with a gradient
    base_color = ImageColor.getrgb(header_color)
    gradient_intensity = 20  # Adjust this value to change the intensity of the gradient
    for x in range(badge_width):
        gradient_color = (
            int(base_color[0] + (gradient_intensity * x / badge_width)),
            int(base_color[1] + (gradient_intensity * x / badge_width)),
            int(base_color[2] + (gradient_intensity * x / badge_width)),
            255,
        )
        draw.line([(x, 0), (x, header_height)], fill=gradient_color)

    def draw_text(draw, content, content_height, content_width, max_height, x_offset, y_offset, stroke_width=0.6):
        lines = content.split("\n")

        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]

            text_x = x_offset + (content_width - line_width) // 2
            draw.text((text_x, y_offset), line, font=font, fill="white",
                      stroke_fill="#434343", stroke_width=stroke_width)
            y_offset += line_height

    draw_text(draw, label, header_content_height, header_content_width, header_height,
              (badge_width - header_content_width) // 2, (header_height - header_content_height) // 2, 1)

    def draw_cell_content(image: Image.Image, draw: ImageDraw.ImageDraw, cell: Cell) -> None:
        [x_offset, y_offset] = cell.table.get_cell_offset(cell)
        y_offset += header_height
        # Draw cell background if color is provided
        if cell.color:
            draw.rectangle(
                [x_offset, y_offset, x_offset + cell.width, y_offset + cell.height],
                fill=cell.color,
            )

        # Handle cell content
        if isinstance(cell.content, str):  # String content
            col_width = cell.table.get_col_width(cell.col)
            row_height = cell.table.get_row_height(cell.row)
            # x_offset += (col_width - cell.width) // 2
            # y_offset += (row_height - cell.height) // 2
            draw_text(draw, cell.content, cell.height, col_width, row_height,
                      x_offset, y_offset, stroke_width=1 if cell.row == 0 else 0.6)

        elif isinstance(cell.content, Image.Image):  # Icon content
            column_width = cell.table.get_col_width(cell.col)
            image_x = x_offset + (column_width - cell.width) // 2
            image_y = y_offset + (column_width - cell.height) // 2
            image.paste(cell.content, (image_x, image_y))

    # Draw content
    def draw_cell(cell: Cell):
        # Draw Content
        draw_cell_content(
            image, draw, cell) if cell.content else None

    def draw_seperator(y_offset: int, row: int):
        if row == 0 or row == len(content):
            return
        draw.line((0, y_offset, badge_width, y_offset),
                  fill=(0, 0, 0, 0), width=2)

    table.for_each_row(lambda y_offset, row: draw_seperator(
        y_offset + header_height, row))
    table.for_each_cell(draw_cell)

    # Round the corners of the image
    def round_corners(image: Image.Image, radius: int) -> Image.Image:
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask)
        return rounded_image

    if corner_radius > 0:
        image = round_corners(image, corner_radius)

    # Save the image
    return image
