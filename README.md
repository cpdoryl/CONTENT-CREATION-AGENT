# 🤖 Social Media Content Agent

> **Fully automated content production pipeline** — researches trends, writes scripts, generates voiceovers via ElevenLabs, creates visuals, assembles Reels/Shorts, packages carousels and posts, and drops everything in your Google Drive. You only schedule.

---

## 📋 Table of Contents

- [What This Agent Does](#what-this-agent-does)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [API Keys Setup](#api-keys-setup)
- [Agent Modules — Build Order](#agent-modules--build-order)
  - [Module 1 — Research Agent](#module-1--research-agent)
  - [Module 2 — Script Writing Agent](#module-2--script-writing-agent)
  - [Module 3 — ElevenLabs Voiceover Agent](#module-3--elevenlabs-voiceover-agent)
  - [Module 4 — Visual Generation Agent](#module-4--visual-generation-agent)
  - [Module 5 — Video Assembly Agent](#module-5--video-assembly-agent)
  - [Module 6 — Carousel Builder Agent](#module-6--carousel-builder-agent)
  - [Module 7 — Packager + Notifier Agent](#module-7--packager--notifier-agent)
- [Running the Agent](#running-the-agent)
- [VS Code Setup & Extensions](#vs-code-setup--extensions)
- [Workflow Automation (Scheduler)](#workflow-automation-scheduler)
- [Output Folder Structure](#output-folder-structure)
- [Customisation Guide](#customisation-guide)
- [Cost Reference](#cost-reference)
- [Troubleshooting](#troubleshooting)

---

## What This Agent Does

```
Your brief (topic / niche / goal)
        ↓
  Research Agent  →  trending topics, hooks, competitor analysis
        ↓
  Script Agent    →  reel scripts, carousel copy, captions, hashtags
        ↓
  Voice Agent     →  ElevenLabs TTS → MP3 voiceover per script
        ↓
  Visual Agent    →  DALL-E 3 background images (9:16 + 1:1)
        ↓
  Video Agent     →  MP4 assembly (audio + visuals + burned captions)
        ↓
  Carousel Agent  →  6-slide JPG sets with your brand template
        ↓
  Packager        →  organised Drive folder + Telegram notification
        ↓
  YOU             →  review in 30 min → schedule in Buffer / Later
```

**Weekly output (default config):** 5 Reels (MP4 9:16), 5 YouTube Shorts (same MP4), 3 carousels (6 JPGs each), 5 static posts (JPG 1:1), captions + hashtag sets for everything.

---

## Architecture Overview

```
src/
├── agents/
│   ├── research_agent.py       ← Perplexity API + Apify scraping
│   ├── script_agent.py         ← GPT-4o script + carousel + caption writer
│   ├── voice_agent.py          ← ElevenLabs TTS API
│   ├── visual_agent.py         ← DALL-E 3 / Stability AI image gen
│   ├── video_agent.py          ← FFmpeg / JSON2Video assembly
│   ├── carousel_agent.py       ← HTML-to-image carousel renderer
│   └── packager_agent.py       ← Drive upload + Telegram notify
├── core/
│   ├── orchestrator.py         ← runs all agents in sequence
│   ├── config.py               ← loads .env, validates keys
│   └── models.py               ← Pydantic models for content objects
├── prompts/
│   ├── research_prompts.py
│   ├── script_prompts.py
│   └── caption_prompts.py
├── templates/
│   ├── carousel_template.html  ← branded Jinja2 carousel template
│   └── post_template.html      ← static post template
├── utils/
│   ├── drive_uploader.py
│   ├── file_utils.py
│   └── logger.py
├── scheduler.py                ← APScheduler weekly trigger
├── main.py                     ← entry point
├── requirements.txt
├── .env.example
└── README.md                   ← this file
```

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | Use pyenv or system Python |
| VS Code | Latest | with Python + Pylance extensions |
| FFmpeg | 6.0+ | for video assembly |
| Node.js | 18+ | for Puppeteer (carousel renderer) |
| Git | Any | for version control |

**API accounts needed (all have free tiers to start):**

| Service | Purpose | Sign up |
|---------|---------|--------|
| OpenAI | GPT-4o scripts | platform.openai.com |
| ElevenLabs | Voiceover TTS | elevenlabs.io |
| Perplexity | Trend research | perplexity.ai/pro |
| DALL-E 3 (via OpenAI) | Background images | same as OpenAI |
| Google Cloud | Drive API | console.cloud.google.com |
| Telegram | Notifications | t.me/BotFather |
| Apify *(optional)* | YouTube scraping | apify.com |
| JSON2Video *(optional)* | Video assembly no-code | json2video.com |

---

## Project Structure

Open VS Code and create this project:

```bash
# In VS Code terminal (Ctrl+` to open)
mkdir social-content-agent
cd social-content-agent
git init
code .
```

Then create the folder structure:

```bash
mkdir -p src/agents src/core src/prompts src/templates src/utils output
touch src/agents/__init__.py src/core/__init__.py src/prompts/__init__.py src/utils/__init__.py
touch main.py scheduler.py requirements.txt .env.example .gitignore
```

Add to `.gitignore`:

```gitignore
.env
output/
__pycache__/
*.pyc
.venv/
node_modules/
*.mp3
*.mp4
*.jpg
*.png
```

---

## Environment Setup

### Step 1 — Create virtual environment

```bash
# In VS Code terminal
python -m venv .venv

# Activate (Mac/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# You should see (.venv) in your terminal prompt
```

### Step 2 — Install FFmpeg

```bash
# Mac
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows — download from ffmpeg.org and add to PATH
# Then verify:
ffmpeg -version
```

### Step 3 — Install Node.js + Puppeteer (for carousel rendering)

```bash
# Install Node.js from nodejs.org, then:
npm install -g puppeteer
```

---

## Installation

### `requirements.txt`

```txt
# Core agent framework
openai>=1.30.0
langchain>=0.2.0
langchain-openai>=0.1.0

# ElevenLabs voiceover
elevenlabs>=1.2.0

# Research
requests>=2.31.0
httpx>=0.27.0

# Google Drive
google-auth>=2.29.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.130.0

# Image processing
Pillow>=10.3.0

# HTML to image (carousel)
pyppeteer>=1.0.2
jinja2>=3.1.4

# Video processing
ffmpeg-python>=0.2.0

# Scheduling
APScheduler>=3.10.4

# Config & validation
pydantic>=2.7.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.1

# Utilities
rich>=13.7.1
tenacity>=8.3.0
```

Install everything:

```bash
pip install -r requirements.txt
```

---

## API Keys Setup

### `.env.example` → copy to `.env`

```bash
cp .env.example .env
```

**`.env.example`** (copy this exactly, fill in your keys):

```env
# ── OpenAI (GPT-4o scripts + DALL-E 3 images) ────────────────────────────
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── ElevenLabs (voiceover) ───────────────────────────────────────────────
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
# Find your voice ID at: elevenlabs.io/voice-lab
# Clone your own voice: elevenlabs.io/voice-cloning

# ── Perplexity (research) ────────────────────────────────────────────────
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Google Drive ─────────────────────────────────────────────────────────
GOOGLE_CREDENTIALS_PATH=credentials/google_credentials.json
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id_here
# Get folder ID from the URL when you open the folder in Drive

# ── Telegram (notifications) ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=123456789
# Create bot: message @BotFather on Telegram → /newbot
# Get chat ID: message @userinfobot

# ── Apify (optional — YouTube/Reddit trend scraping) ─────────────────────
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── JSON2Video (optional — no-code video assembly) ───────────────────────
JSON2VIDEO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Content Configuration ────────────────────────────────────────────────
NICHE=personal finance for millennials
TARGET_AUDIENCE=25-35 year olds struggling with saving and investing
BRAND_VOICE=calm, direct, educational, uses simple words, no jargon
BRAND_COLORS=#1D9E75,#06132B,#F5F4F0
CONTENT_PER_WEEK=5
OUTPUT_DIR=output
```

### Setting up Google Drive API

```bash
# 1. Go to console.cloud.google.com
# 2. Create new project → "ContentAgent"
# 3. Enable Google Drive API
# 4. Create credentials → OAuth 2.0 Client ID → Desktop app
# 5. Download JSON → save as credentials/google_credentials.json
mkdir credentials
# Move downloaded file to credentials/google_credentials.json

# First run will open browser for OAuth consent
```

### Setting up Telegram Bot

```
1. Open Telegram → search @BotFather
2. Send: /newbot
3. Follow prompts → get your BOT_TOKEN
4. Start a chat with your new bot
5. Visit: https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates
6. Send a message to your bot, refresh the URL
7. Copy the "id" field from "chat" → that's your CHAT_ID
```

---

## Agent Modules — Build Order

Build and test each module individually before connecting them. Use VS Code's built-in debugger (`F5`) to step through each one.

---

### Module 1 — Research Agent

**File:** `src/agents/research_agent.py`

```python
"""
Research Agent — finds trending topics for your niche
Uses Perplexity API for real-time web search + trend analysis
"""

import json
import httpx
from typing import List
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ContentTopic(BaseModel):
    topic: str
    why_trending: str
    hook_angle: str
    recommended_format: str  # "reel" | "carousel" | "post" | "all"
    pain_point: str
    title_options: List[str]
    priority_score: int  # 1-10


class ResearchAgent:
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def research_trends(self) -> List[ContentTopic]:
        """Fetch trending topics for the configured niche"""
        logger.info(f"Researching trends for niche: {settings.NICHE}")

        prompt = f"""
        You are a social media content researcher.
        
        Find the top 5 trending content opportunities THIS WEEK for: {settings.NICHE}
        Target audience: {settings.TARGET_AUDIENCE}
        
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
            "model": "sonar-medium-online",  # has real-time web access
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

        # Clean any accidental markdown code fences
        content = content.strip().strip("```json").strip("```").strip()
        topics_data = json.loads(content)

        topics = [ContentTopic(**t) for t in topics_data]
        logger.info(f"Found {len(topics)} trending topics")

        # Sort by priority score
        return sorted(topics, key=lambda x: x.priority_score, reverse=True)
```

**Test it:**

```bash
# In VS Code terminal, with .venv active:
python -c "
from src.agents.research_agent import ResearchAgent
agent = ResearchAgent()
topics = agent.research_trends()
for t in topics:
    print(f'[{t.priority_score}/10] {t.topic} — {t.recommended_format}')
"
```

---

### Module 2 — Script Writing Agent

**File:** `src/agents/script_agent.py`

```python
"""
Script Writing Agent — generates all written content
- 30/45/60-sec reel scripts
- 6-slide carousel copy
- Instagram captions + hashtags
"""

from openai import OpenAI
from pydantic import BaseModel
from typing import List
from ..core.config import settings
from ..agents.research_agent import ContentTopic
from ..utils.logger import get_logger

logger = get_logger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class ReelScript(BaseModel):
    topic: str
    hook: str           # 0-3 seconds
    problem: str        # 3-15 seconds
    value: str          # 15-40 seconds
    cta: str            # last 5 seconds
    full_script: str    # complete script for TTS
    word_count: int


class CarouselSlide(BaseModel):
    slide_number: int
    headline: str       # max 8 words
    body: str           # max 40 words


class ContentPackage(BaseModel):
    topic: ContentTopic
    reel_script: ReelScript
    carousel_slides: List[CarouselSlide]
    caption: str
    hashtags: List[str]


class ScriptAgent:
    def __init__(self):
        self.model = "gpt-4o"

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
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        data = response.choices[0].message.content
        import json
        script_data = json.loads(data)
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
            ],
            temperature=0.6,
            response_format={"type": "json_object"}
        )

        import json
        data = json.loads(response.choices[0].message.content)
        slides_data = data.get("slides", data)
        return [CarouselSlide(**s) for s in slides_data]

    def write_caption(self, topic: ContentTopic, reel_script: ReelScript) -> tuple[str, List[str]]:
        """Write Instagram caption + hashtag set"""
        prompt = f"""
Write an Instagram caption and hashtag set for this content:
Topic: {topic.topic}
Hook: {reel_script.hook}
Audience: {settings.TARGET_AUDIENCE}

Return JSON with:
- caption: the full caption (first 3 lines are most important — make them grab attention before 
  "more" fold. Then expand. End with a question to drive comments. Max 300 words.)
- hashtags: array of 30 hashtags (mix: 5 large >1M, 15 medium 100k-1M, 10 niche <100k)

The first line of caption must mirror the reel hook or make a bold claim.
Do NOT start with emojis on the first line.
        """

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Return only valid JSON. No markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            response_format={"type": "json_object"}
        )

        import json
        data = json.loads(response.choices[0].message.content)
        return data["caption"], data["hashtags"]

    def create_content_package(self, topic: ContentTopic) -> ContentPackage:
        """Create the full content package for a topic"""
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
```

---

### Module 3 — ElevenLabs Voiceover Agent

**File:** `src/agents/voice_agent.py`

```python
"""
Voice Agent — converts scripts to MP3 using ElevenLabs TTS API
Handles voice settings, error retry, and file output
"""

import httpx
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VoiceAgent:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID
        self.base_url = "https://api.elevenlabs.io/v1"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_voiceover(
        self,
        script: str,
        output_path: Path,
        stability: float = 0.5,
        similarity_boost: float = 0.85,
        style: float = 0.4
    ) -> Path:
        """
        Convert script to MP3 voiceover.
        
        Voice settings guide:
        - stability: 0.3 = expressive/dynamic, 0.8 = consistent/steady
          → Use 0.4 for energetic content, 0.6 for educational content
        - similarity_boost: how close to reference voice (0.75-0.95)
        - style: how dramatic the delivery (0.2 = neutral, 0.8 = theatrical)
          → Use 0.3 for calm educational, 0.5 for motivational reels
        """
        logger.info(f"Generating voiceover: {output_path.name}")

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        payload = {
            "text": script,
            "model_id": "eleven_turbo_v2",  # fastest + cheapest, great quality
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": True
            }
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/text-to-speech/{self.voice_id}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Voiceover saved: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
        return output_path

    def get_audio_duration(self, mp3_path: Path) -> float:
        """Get duration of MP3 in seconds using ffmpeg"""
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
            capture_output=True, text=True
        )
        return float(result.stdout.strip())

    def get_remaining_characters(self) -> dict:
        """Check ElevenLabs quota remaining"""
        headers = {"xi-api-key": self.api_key}
        with httpx.Client() as client:
            response = client.get(f"{self.base_url}/user/subscription", headers=headers)
        data = response.json()
        return {
            "used": data.get("character_count", 0),
            "limit": data.get("character_limit", 0),
            "remaining": data.get("character_limit", 0) - data.get("character_count", 0)
        }
```

**Test it:**

```bash
python -c "
from pathlib import Path
from src.agents.voice_agent import VoiceAgent
agent = VoiceAgent()
quota = agent.get_remaining_characters()
print(f'Quota remaining: {quota[\"remaining\"]:,} characters')
agent.generate_voiceover(
    'This is a test. Your content agent is working correctly.',
    Path('output/test_voice.mp3')
)
print('test_voice.mp3 created — play it to check quality')
"
```

---

### Module 4 — Visual Generation Agent

**File:** `src/agents/visual_agent.py`

```python
"""
Visual Agent — generates background images for reels and carousel frames
Uses DALL-E 3 via OpenAI API
"""

import httpx
from pathlib import Path
from openai import OpenAI
from ..core.config import settings
from ..agents.script_agent import ContentPackage
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
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def generate_reel_background(self, package: ContentPackage, output_path: Path) -> Path:
        """Generate 9:16 background image for reel"""
        logger.info(f"Generating reel background for: {package.topic.topic}")

        dalle_prompt = self.generate_visual_prompt(package, format="reel")

        response = client.images.generate(
            model="dall-e-3",
            prompt=dalle_prompt,
            size="1024x1792",   # 9:16 vertical
            quality="standard", # use "hd" for premium quality ($0.08/image)
            n=1
        )

        image_url = response.data[0].url

        # Download and save
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
            model="dall-e-3",
            prompt=dalle_prompt,
            size="1024x1024",   # 1:1 square
            quality="standard",
            n=1
        )

        image_url = response.data[0].url

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with httpx.Client() as http_client:
            img_response = http_client.get(image_url)
        with open(output_path, "wb") as f:
            f.write(img_response.content)

        return output_path
```

---

### Module 5 — Video Assembly Agent

**File:** `src/agents/video_agent.py`

```python
"""
Video Assembly Agent — combines voiceover + background + captions into MP4
Uses FFmpeg for local assembly (free) or JSON2Video API (easier)
"""

import subprocess
import json
import httpx
from pathlib import Path
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VideoAgent:
    def assemble_reel_ffmpeg(
        self,
        background_image: Path,
        voiceover_mp3: Path,
        output_path: Path,
        subtitle_text: str = None
    ) -> Path:
        """
        Assemble reel using local FFmpeg.
        Free, no API limits, requires FFmpeg installed.
        Output: MP4 1080x1920 (Instagram/YouTube Shorts spec)
        """
        logger.info(f"Assembling reel: {output_path.name}")

        # Get audio duration to set video length
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(voiceover_mp3)],
            capture_output=True, text=True
        )
        duration = float(probe.stdout.strip())

        # Write subtitles file if script provided
        srt_path = None
        if subtitle_text:
            srt_path = output_path.parent / f"{output_path.stem}.srt"
            self._create_simple_srt(subtitle_text, duration, srt_path)

        # Build FFmpeg command
        cmd = [
            "ffmpeg", "-y",
            # Input: static background image (loop for duration)
            "-loop", "1",
            "-i", str(background_image),
            # Input: voiceover audio
            "-i", str(voiceover_mp3),
            # Scale to 1080x1920 (9:16 Instagram/Shorts spec)
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            # Match video length to audio
            "-t", str(duration),
            # Video codec settings
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            # Audio codec
            "-c:a", "aac",
            "-b:a", "192k",
            # Pixel format for compatibility
            "-pix_fmt", "yuv420p",
            # Output
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"Video assembly failed: {result.stderr}")

        logger.info(f"Reel assembled: {output_path} ({output_path.stat().st_size / 1024 / 1024:.1f} MB)")
        return output_path

    def assemble_reel_json2video(
        self,
        background_image_url: str,
        voiceover_url: str,
        output_path: Path,
        api_key: str = None
    ) -> Path:
        """
        Assemble using JSON2Video API (json2video.com).
        Easier than FFmpeg, handles captions automatically.
        Cost: ~$0.05 per video.
        """
        api_key = api_key or settings.JSON2VIDEO_API_KEY
        logger.info("Assembling reel via JSON2Video API")

        template = {
            "resolution": "instagram-story",  # 1080x1920
            "quality": "high",
            "fps": 30,
            "scenes": [{
                "comment": "Main scene",
                "elements": [
                    {
                        "type": "image",
                        "src": background_image_url,
                        "x": 0, "y": 0,
                        "width": "100%", "height": "100%",
                        "z-index": 0
                    },
                    {
                        "type": "audio",
                        "src": voiceover_url,
                        "volume": 1.0
                    },
                    {
                        "type": "subtitles",
                        "src": voiceover_url,
                        "font-size": 38,
                        "font-weight": "bold",
                        "color": "#FFFFFF",
                        "background": "rgba(0,0,0,0.55)",
                        "border-radius": 8,
                        "padding": 10,
                        "y": "75%",
                        "width": "90%",
                        "x": "5%",
                        "z-index": 10,
                        "max-words-per-line": 5
                    }
                ]
            }]
        }

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

        with httpx.Client(timeout=120.0) as client:
            # Start render
            response = client.post(
                "https://api.json2video.com/v2/movies",
                headers=headers,
                json=template
            )
            response.raise_for_status()
            movie_id = response.json()["movie"]

            # Poll for completion
            import time
            for _ in range(60):
                time.sleep(5)
                status_response = client.get(
                    f"https://api.json2video.com/v2/movies?movie={movie_id}",
                    headers=headers
                )
                status_data = status_response.json()
                status = status_data.get("movie", {}).get("status")
                if status == "done":
                    video_url = status_data["movie"]["url"]
                    break
                elif status == "error":
                    raise RuntimeError(f"JSON2Video render failed: {status_data}")

        # Download final video
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with httpx.Client() as client:
            video_response = client.get(video_url)
        with open(output_path, "wb") as f:
            f.write(video_response.content)

        return output_path

    def _create_simple_srt(self, text: str, duration: float, srt_path: Path):
        """Create a basic SRT subtitle file from script text"""
        words = text.split()
        words_per_chunk = 5
        chunks = [" ".join(words[i:i+words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
        chunk_duration = duration / len(chunks)

        srt_content = ""
        for i, chunk in enumerate(chunks):
            start = i * chunk_duration
            end = (i + 1) * chunk_duration
            srt_content += f"{i+1}\n"
            srt_content += f"{self._sec_to_srt(start)} --> {self._sec_to_srt(end)}\n"
            srt_content += f"{chunk}\n\n"

        with open(srt_path, "w") as f:
            f.write(srt_content)

    def _sec_to_srt(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

---

### Module 6 — Carousel Builder Agent

**File:** `src/agents/carousel_agent.py`

```python
"""
Carousel Agent — renders branded carousel slides as JPG images
Uses Jinja2 HTML templates + Pyppeteer (headless Chrome) to render
"""

import asyncio
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from pyppeteer import launch
from ..core.config import settings
from ..agents.script_agent import ContentPackage
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CarouselAgent:
    def __init__(self):
        self.template_dir = Path("src/templates")
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    async def render_slide_async(self, html: str, output_path: Path) -> Path:
        """Render HTML to JPG using headless Chrome"""
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

    def render_carousel(self, package: ContentPackage, output_dir: Path) -> list[Path]:
        """Render all 6 carousel slides"""
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
            asyncio.get_event_loop().run_until_complete(
                self.render_slide_async(html, output_path)
            )
            slide_paths.append(output_path)
            logger.info(f"  Slide {slide.slide_number} rendered")

        return slide_paths
```

**File:** `src/templates/carousel_template.html`

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px;
    height: 1080px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: {{ brand_colors[1] if brand_colors|length > 1 else '#06132B' }};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: white;
    padding: 80px;
    position: relative;
    overflow: hidden;
  }
  .slide-number {
    position: absolute;
    top: 40px;
    right: 50px;
    font-size: 24px;
    opacity: 0.4;
    letter-spacing: 2px;
  }
  .accent-bar {
    width: 60px;
    height: 6px;
    background: {{ brand_colors[0] if brand_colors else '#1D9E75' }};
    border-radius: 3px;
    margin-bottom: 40px;
  }
  .headline {
    font-size: 68px;
    font-weight: 700;
    line-height: 1.1;
    text-align: center;
    margin-bottom: 40px;
    letter-spacing: -1px;
  }
  .body {
    font-size: 34px;
    line-height: 1.5;
    text-align: center;
    opacity: 0.85;
    max-width: 900px;
  }
  .brand-tag {
    position: absolute;
    bottom: 40px;
    font-size: 22px;
    opacity: 0.4;
    letter-spacing: 3px;
    text-transform: uppercase;
  }
</style>
</head>
<body>
  <div class="slide-number">{{ slide_number }}/{{ total_slides }}</div>
  <div class="accent-bar"></div>
  <div class="headline">{{ headline }}</div>
  <div class="body">{{ body }}</div>
  <div class="brand-tag">{{ niche }}</div>
</body>
</html>
```

---

### Module 7 — Packager + Notifier Agent

**File:** `src/agents/packager_agent.py`

```python
"""
Packager Agent — organises outputs + uploads to Google Drive + sends Telegram notification
"""

import json
import httpx
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from ..core.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class PackagerAgent:
    def __init__(self):
        self.drive_service = self._get_drive_service()
        self.week_label = datetime.now().strftime("%Y-W%V")

    def _get_drive_service(self):
        """Authenticate with Google Drive"""
        creds = None
        token_path = Path("credentials/token.json")

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, "w") as f:
                f.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def create_week_folder(self, parent_folder_id: str, subfolder: str) -> str:
        """Create week/subfolder in Drive, return folder ID"""
        folder_name = f"{self.week_label}/{subfolder}"

        metadata = {
            "name": subfolder,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id]
        }
        folder = self.drive_service.files().create(
            body=metadata, fields="id"
        ).execute()
        return folder["id"]

    def upload_file(self, file_path: Path, folder_id: str) -> str:
        """Upload file to Google Drive folder, return file URL"""
        mime_types = {
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".txt": "text/plain"
        }
        mime_type = mime_types.get(file_path.suffix.lower(), "application/octet-stream")

        metadata = {"name": file_path.name, "parents": [folder_id]}
        media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)

        file = self.drive_service.files().create(
            body=metadata, media_body=media, fields="id,webViewLink"
        ).execute()

        return file.get("webViewLink", "")

    def save_caption_file(self, topic_slug: str, caption: str, hashtags: list, output_dir: Path):
        """Save caption and hashtags as text files"""
        caption_path = output_dir / f"{topic_slug}_caption.txt"
        hashtag_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)

        with open(caption_path, "w") as f:
            f.write(f"CAPTION:\n{caption}\n\n")
            f.write(f"HASHTAGS:\n{hashtag_str}\n")

        return caption_path

    def send_telegram_notification(self, summary: dict):
        """Send Telegram message when content is ready"""
        lines = [
            f"✅ *Week {self.week_label} content is ready*",
            "",
            f"📱 *Reels/Shorts:* {summary.get('reels', 0)}",
            f"📊 *Carousels:* {summary.get('carousels', 0)}",
            f"🖼 *Static posts:* {summary.get('posts', 0)}",
            "",
            "📁 Check your Google Drive folder to review.",
            "",
            "_Open Drive → review → paste captions → schedule in Buffer_"
        ]

        message = "\n".join(lines)

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        with httpx.Client() as client:
            response = client.post(url, json=payload)
            response.raise_for_status()

        logger.info("Telegram notification sent")
```

---

## Running the Agent

### `src/core/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API Keys
    OPENAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    PERPLEXITY_API_KEY: str
    GOOGLE_CREDENTIALS_PATH: str = "credentials/google_credentials.json"
    GOOGLE_DRIVE_FOLDER_ID: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    APIFY_API_TOKEN: str = ""
    JSON2VIDEO_API_KEY: str = ""

    # Content Config
    NICHE: str = "personal finance"
    TARGET_AUDIENCE: str = "millennials"
    BRAND_VOICE: str = "calm, direct, educational"
    BRAND_COLORS: str = "#1D9E75,#06132B,#F5F4F0"
    CONTENT_PER_WEEK: int = 5
    OUTPUT_DIR: str = "output"

settings = Settings()
```

### `main.py` — the orchestrator

```python
"""
Main orchestrator — runs all agents in sequence
Usage: python main.py
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.agents.research_agent import ResearchAgent
from src.agents.script_agent import ScriptAgent
from src.agents.voice_agent import VoiceAgent
from src.agents.visual_agent import VisualAgent
from src.agents.video_agent import VideoAgent
from src.agents.carousel_agent import CarouselAgent
from src.agents.packager_agent import PackagerAgent
from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger("orchestrator")


def slugify(text: str) -> str:
    """Convert topic name to safe filename"""
    return text.lower().replace(" ", "-").replace("/", "-")[:40]


def run_weekly_production():
    logger.info("=" * 60)
    logger.info("CONTENT AGENT — WEEKLY PRODUCTION RUN STARTED")
    logger.info("=" * 60)

    week = datetime.now().strftime("%Y-W%V")
    output_base = Path(settings.OUTPUT_DIR) / week

    # ── Initialise all agents ──────────────────────────────────────────
    research   = ResearchAgent()
    script     = ScriptAgent()
    voice      = VoiceAgent()
    visual     = VisualAgent()
    video      = VideoAgent()
    carousel   = CarouselAgent()
    packager   = PackagerAgent()

    summary = {"reels": 0, "carousels": 0, "posts": 0}

    # ── Step 1: Research trending topics ──────────────────────────────
    logger.info("\n[1/7] Researching trending topics...")
    topics = research.research_trends()
    topics = topics[:settings.CONTENT_PER_WEEK]
    logger.info(f"      Found {len(topics)} topics to produce")

    # ── Steps 2-6: Produce content for each topic ──────────────────────
    for i, topic in enumerate(topics):
        logger.info(f"\n[Topic {i+1}/{len(topics)}] {topic.topic}")
        slug = slugify(topic.topic)
        topic_dir = output_base / slug

        try:
            # ── Step 2: Write all scripts ──────────────────────────────
            logger.info("  [2/7] Writing scripts...")
            package = script.create_content_package(topic)

            # ── Step 3: Generate voiceover ─────────────────────────────
            logger.info("  [3/7] Generating voiceover...")
            mp3_path = topic_dir / "reels" / f"{slug}-voice.mp3"
            voice.generate_voiceover(
                package.reel_script.full_script,
                mp3_path,
                stability=0.45,     # expressive for reels
                style=0.45
            )

            # ── Step 4: Generate background image ─────────────────────
            logger.info("  [4/7] Generating background image...")
            bg_path = topic_dir / "reels" / f"{slug}-bg.jpg"
            visual.generate_reel_background(package, bg_path)

            # ── Step 5: Assemble reel video ────────────────────────────
            logger.info("  [5/7] Assembling reel video...")
            reel_path = topic_dir / "reels" / f"{slug}-reel.mp4"
            video.assemble_reel_ffmpeg(
                background_image=bg_path,
                voiceover_mp3=mp3_path,
                output_path=reel_path,
                subtitle_text=package.reel_script.full_script
            )
            summary["reels"] += 1

            # ── Step 6: Build carousel ─────────────────────────────────
            logger.info("  [6/7] Building carousel slides...")
            carousel_dir = topic_dir / "carousel"
            carousel.render_carousel(package, carousel_dir)
            summary["carousels"] += 1

            # ── Save static post image ─────────────────────────────────
            post_path = topic_dir / "post" / f"{slug}-post.jpg"
            visual.generate_post_image(package, post_path)
            summary["posts"] += 1

            # ── Save caption + hashtags ────────────────────────────────
            packager.save_caption_file(
                slug,
                package.caption,
                package.hashtags,
                topic_dir
            )

            logger.info(f"  ✅ Topic complete: {topic.topic}")

        except Exception as e:
            logger.error(f"  ❌ Failed for topic '{topic.topic}': {e}")
            continue

    # ── Step 7: Notify ─────────────────────────────────────────────────
    logger.info(f"\n[7/7] Sending notification...")
    if settings.TELEGRAM_BOT_TOKEN:
        packager.send_telegram_notification(summary)

    logger.info("\n" + "=" * 60)
    logger.info(f"PRODUCTION COMPLETE — Week {week}")
    logger.info(f"  Reels: {summary['reels']}  Carousels: {summary['carousels']}  Posts: {summary['posts']}")
    logger.info(f"  Output: {output_base.absolute()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_weekly_production()
```

**Run it:**

```bash
# Manual run (test everything end to end):
python main.py
```

---

## VS Code Setup & Extensions

### Recommended extensions

Install these in VS Code (`Ctrl+Shift+X`):

| Extension | ID | Purpose |
|-----------|-----|---------|
| Python | `ms-python.python` | Python language support |
| Pylance | `ms-python.vscode-pylance` | Type checking, autocomplete |
| Python Debugger | `ms-python.debugpy` | Step-through debugging |
| Python Environments | `ms-python.python` | Virtual env management |
| Ruff | `charliermarsh.ruff` | Fast linting + formatting |
| GitLens | `eamodio.gitlens` | Git history in editor |
| Thunder Client | `rangav.vscode-thunder-client` | Test API calls inline |
| Dotenv | `mikestead.dotenv` | .env syntax highlighting |
| Error Lens | `usernamehw.errorlens` | Inline error messages |

### `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".venv": true,
    "output": true
  }
}
```

### `.vscode/launch.json` (debugger config)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run full agent",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    },
    {
      "name": "Test research agent only",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/test_research_agent.py", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

Press `F5` in VS Code to run with the debugger. Set breakpoints by clicking the gutter next to any line number.

---

## Workflow Automation (Scheduler)

**File:** `scheduler.py`

```python
"""
Scheduler — runs the content agent every Monday at 9:00 AM
Start this once and it runs indefinitely in the background
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from main import run_weekly_production
from src.utils.logger import get_logger

logger = get_logger("scheduler")

scheduler = BlockingScheduler(timezone="Asia/Kolkata")

# Run every Monday at 9:00 AM IST
scheduler.add_job(
    run_weekly_production,
    CronTrigger(day_of_week="mon", hour=9, minute=0),
    id="weekly_content_production",
    name="Weekly Content Production",
    misfire_grace_time=3600  # allow up to 1hr late start
)

if __name__ == "__main__":
    logger.info("Scheduler started — will run every Monday at 9:00 AM IST")
    logger.info("Press Ctrl+C to stop")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")
```

```bash
# Run the scheduler (keep this terminal open or run as a service):
python scheduler.py

# To run as a background service on Mac/Linux:
nohup python scheduler.py > logs/scheduler.log 2>&1 &

# Check it's running:
ps aux | grep scheduler.py
```

---

## Output Folder Structure

After each run, your `output/` directory will look like:

```
output/
└── 2025-W23/
    ├── why-you-cant-save-money/
    │   ├── reels/
    │   │   ├── why-you-cant-save-money-bg.jpg       ← 9:16 background
    │   │   ├── why-you-cant-save-money-voice.mp3    ← ElevenLabs voiceover
    │   │   └── why-you-cant-save-money-reel.mp4     ← FINAL REEL (post to IG + YT)
    │   ├── carousel/
    │   │   ├── slide-01.jpg                          ← title card
    │   │   ├── slide-02.jpg                          ← problem
    │   │   ├── slide-03.jpg                          ← insight 1
    │   │   ├── slide-04.jpg                          ← insight 2
    │   │   ├── slide-05.jpg                          ← insight 3
    │   │   └── slide-06.jpg                          ← CTA
    │   ├── post/
    │   │   └── why-you-cant-save-money-post.jpg      ← 1:1 static post
    │   └── why-you-cant-save-money_caption.txt       ← caption + hashtags
    │
    ├── emergency-fund-myths/
    │   └── ... (same structure)
    │
    └── ... (one folder per topic)
```

---

## Customisation Guide

### Change your voice style

In `main.py`, adjust ElevenLabs voice settings per content type:

```python
# Energetic / motivational reels
voice.generate_voiceover(script, path, stability=0.35, style=0.55)

# Calm / educational content
voice.generate_voiceover(script, path, stability=0.65, style=0.25)

# Storytelling / narrative
voice.generate_voiceover(script, path, stability=0.50, style=0.40)
```

### Change reel duration

In `main.py`:

```python
package = script.create_content_package(topic)
# Change 45 to 30 or 60:
reel_script = script.write_reel_script(topic, duration=30)
```

### Add background music

In `video_agent.py`, add a music mixing step after assembly:

```python
def add_background_music(self, video_path: Path, music_path: Path, volume: float = 0.08) -> Path:
    """Mix background music into assembled reel at low volume"""
    output_path = video_path.parent / f"{video_path.stem}_music.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(music_path),
        "-filter_complex",
        f"[1:a]volume={volume},aloop=loop=-1:size=2e+09[bg];[0:a][bg]amix=inputs=2:duration=first[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    return output_path
```

---

## Cost Reference

| API | Free tier | Starter ($25/mo) | Full ($60/mo) |
|-----|----------|-----------------|--------------|
| OpenAI GPT-4o | $5 credit | ~2,000 scripts | ~5,000 scripts |
| ElevenLabs | 10k chars | Creator $5 (100k chars) | Pro $22 (500k chars) |
| Perplexity | Limited | $5 sonar-medium | $10 unlimited |
| DALL-E 3 | $5 credit | ~125 images | ~300 images |
| FFmpeg (local) | Free | Free | Free |
| Google Drive | Free | Free | Free |
| Telegram | Free | Free | Free |

**At 5 pieces of content per week = ~20/month:**
- Research: ~$3/month (20 API calls)
- Scripts: ~$8/month (60 GPT-4o calls at ~1,500 tokens each)
- Voice: ~$5/month (ElevenLabs Creator plan, ~50k chars/month)
- Images: ~$4/month (20 DALL-E HD images at $0.04 each + 120 DALL-E standard at $0.02)
- **Total: ~$20/month**

---

## Troubleshooting

### ElevenLabs returns 401
```bash
# Check your API key is correct:
curl -H "xi-api-key: YOUR_KEY" https://api.elevenlabs.io/v1/user/subscription
# Should return your subscription info, not an error
```

### FFmpeg not found
```bash
which ffmpeg          # Should return a path
ffmpeg -version       # Should show version info
# If missing: brew install ffmpeg (Mac) or sudo apt install ffmpeg (Linux)
```

### Google Drive authentication fails
```bash
# Delete the cached token and re-authenticate:
rm credentials/token.json
python main.py
# Browser will open for OAuth consent — allow access
```

### DALL-E generates text in images
```
Add to your visual prompt: "No text, no words, no letters, no numbers, 
no typography, purely photographic background image"
```

### Carousel slides look wrong
```bash
# Test the carousel renderer alone:
python -c "
from src.agents.carousel_agent import CarouselAgent
from pathlib import Path
import asyncio
agent = CarouselAgent()
html = open('src/templates/carousel_template.html').read()
asyncio.get_event_loop().run_until_complete(
    agent.render_slide_async(html, Path('output/test-slide.jpg'))
)
print('Check output/test-slide.jpg')
"
```

### Out of ElevenLabs characters
```python
# Check quota before running:
from src.agents.voice_agent import VoiceAgent
agent = VoiceAgent()
print(agent.get_remaining_characters())
```

---

## Quick Start Checklist

```
□ Python 3.11+ installed
□ FFmpeg installed (ffmpeg -version works)
□ Node.js 18+ installed (node -v works)
□ Virtual environment created and activated
□ pip install -r requirements.txt completed
□ .env file created with all API keys
□ Google Drive credentials downloaded to credentials/
□ Telegram bot created and tested
□ python main.py runs without errors
□ Output folder has content after first run
□ python scheduler.py starts without errors
```

---

*Built with: Python 3.11 · OpenAI GPT-4o · ElevenLabs TTS · DALL-E 3 · FFmpeg · APScheduler · Google Drive API*

*Questions or issues: Check the Troubleshooting section first, then review your .env file for missing or incorrect API keys.*
