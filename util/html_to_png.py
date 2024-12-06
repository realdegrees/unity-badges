from PIL import Image
import io
from playwright.async_api import async_playwright
import asyncio

async def html_to_png(html_content) -> io.BytesIO:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            handle_sighup=False,
            handle_sigint=False,
            handle_sigterm=False,
            headless=True,
            # executable_path='/usr/bin/chromium-browser',
        )
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1200, "height": 3000})
        await page.set_content(html_content)
        screenshot = await page.screenshot(omit_background=True)
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
