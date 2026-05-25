"""Data models for content objects — shared across agents"""

from pydantic import BaseModel
from typing import List


class ContentTopic(BaseModel):
    """Research output — a trending topic"""
    topic: str
    why_trending: str
    hook_angle: str
    recommended_format: str  # "reel" | "carousel" | "post" | "all"
    pain_point: str
    title_options: List[str]
    priority_score: int  # 1-10


class ReelScript(BaseModel):
    """Script for a video reel"""
    topic: str
    hook: str           # 0-3 seconds
    problem: str        # 3-15 seconds
    value: str          # 15-40 seconds
    cta: str            # last 5 seconds
    full_script: str    # complete script for TTS
    word_count: int


class CarouselSlide(BaseModel):
    """Single carousel slide copy"""
    slide_number: int
    headline: str       # max 8 words
    body: str           # max 40 words


class ContentPackage(BaseModel):
    """Complete content package for a topic"""
    topic: ContentTopic
    reel_script: ReelScript
    carousel_slides: List[CarouselSlide]
    caption: str
    hashtags: List[str]
