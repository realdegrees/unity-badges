import textwrap

def get_text_dimensions(font, max_width, content):
    wrapped_text = textwrap.fill(
        content, width=max_width // font.size)
    content = wrapped_text
    lines = wrapped_text.split("\n")
    height = 0
    width = 0
    
    for line in lines:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]

        width = max(width, line_width)
        height += line_height
        
    return width, height,content