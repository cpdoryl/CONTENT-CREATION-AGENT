# Setup Guide — Social Media Content Agent

## Prerequisites

- Python 3.11+ installed
- FFmpeg 6.0+ (`ffmpeg -version` to verify)
- Node.js 18+ (`node -v` to verify)
- Git installed

## 1. Initialize Git & Virtual Environment

```bash
cd "c:\social media content buiding agent"
git init
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source .venv/bin/activate

# Verify activation — you should see (.venv) in your terminal
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Set Up Environment Variables

```bash
# Copy template
copy .env.example .env

# Edit .env with your API keys
# Required keys:
# - OPENAI_API_KEY
# - ELEVENLABS_API_KEY
# - PERPLEXITY_API_KEY
# - GOOGLE_CREDENTIALS_PATH (download from Google Cloud)
# - TELEGRAM_BOT_TOKEN (optional but recommended)
```

## 4. Set Up Google Drive API

```bash
# 1. Go to console.cloud.google.com
# 2. Create new project → "ContentAgent"
# 3. Enable Google Drive API
# 4. Create credentials → OAuth 2.0 Client ID → Desktop app
# 5. Download JSON as credentials/google_credentials.json

mkdir credentials
# Move downloaded file to credentials/google_credentials.json
```

## 5. Get Your ElevenLabs Voice ID

Visit https://elevenlabs.io/voice-lab to find your voice ID or clone your own voice. Copy it to `ELEVENLABS_VOICE_ID` in `.env`.

## 6. Create Telegram Bot (Optional)

```
1. Open Telegram → search @BotFather
2. Send: /newbot
3. Follow prompts → get your BOT_TOKEN
4. Start a chat with your bot
5. Visit: https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates
6. Send a message to your bot, refresh the URL
7. Copy the "id" field from "chat" → that's your CHAT_ID
```

## 7. Test Individual Agents

### Test Research Agent
```bash
python -c "
from src.agents.research_agent import ResearchAgent
agent = ResearchAgent()
topics = agent.research_trends()
for t in topics[:3]:
    print(f'[{t.priority_score}/10] {t.topic}')
"
```

### Test Script Agent
```bash
python -c "
from src.agents.script_agent import ScriptAgent
from src.core.models import ContentTopic

agent = ScriptAgent()
test_topic = ContentTopic(
    topic='5 Money Mistakes',
    why_trending='Financial literacy is trending',
    hook_angle='shame and identity',
    recommended_format='reel',
    pain_point='wasting money without knowing',
    title_options=['5 Money Mistakes', 'Stop Wasting Money', 'Rich People Know This'],
    priority_score=9
)
script = agent.write_reel_script(test_topic)
print(f'Word count: {script.word_count}')
print(f'Hook: {script.hook}')
"
```

### Test Voice Agent
```bash
python -c "
from src.agents.voice_agent import VoiceAgent
from pathlib import Path

agent = VoiceAgent()
quota = agent.get_remaining_characters()
print(f'Quota remaining: {quota[\"remaining\"]:,} characters')
agent.generate_voiceover(
    'This is a test voiceover. Your content agent is working correctly.',
    Path('output/test_voice.mp3')
)
print('✅ test_voice.mp3 created — play it to check quality')
"
```

## 8. Run Full Pipeline

```bash
# Manual test run
python main.py

# Check output folder
# output/
# └── 2025-W23/
#     ├── topic-1/
#     │   ├── reels/
#     │   ├── carousel/
#     │   ├── post/
#     │   └── caption.txt
```

## 9. Set Up Scheduler (Optional)

```bash
# Start scheduler (runs every Monday at 9:00 AM IST)
python scheduler.py

# To run as background service on Mac/Linux
nohup python scheduler.py > logs/scheduler.log 2>&1 &

# Check if running
ps aux | grep scheduler.py
```

## Troubleshooting

### "Python not found"
- Ensure Python 3.11+ is installed: `python --version`
- Use full path if needed: `C:\Python311\python.exe`

### "No module named 'src'"
- Verify you're running from the project root directory
- Check that `src/__init__.py` exists

### "ffmpeg: command not found"
```bash
# Windows: Download from https://ffmpeg.org/download.html and add to PATH
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### "API key invalid"
- Double-check your keys in `.env`
- For OpenAI: https://platform.openai.com/api-keys
- For ElevenLabs: https://elevenlabs.io/account/subscription
- For Perplexity: https://www.perplexity.ai/login

### Pyppeteer timeout issues
```bash
# Reinstall with:
pip install --upgrade pyppeteer
# If still issues, use Puppeteer via Node instead
```

## Quick Checklist

```
□ Python 3.11+ installed (python --version)
□ FFmpeg installed (ffmpeg -version)
□ Node.js 18+ installed (node -v)
□ .venv created and activated (you see (.venv) in terminal)
□ pip install -r requirements.txt completed
□ .env file created with all API keys filled
□ credentials/google_credentials.json exists
□ python main.py runs without errors
□ output/ folder has content after first run
```

## For CTO: Next Phase Implementation

Once verified:

1. **Add error handling & retries** — expand tenacity usage
2. **Add quality checks** — validate output before packaging
3. **Add content queue** — buffer topics for scheduling
4. **Add analytics** — track what performs best
5. **Add content variants** — A/B test hooks and CTAs
6. **Add cost tracking** — monitor API spend per week
7. **Add config presets** — save brand/niche templates

See README.md for full architecture and customization guide.
