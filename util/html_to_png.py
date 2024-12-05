from pyppeteer import launch
from PIL import Image
import io


async def html_to_png(html_content) -> io.BytesIO:
    """Render HTML content to PNG, then trim the transparent borders."""
    browser = await launch(
        headless=True,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
    )
    page = await browser.newPage()
    await page.setContent(html_content)

    # Capture the page as PNG with transparent background
    screenshot = await page.screenshot(omitBackground=True)
    await browser.close()
    
    # Convert the screenshot to a PIL image for processing
    img = Image.open(io.BytesIO(screenshot))

    # Crop the image to the bounding box of non-transparent pixels
    img = img.convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox) 

    # Save or return the trimmed image
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output