"""Carousel Agent — renders branded carousel slides as JPG images using Pyppeteer"""

import asyncio
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..core.config import settings
from ..core.models import ContentPackage
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CarouselAgent:
    def __init__(self):
        self.template_dir = Path("src/templates")
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    async def render_slide_async(self, html: str, output_path: Path) -> Path:
        """Render HTML to JPG using headless browser via Pyppeteer"""
        try:
            from pyppeteer import launch
        except ImportError:
            logger.error("Pyppeteer not installed. Install with: pip install pyppeteer")
            raise

        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = await browser.newPage()
        await page.setViewport({"width": 1080, "height": 1080})
        await page.setContent(html, waitUntil="networkidle0")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot({
            "path": str(output_path),
            "type": "jpeg",
            "quality": 95,
            "fullPage": False
        })

        await browser.close()
        return output_path

    def render_carousel(self, package: ContentPackage, output_dir: Path) -> list:
        """Render all carousel slides"""
        logger.info(f"Rendering carousel for: {package.topic.topic}")

        template = self.env.get_template("carousel_template.html")
        slide_paths = []

        for slide in package.carousel_slides:
            html = template.render(
                headline=slide.headline,
                body=slide.body,
                slide_number=slide.slide_number,
                total_slides=len(package.carousel_slides),
                brand_colors=settings.BRAND_COLORS.split(","),
                niche=settings.NICHE
            )

            output_path = output_dir / f"slide-{slide.slide_number:02d}.jpg"

            try:
                asyncio.get_event_loop().run_until_complete(
                    self.render_slide_async(html, output_path)
                )
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.render_slide_async(html, output_path))
                loop.close()

            slide_paths.append(output_path)
            logger.info(f"  Slide {slide.slide_number} rendered: {output_path}")

        return slide_paths
