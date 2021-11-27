from driver_class import Renderer
from playwright.async_api import async_playwright


class PDFRenderer(Renderer):
    async def render(self, data: str) -> bytes:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("about:blank")
            # f-string cannot contain a backslash, so not using f-string.
            await page.evaluate(
                "document.body.innerHTML = `" + data.replace("`", "\\`") + "`"
            )
            raw_pdf = await page.pdf(display_header_footer=False)
            return raw_pdf
