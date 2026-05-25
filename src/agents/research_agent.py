"""Research Agent — finds trending topics for your niche using Perplexity API"""

import json
import httpx
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
from ..core.config import settings
from ..core.models import ContentTopic
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ResearchAgent:
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def research_trends(self, niche: str = None, audience: str = None) -> List[ContentTopic]:
        """Fetch trending topics for the configured niche"""
        # Use custom niche/audience if provided, otherwise use defaults
        niche = niche or settings.NICHE
        audience = audience or settings.TARGET_AUDIENCE

        logger.info(f"Researching trends for niche: {niche}")

        prompt = f"""
You are a social media content researcher.

Find the top 5 trending content opportunities THIS WEEK for: {niche}
Target audience: {audience}

For each topic, return a JSON object with these exact keys:
- topic: short punchy topic name (max 6 words)
- why_trending: why this is relevant right now (1 sentence)
- hook_angle: the emotion or curiosity gap to exploit
- recommended_format: one of "reel", "carousel", "post", or "all"
- pain_point: the specific audience pain this addresses
- title_options: array of 3 viral title ideas
- priority_score: integer 1-10 (10 = highest opportunity)

Prioritise topics where:
1. Search intent is rising this week
2. Fewer than 10 high-quality videos exist on the topic
3. The hook angle is emotional or counter-intuitive

Return ONLY a valid JSON array. No markdown, no explanation.
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Return only valid JSON arrays. No markdown."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        content = content.strip().strip("```json").strip("```").strip()
        topics_data = json.loads(content)

        topics = [ContentTopic(**t) for t in topics_data]
        logger.info(f"Found {len(topics)} trending topics")

        return sorted(topics, key=lambda x: x.priority_score, reverse=True)
