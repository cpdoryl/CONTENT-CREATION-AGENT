# API Keys & Environment Setup Guide

**Estimated Time**: 40 minutes  
**Difficulty**: Easy  
**Prerequisites**: Web browser, email

---

## Overview: 5 APIs to Configure

| # | Service | Cost | Required | Status | Time |
|---|---------|------|----------|--------|------|
| 1 | **OpenAI** | $5+ credit | ✅ YES | [ ] | 5 min |
| 2 | **Perplexity** | Paid (~$5/mo) | ✅ YES | [ ] | 3 min |
| 3 | **ElevenLabs** | Free tier | ✅ YES | [ ] | 5 min |
| 4 | **Google Drive** | Free | ❌ OPTIONAL | [ ] | 10 min |
| 5 | **Telegram Bot** | Free | ❌ OPTIONAL | [ ] | 5 min |
| 6 | **FFmpeg** | Free | ✅ YES | [ ] | 10 min |

---

## ✅ STEP 1: OpenAI API Key (5 minutes)

### What it's for:
- Writing scripts with GPT-4o
- Generating images with DALL-E 3
- Creating visual prompts

### How to get it:

1. **Go to**: https://platform.openai.com/api-keys
2. **Sign in** with your OpenAI account (create one if needed)
3. **Click**: "Create new secret key"
4. **Copy** the key (looks like: `sk-proj-xxxxxxxxxxxxx...`)
5. **Save it somewhere** (you'll need it in 10 minutes)

### Cost:
- Free trial: $5 credit (expires in 3 months)
- Pay-as-you-go: $0.10-0.04 per 1,000 tokens
- ~$2-3 per content batch (5 pieces)

### Your OpenAI Key:
```
OPENAI_API_KEY = ___________________________________
```

**Status**: [ ] Complete

---

## ✅ STEP 2: Perplexity API Key (3 minutes)

### What it's for:
- Researching trending topics in your niche
- Finding what content opportunities exist this week

### How to get it:

1. **Go to**: https://www.perplexity.ai/pro
2. **Sign up** or **log in**
3. **Go to**: Account Settings → API
4. **Create API key** or **View API key**
5. **Copy** the key (looks like: `pplx-xxxxxxx...`)

### Important:
- Perplexity requires a **paid subscription** (~$5/month)
- Free tier has limited API access
- You may need to upgrade to use the API

### Your Perplexity Key:
```
PERPLEXITY_API_KEY = ___________________________________
```

**Status**: [ ] Complete

---

## ✅ STEP 3: ElevenLabs API Key (5 minutes)

### What it's for:
- Converting scripts to natural-sounding voiceovers
- Generated MP3 files for videos

### How to get it:

1. **Go to**: https://elevenlabs.io
2. **Sign up** or **log in** (free account)
3. **Go to**: Account → API Keys
4. **Copy** the API key
5. **Note**: Also note your Voice ID (for voiceover voice selection)

### Cost:
- Free tier: 10,000 characters/month (~5-10 voiceovers)
- Creator plan: $5/month (100,000 chars)
- Professional: $22/month (500,000 chars)

### Get Your Voice ID:
1. Go to: https://elevenlabs.io/voice-lab
2. Find a voice you like (or clone your own)
3. Copy the Voice ID

### Your ElevenLabs Keys:
```
ELEVENLABS_API_KEY = ___________________________________
ELEVENLABS_VOICE_ID = ___________________________________
(Default: 21m00Tcm4TlvDq8ikWAM)
```

**Status**: [ ] Complete

---

## ⭐ STEP 4: Google Drive API (Optional, 10 minutes)

### What it's for:
- Automatically upload content to your Google Drive
- Organize by week/topic
- Backup your content files

### Is it required?
- ❌ NO - system works without it
- ✅ BUT RECOMMENDED for organization + backup

### How to set it up:

#### 4A. Create Google Cloud Project
1. Go to: https://console.cloud.google.com
2. **Create a new project**:
   - Click "Select a Project" (top left)
   - Click "NEW PROJECT"
   - Name it: "ContentAgent"
   - Click "CREATE"

#### 4B. Enable Google Drive API
1. In the project, go to "APIs & Services" → "Library"
2. Search for: "Google Drive API"
3. Click on it
4. Click: "ENABLE"

#### 4C. Create OAuth Credentials
1. Go to: "APIs & Services" → "Credentials"
2. Click: "CREATE CREDENTIALS" → "OAuth 2.0 Client ID"
3. Choose: "Desktop application"
4. Click: "CREATE"
5. You get a popup - click: "DOWNLOAD JSON"
6. Save the file as: `credentials/google_credentials.json`

#### 4D. Set Folder ID
1. Open your Google Drive
2. Create a folder called "ContentAgent"
3. Open the folder
4. Copy the folder ID from the URL:
   - URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Copy that ID

### Your Google Settings:
```
GOOGLE_CREDENTIALS_PATH = credentials/google_credentials.json
GOOGLE_DRIVE_FOLDER_ID = ___________________________________
```

**Status**: [ ] Complete

---

## ⭐ STEP 5: Telegram Bot (Optional, 5 minutes)

### What it's for:
- Get notified when content is ready
- Receive summary of what was generated

### Is it required?
- ❌ NO - system works without it
- ✅ BUT NICE TO HAVE for notifications

### How to set it up:

1. **Open Telegram** (app or web.telegram.org)
2. **Search for**: @BotFather
3. **Start the chat**
4. **Send**: `/newbot`
5. **Answer questions**:
   - Bot name: "ContentAgent" (or your preference)
   - Bot username: "ContentAgent_bot" (must be unique)
6. **You get a BOT_TOKEN** - copy it
7. **Now get your CHAT_ID**:
   - Search for: @userinfobot
   - Start the chat
   - Message it anything
   - It responds with your user ID
   - Copy that ID

### Your Telegram Settings:
```
TELEGRAM_BOT_TOKEN = ___________________________________
TELEGRAM_CHAT_ID = ___________________________________
```

**Status**: [ ] Complete

---

## ✅ STEP 6: Install FFmpeg (10 minutes)

### What it's for:
- Assembling videos (voiceover + background image → MP4)
- Required for the Video Agent

### Is it required?
- ✅ YES - system cannot work without it

### Installation by OS:

#### Windows:
1. Download: https://ffmpeg.org/download.html
2. Click "Windows builds by BtbN"
3. Download latest stable (usually "essentials" version)
4. Extract to: `C:\ffmpeg`
5. Add to PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Click "New" (under System variables)
   - Variable name: `Path`
   - Variable value: `C:\ffmpeg\bin`
   - Click OK
6. **Verify**: Open new terminal, run: `ffmpeg -version`

#### Mac:
```bash
# Install Homebrew first if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install FFmpeg
brew install ffmpeg

# Verify
ffmpeg -version
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Verify
ffmpeg -version
```

**Status**: [ ] Complete

---

## 📝 STEP 7: Update .env File

Once you have all your keys, edit the `.env` file:

### Open `.env` file:
```bash
# In project root directory
# Open with any text editor
```

### Fill in REQUIRED keys:
```env
# REQUIRED - Get from steps above
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
ELEVENLABS_API_KEY=YOUR_KEY_HERE
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
PERPLEXITY_API_KEY=pplx-YOUR_KEY_HERE

# OPTIONAL - Leave blank if not setting up
GOOGLE_CREDENTIALS_PATH=credentials/google_credentials.json
GOOGLE_DRIVE_FOLDER_ID=YOUR_FOLDER_ID_HERE
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE

# CUSTOMIZATION - Change to your niche
NICHE=personal finance for millennials
TARGET_AUDIENCE=25-35 year olds struggling with saving and investing
BRAND_VOICE=calm, direct, educational, uses simple words, no jargon
BRAND_COLORS=#1D9E75,#06132B,#F5F4F0
CONTENT_PER_WEEK=5
OUTPUT_DIR=output
```

### SAVE the file!

**Status**: [ ] Complete

---

## ✅ STEP 8: Verify Everything Works

Once all keys are in `.env`:

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Mac/Linux

# Run the test suite
python test_agents.py
```

### Expected Results:
```
Config          PASSED
Research        PASSED
Script          PASSED
Voice           PASSED
Visual          PASSED
Video           PASSED
Carousel        PASSED
Packager        PASSED

Result: 8/8 PASSED ✅
```

If all pass → Ready to deploy!

**Status**: [ ] Complete

---

## 🚀 STEP 9: Deploy!

Once tests pass:

```bash
python main.py
```

This will:
1. Research 5 trending topics
2. Write scripts for each
3. Generate voiceovers
4. Create images
5. Assemble videos
6. Render carousels
7. Upload to Drive (optional)
8. Send Telegram notification (optional)

**Duration**: ~25 minutes  
**Cost**: ~$4-5  
**Output**: 5 complete content pieces

---

## 📊 Checklist

### API Keys
- [ ] OpenAI API key obtained
- [ ] Perplexity API key obtained
- [ ] ElevenLabs API key obtained
- [ ] ElevenLabs Voice ID obtained
- [ ] Google Drive credentials (optional)
- [ ] Telegram Bot token (optional)
- [ ] Telegram Chat ID (optional)

### Setup
- [ ] FFmpeg installed
- [ ] FFmpeg in PATH
- [ ] .env file updated with all keys
- [ ] .env file saved

### Testing
- [ ] Virtual environment activated
- [ ] python test_agents.py runs
- [ ] 8/8 tests PASS
- [ ] No errors in logs/agent.log

### Ready to Deploy
- [ ] All tests passing
- [ ] Ready to run: python main.py
- [ ] Ready to schedule: python scheduler.py

---

## 🆘 Troubleshooting

### "API key invalid" error
→ Double-check you copied the key correctly  
→ Make sure there are no spaces before/after the key  
→ Key should look like: `sk-proj-xxxxx` (no `[brackets]`)

### "FFmpeg not found" error
→ Run `ffmpeg -version` in terminal  
→ If not found, reinstall and add to PATH  
→ Restart terminal after adding to PATH

### "Module not found" error
→ Make sure you're in project root directory  
→ Make sure virtual environment is activated  
→ Make sure pip install -r requirements.txt was run

### "Perplexity returns 401"
→ Make sure you have a paid Perplexity subscription  
→ Free tier doesn't support API access

### "ElevenLabs returns 0 quota"
→ Free tier starts with 10k characters  
→ One voiceover uses ~1000-2000 characters  
→ Upgrade to Creator plan ($5/mo) for more

---

## 💡 Tips

1. **Save your keys somewhere safe** - you'll need them again if you lose the .env file
2. **Don't share your .env file** - it contains secret keys
3. **Start with required APIs only** - add Google Drive later if you want
4. **Test each agent separately** - helps debug if something fails
5. **Monitor your costs** - APIs charge based on usage

---

## Next Steps After Setup

1. ✅ Verify all 8 tests pass
2. ✅ Run `python main.py` for first batch
3. ✅ Check output quality
4. ✅ Optional: Set up scheduler `python scheduler.py`

**Good luck! You've got this! 🚀**
