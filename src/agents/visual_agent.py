"""Visual Agent — generates background images for reels and carousel frames using DALL-E 3"""

import httpx
from pathlib import Path
from openai import OpenAI
from ..core.config import settings
from ..core.models import ContentPackage
from ..utils.logger import get_logger

logger = get_logger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class VisualAgent:
    def generate_visual_prompt(self, package: ContentPackage, format: str = "reel") -> str:
        """Ask GPT-4o to write an optimised DALL-E prompt based on the script"""

        size_desc = "vertical 9:16 portrait" if format == "reel" else "square 1:1"

        prompt = f"""
Write a DALL-E 3 image generation prompt for a {size_desc} background image.

Content topic: {package.topic.topic}
Script hook: {package.reel_script.hook}
Mood/feeling: {package.topic.hook_angle}
Brand colors: {settings.BRAND_COLORS}

Requirements:
- No text, no words, no letters in the image
- The image will have white text overlaid — needs visual breathing room
- Photographic or cinematic quality, not illustrative
- Colors should evoke: {package.topic.hook_angle}
- High contrast areas should be in top and bottom thirds (where text will sit)
- Style: modern, professional, Instagram-worthy

Return ONLY the DALL-E prompt. No explanation.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview-2025-03-11",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def generate_reel_background(self, package: ContentPackage, output_path: Path) -> Path:
        """Generate 9:16 background image for reel"""
        logger.info(f"Generating reel background for: {package.topic.topic}")

        dalle_prompt = self.generate_visual_prompt(package, format="reel")
        logger.info(f"DALL-E prompt: {dalle_prompt[:100]}...")

        response = client.images.generate(
            model="dall-e-2",
            prompt=dalle_prompt,
            size="1024x1792",
            n=1
        )

        image_url = response.data[0].url

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with httpx.Client() as http_client:
            img_response = http_client.get(image_url)
            img_response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(img_response.content)

        logger.info(f"Background saved: {output_path}")
        return output_path

    def generate_post_image(self, package: ContentPackage, output_path: Path) -> Path:
        """Generate 1:1 square image for static post"""
        logger.info(f"Generating post image for: {package.topic.topic}")

        dalle_prompt = self.generate_visual_prompt(package, format="post")

        response = client.images.generate(
            model="dall-e-2",
            prompt=dalle_prompt,
            size="1024x1024",
            n=1
        )

        image_url = response.data[0].url

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with httpx.Client() as http_client:
            img_response = http_client.get(image_url)

        with open(output_path, "wb") as f:
            f.write(img_response.content)

        logger.info(f"Post image saved: {output_path}")
        return output_path
