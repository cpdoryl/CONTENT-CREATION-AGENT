# Claude.md — Social Media Content Agent

## Project Overview

This is a **fully automated social media content production pipeline** that researches trends, generates scripts, creates voiceovers, produces visuals, assembles videos, and builds carousels — all in one orchestrated workflow.

**Architecture:** 7-agent pipeline (Research → Script → Voice → Visual → Video → Carousel → Package)

## Key Implementation Details

### 1. Architecture Pattern

- **Modular agents**: Each agent in `src/agents/` is independent, testable, and uses its own API
- **Shared models**: Pydantic models in `src/core/models.py` for data passing between agents
- **Central config**: `src/core/config.py` loads from `.env` using pydantic-settings
- **Orchestrator**: `main.py` runs agents sequentially, handles errors, and summarizes

### 2. Agent Responsibilities

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Research | Find trending topics (Perplexity) | Niche, audience | List[ContentTopic] |
| Script | Write all copy (GPT-4o) | ContentTopic | ContentPackage |
| Voice | Generate MP3 (ElevenLabs) | Script text | MP3 file |
| Visual | Create images (DALL-E 3) | Script, topic | JPG files (9:16 + 1:1) |
| Video | Assemble MP4 (FFmpeg) | Image + MP3 | MP4 file |
| Carousel | Render slides (Pyppeteer) | Slide data | 6 JPG files |
| Packager | Upload + notify (Google Drive + Telegram) | All files | Drive URL + Telegram msg |

### 3. Tech Stack Choices

- **Pydantic** — strict validation, fast, great IDE support
- **Tenacity** — automatic retries with exponential backoff (critical for API stability)
- **HTTPX** — async-capable HTTP client, better than requests
- **OpenAI SDK** — official, maintains GPT-4o support
- **FFmpeg** — free, no rate limits, battle-tested
- **Pyppeteer** — headless browser for carousel HTML rendering
- **APScheduler** — clean recurring task scheduling

### 4. Critical Implementation Notes

1. **API Key Validation**: Config fails early if keys are missing — catches setup errors before runtime
2. **Error Resilience**: Tenacity retries with exponential backoff; loop continues on individual topic failures
3. **File Organization**: Output structure is `output/YYYY-WXX/topic-slug/` for easy weekly sorting
4. **Async Carousel**: Pyppeteer rendering can conflict with existing event loop — handled with loop creation
5. **FFmpeg Subtitles**: Basic SRT generation chunks text by word count for readability

### 5. Testing Strategy

**Single-agent tests** (see SETUP.md):
```bash
# Research agent quick test
python -c "from src.agents.research_agent import ResearchAgent; ..."

# Script agent with mock topic
# Voice agent quota check
```

**Full pipeline test**:
```bash
python main.py  # Runs on live APIs — costs ~$5-10 per run
```

## Future Development Priorities (CTO View)

1. **Batching** — queue topics, run pipeline on schedule, not on-demand
2. **Cost Tracking** — monitor API spend per topic and weekly
3. **Quality Gates** — validate outputs before packaging (blur check, text detection, duration check)
4. **A/B Testing** — generate 2-3 script variants per topic, track engagement
5. **Analytics** — store metadata, track which hooks/CTAs perform best
6. **Content Calendar** — queue up future topics, schedule across weeks
7. **Backup Strategies** — fallback to alt image providers if DALL-E fails
8. **Video Variants** — auto-generate shorts, TikTok, Instagram reel versions

## Configuration

- **Niche**: Set in `.env` as `NICHE` — shapes all research + script prompts
- **Target Audience**: Drives script tone and content angle
- **Brand Voice**: Used in all script generation
- **Brand Colors**: Displayed in carousel templates
- **Content Per Week**: Controls how many topics to process

## Troubleshooting

### "Module not found"
→ Ensure you're running from project root, not from `src/`

### Perplexity returns 401
→ Check API key at https://www.perplexity.ai/pro (not basic free tier)

### ElevenLabs quota exceeded
→ Check remaining: `agent.get_remaining_characters()` or upgrade plan

### Carousel slides look wrong
→ Verify Pyppeteer installed: `pip install --upgrade pyppeteer`

### Google Drive auth fails
→ Delete `credentials/token.json` and re-run to trigger new OAuth

## Running in Production

```bash
# One-time run
python main.py

# Scheduled weekly (Monday 9am IST)
python scheduler.py

# As background service (Linux/Mac)
nohup python scheduler.py > logs/scheduler.log 2>&1 &
```

## Performance Expectations

- **Research**: 30-60 seconds (Perplexity API)
- **Scripts** (5 topics): 2-3 minutes (GPT-4o calls)
- **Voiceovers**: 30 seconds each (parallel possible)
- **Visuals**: 30-60 seconds each (sequential, API limits)
- **Videos**: 1-2 minutes each (FFmpeg local)
- **Carousels**: 2-3 minutes total (Pyppeteer rendering)
- **Total weekly run**: ~20-30 minutes for 5 complete topics

## Costs (Monthly, 5 pieces/week = ~20/month)

| Service | Cost | Notes |
|---------|------|-------|
| OpenAI GPT-4o | ~$8 | Scripts + visual prompts |
| ElevenLabs | ~$5 | Creator plan (100k chars) |
| Perplexity | ~$5 | Sonar-medium tier |
| DALL-E 3 | ~$4 | 20 HD @ $0.04 + 120 std @ $0.02 |
| **Total** | **~$22** | All other tools are free |

---

**CTO Notes:** This system prioritizes automation quality over feature count. Each agent is battle-tested against common API failures. The orchestrator gracefully handles individual topic failures without stopping the whole pipeline. All outputs are organized by week for easy calendar-based planning.

Last Updated: 2026-05-23
