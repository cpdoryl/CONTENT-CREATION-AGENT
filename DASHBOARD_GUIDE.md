# 📺 Content Generation Studio — Dashboard Guide

## Quick Start

### 1. Launch the Dashboard
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 📖 How to Use

### Page 1️⃣: **🚀 Generate**

**Step 1: Research Trends**
- Click "🔍 Find Trending Topics"
- Waits ~30-60 seconds for Perplexity to find 5 trending topics
- Shows topics with priority scores

**Step 2: Select & Create Package**
- Choose a topic from the dropdown
- Click "✨ Generate Full Content Package"
- Waits ~2-3 minutes while AI generates:
  - Reel script (45 seconds)
  - 6-slide carousel
  - Instagram caption
  - 30 hashtags
  - Hook angle analysis

**Status Indicator:** ✅ All generated when balloon animation appears

---

### Page 2️⃣: **📝 Review & Edit**

Review and customize every piece before posting.

#### **Tab 1: 📹 Reel Script**
- **Edit the hook** (opening line that grabs attention)
- **Edit full script** (complete 45-second voiceover text)
- **View word count** (target: 100-150 words)
- **Generate voiceover** (ElevenLabs TTS)
  - Creates MP3 file automatically
  - Play inline to hear the voice

**Tips:**
- Keep sentences under 10 words
- Use [PAUSE] for breathing room
- CAPITALIZE key words for emphasis

#### **Tab 2: 📸 Carousel**
- **Edit each of 6 slides**
- **Slide 1:** Title + hook
- **Slides 2-5:** Key insights (each ~40 words)
- **Slide 6:** Call-to-action

**Tips:**
- Headlines: max 8 words
- Body: max 40 words
- Each slide should take 5 seconds to read

#### **Tab 3: 📝 Caption**
- **Edit Instagram caption** (max 2200 characters)
- First 3 lines = most important (before "more" fold)
- Ask a question at the end to drive comments
- Don't start with emojis

#### **Tab 4: #️⃣ Hashtags**
- **Edit 30 hashtags** (one per line)
- Recommended mix:
  - 5 large (>1M followers)
  - 15 medium (100k-1M)
  - 10 niche (<100k)

#### **Tab 5: 🎨 Visuals**
- **Reel background** (9:16, vertical)
- **Post image** (1:1, square)
- Click "🎨 Generate" if not created yet
- Uses DALL-E 3 to create AI images

**💾 Important:** Click "Save Edits" to keep changes in memory

---

### Page 3️⃣: **⬇️ Download**

Export all content for posting.

**Available Downloads:**
- 📄 **Script.txt** — Voiceover text
- 📄 **Caption.txt** — Instagram caption
- 📄 **Hashtags.txt** — Hashtag list (one per line)
- 📦 **Complete.json** — All data as JSON
- 🎨 **Reel.jpg** — 9:16 background image
- 🎨 **Post.jpg** — 1:1 post image
- 🎙️ **Voiceover.mp3** — Audio file

**Workflow:**
1. Edit everything in "Review & Edit" tab
2. Come here to download
3. Copy-paste into Instagram/TikTok Creator Studio

---

### Page 4️⃣: **📊 Dashboard**

Overview of all generated content.

**Shows:**
- Total topics researched
- Total packages created
- Items edited
- Word counts, hashtags, slides
- Status of each piece (Edited ✅ / Pending ⏳)

---

## 🎬 Complete Workflow Example

### Generate a Full Week (5 pieces)

**Time required:** ~30-40 minutes total

```
🚀 GENERATE (10 min)
  ├─ Research trends (2 min)
  └─ Generate 5 packages (5-8 min total)

📝 REVIEW & EDIT (15 min)
  ├─ Edit each script (2 min each × 5 = 10 min)
  ├─ Adjust hashtags (2 min each × 5 = 10 min)
  └─ Generate voiceovers (5-10 min background)

⬇️ DOWNLOAD (5 min)
  └─ Download all files for each piece

📱 POST (10 min)
  └─ Copy-paste to Instagram/TikTok
```

---

## 💡 Tips & Tricks

### Speed Up Workflow
- Generate all 5 topics at once
- While scripts generate, prepare post templates
- Download everything in batch

### Quality Checks Before Posting
**Script:**
- [ ] No filler words (so, like, basically)
- [ ] Sentences are punchy (<10 words)
- [ ] Hook is curiosity-driven
- [ ] CTA is specific (not "follow me")

**Caption:**
- [ ] First line grabs attention
- [ ] Ends with a question
- [ ] Under 300 characters preferred
- [ ] No emoji overload

**Hashtags:**
- [ ] Specific to your niche
- [ ] Mix of sizes (5 large + 15 medium + 10 niche)
- [ ] No hashtags on first line of caption

**Images:**
- [ ] No text/words in image
- [ ] High contrast for text overlay
- [ ] Professional/cinematic quality
- [ ] Matches brand colors

### Editing Tips
- **Script too short?** Add more details or expand problem section
- **Caption too long?** Focus on first 3 lines and CTA
- **Hashtags not working?** Replace niche ones with trending alternatives
- **Voice sounds off?** Regenerate or adjust punctuation in script

---

## ⚠️ Common Issues

### "Package not created yet"
- You need to click "Generate Full Content Package" first
- Wait for all indicators to show ✅

### "No files to download"
- Generate the visuals first:
  - Tab 5 → "Generate Reel Image"
  - Tab 5 → "Generate Post Image"

### "Voiceover sounds robotic"
- Adjust script for more natural flow
- Add [PAUSE] for breathing
- Avoid very long sentences

### "Generation takes too long"
- Visual generation (DALL-E): 30-60 seconds normal
- Script generation (GPT): 30-60 seconds per package
- This is API limitation, not dashboard issue

---

## 🔑 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Rerun page | `R` |
| Clear cache | `C` |
| Show settings | `⚙️` (top-right) |
| Theme toggle | Bottom-right icon |

---

## 📊 Data Storage

All data is stored in **session memory** during this session:
- Survives page refreshes
- Cleared when closing browser
- **To persist:** Download JSON file

**Future enhancement:** Save to database

---

## 🚀 Next Steps

1. **Try it now:**
   ```bash
   streamlit run app.py
   ```

2. **Go to 🚀 Generate tab**
3. **Click "🔍 Find Trending Topics"**
4. **Choose a topic and click "✨ Generate"**
5. **Review in 📝 Review & Edit**
6. **Download in ⬇️ Download**

---

## 📞 Support

**For issues:**
- Check CLAUDE.md for architecture
- Review project_status.md for API setup
- All agents tested and working

**Costs:**
- Each research: ~$0.10 (Perplexity)
- Each package: ~$1-2 (GPT + DALL-E)
- Each voiceover: ~$0.02-0.05 (ElevenLabs)
