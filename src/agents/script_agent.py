"""Script Agent — generates all written content (reels, carousels, captions)"""

import json
import re
from openai import OpenAI
from typing import List, Tuple
from ..core.config import settings
from ..core.models import ContentTopic, ReelScript, CarouselSlide, ContentPackage
from ..utils.logger import get_logger

logger = get_logger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def parse_json_safely(content: str, max_retries: int = 3) -> dict:
    """Safely parse JSON with automatic error recovery"""
    content = content.strip()
    content = content.strip("```json").strip("```").strip()

    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error at position {e.pos}: {e.msg}")

    # Try to fix common JSON issues
    for attempt in range(max_retries):
        try:
            # Fix missing commas between fields
            content_fixed = re.sub(r'"\s*:\s*"([^"]*?)"\s*"(\w+)"', r'": "\1", "\2"', content)

            # Fix missing commas after closing braces
            content_fixed = re.sub(r'}\s*"', '}, "', content_fixed)
            content_fixed = re.sub(r']\s*"', '], "', content_fixed)

            # Remove trailing commas
            content_fixed = re.sub(r',\s*}', '}', content_fixed)
            content_fixed = re.sub(r',\s*]', ']', content_fixed)

            return json.loads(content_fixed)
        except json.JSONDecodeError:
            logger.warning(f"Retry {attempt + 1}/{max_retries} failed")
            continue

    # Last resort: try to extract valid JSON from the content
    try:
        # Find JSON array or object
        match = re.search(r'\[.*\]|\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    # If all fails, raise with more context
    logger.error(f"Failed to parse JSON after {max_retries} retries. Content: {content[:500]}")
    raise json.JSONDecodeError("All JSON parsing attempts failed", content, 0)


class ScriptAgent:
    def __init__(self):
        self.model = "gpt-4o-mini-search-preview-2025-03-11"

    def write_reel_script(self, topic: ContentTopic, duration: int = 45) -> ReelScript:
        """Write a reel script for the given topic and duration"""
        logger.info(f"Writing {duration}s reel script for: {topic.topic}")

        max_words = {30: 70, 45: 110, 60: 145}.get(duration, 110)

        prompt = f"""
You are a short-form video scriptwriter specialising in {settings.NICHE}.

Write a {duration}-second Instagram Reel script for:
Topic: {topic.topic}
Hook angle: {topic.hook_angle}
Audience pain point: {topic.pain_point}
Brand voice: {settings.BRAND_VOICE}

Structure your response as JSON with these exact keys:
- hook: the opening 0-3 second line (single punchy sentence, pattern interrupt)
- problem: the pain point expansion 3-15 seconds (2-3 short sentences)
- value: the insight/solution 15-{duration-5} seconds (3-4 key points, fast delivery)
- cta: the final 5-second call to action (specific, not generic)
- full_script: the complete script as one block for text-to-speech
- word_count: integer word count of full_script

Rules for full_script:
- Max {max_words} words
- Every sentence max 10 words
- Start with the hook, no intro
- Use "you" not "people"
- No filler words: so, like, basically, actually, right
- Add [PAUSE] where the speaker should breathe
- CAPITALISE words that need emphasis
- Write exactly as spoken — conversational
        """

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Return only valid JSON. No markdown."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        script_data = parse_json_safely(content)

        # Fix malformed data where fields are lists instead of strings
        for key in ["hook", "problem", "value", "cta", "full_script"]:
            if key in script_data and isinstance(script_data[key], list):
                script_data[key] = " ".join(script_data[key])

        script_data["topic"] = topic.topic
        return ReelScript(**script_data)

    def write_carousel(self, topic: ContentTopic) -> List[CarouselSlide]:
        """Write 6-slide carousel copy"""
        logger.info(f"Writing carousel for: {topic.topic}")

        prompt = f"""
Write a 6-slide Instagram carousel for: {topic.topic}
Audience: {settings.TARGET_AUDIENCE}
Brand voice: {settings.BRAND_VOICE}

Return a JSON array of 6 objects, each with:
- slide_number: 1 through 6
- headline: max 8 words, bold hook
- body: max 40 words, conversational explanation

Slide structure:
1. Title card — bold hook headline + expansion sub-line
2. The problem — name the pain point vividly
3. Insight one — one key idea + short explanation
4. Insight two — one key idea + short explanation
5. Insight three — one key idea + short explanation
6. CTA — "Save this. Share it. Follow for more {settings.NICHE} tips."

Keep each slide scannable in 5 seconds.
        """

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Return only valid JSON array. No markdown."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        data = parse_json_safely(content)
        slides_data = data if isinstance(data, list) else data.get("slides", data)
        return [CarouselSlide(**s) for s in slides_data]

    def write_caption(self, topic: ContentTopic, reel_script: ReelScript) -> Tuple[str, List[str]]:
        """Write Instagram caption + hashtag set"""
        logger.info(f"Writing caption for: {topic.topic}")

        prompt = f"""
Write an Instagram caption and hashtag set for this content:
Topic: {topic.topic}
Hook: {reel_script.hook}
Audience: {settings.TARGET_AUDIENCE}

Return JSON with:
- caption: the full caption (first 3 lines are most important — make them grab attention before "more" fold. Then expand. End with a question to drive comments. Max 300 words.)
- hashtags: array of 30 hashtags (mix: 5 large >1M, 15 medium 100k-1M, 10 niche <100k)

The first line of caption must mirror the reel hook or make a bold claim.
Do NOT start with emojis on the first line.
        """

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Return only valid JSON. No markdown."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        data = parse_json_safely(content)
        return data["caption"], data["hashtags"]

    def create_content_package(self, topic: ContentTopic) -> ContentPackage:
        """Create the full content package for a topic"""
        logger.info(f"Creating full content package for: {topic.topic}")

        reel_script = self.write_reel_script(topic)
        carousel_slides = self.write_carousel(topic)
        caption, hashtags = self.write_caption(topic, reel_script)

        return ContentPackage(
            topic=topic,
            reel_script=reel_script,
            carousel_slides=carousel_slides,
            caption=caption,
            hashtags=hashtags
        )
