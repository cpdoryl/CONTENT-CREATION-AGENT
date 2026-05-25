# 🚀 Deployment Guide - Live Web URL

## Get Your App Live in 5 Minutes

### **Step 1: Push Latest Changes** ✅ DONE
Your code is already on GitHub at:
```
https://github.com/cpdoryl/CONTENT-CREATION-AGENT
```

### **Step 2: Deploy to Streamlit Cloud** (RECOMMENDED)

#### **A. Create Streamlit Cloud Account**
1. Go to: https://share.streamlit.io/
2. Click **Sign in with GitHub**
3. Authorize Streamlit to access your repositories
4. Click **New app**

#### **B. Configure Your App**
Fill in these fields:
- **GitHub repository**: `cpdoryl/CONTENT-CREATION-AGENT`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL name**: `content-creation-agent` (or your choice)

Click **Deploy** — takes 2-3 minutes

#### **C. Add Secrets (IMPORTANT)**
Once deployed:
1. Click your app
2. Go to **Settings** (gear icon) → **Secrets**
3. Copy-paste this template and fill in YOUR keys:

```
OPENAI_API_KEY = "sk-proj-xxxxx"
PERPLEXITY_API_KEY = "pplx-xxxxx"
ELEVENLABS_API_KEY = "xxxxx"
TELEGRAM_BOT_TOKEN = "123456:ABCxyz"
TELEGRAM_CHAT_ID = "987654321"
NICHE = "AI Technology"
TARGET_AUDIENCE = "Tech professionals"
BRAND_VOICE = "Informative and engaging"
BRAND_COLORS = '["#FF6B6B", "#4ECDC4", "#45B7D1"]'
```

4. Click **Save**
5. App automatically restarts with secrets loaded

#### **D. Your Live URL**
```
https://content-creation-agent.streamlit.app
```

✅ **Share this link with anyone!**

---

## **Alternative: Test Locally First with ngrok**

If you want to test before deploying:

### **Option 1: ngrok (Instant Remote Access)**
```powershell
# 1. Install ngrok
choco install ngrok

# 2. Create .streamlit/secrets.toml with your API keys
# (Copy from .streamlit/secrets.toml.example)

# 3. Run Streamlit
streamlit run app.py

# 4. In another terminal
ngrok http 8501

# 5. Share the ngrok URL
# https://abc-123-xyz.ngrok-free.app
```

✅ **Instant link for testing!**

---

## **What You Can Test**

Once deployed, your app has these features:

### **⚡ Auto Pipeline**
- One-click content generation for multiple topics
- Automated research, scripts, voiceovers, visuals
- Real-time progress tracking

### **🚀 Generate**
- Manual topic input
- Choose generation stage (Research → Script → Voice → Visual)
- Download individual outputs

### **📝 Review & Edit**
- Edit generated scripts
- Adjust tone, length, CTAs
- Preview content before finalizing

### **⬇️ Download**
- Export as MP4 video
- Download carousel slides (JPG)
- Get all assets in ZIP

### **📊 Dashboard**
- View generation history
- Cost tracking (if enabled)
- Success/failure rates

---

## **Troubleshooting**

### **"API Key Not Found"**
→ Check Secrets are added in Streamlit Cloud settings
→ Restart the app after adding secrets

### **"Module not found"**
→ All dependencies in `requirements.txt` ✓
→ Streamlit Cloud auto-installs them

### **"File not found"**
→ Ensure all files are committed to GitHub
→ Check `.gitignore` doesn't exclude needed files

### **Slow to load first time**
→ Normal — Streamlit Cloud builds environment first load
→ Subsequent loads are faster

---

## **Monitor Your App**

1. **Streamlit Cloud Dashboard**: https://share.streamlit.io/
2. **View Logs**: Click app → **Manage** → **View Logs**
3. **Restart**: Click app → **Manage** → **Reboot Script**
4. **Settings**: Click app → **Settings** (add more secrets anytime)

---

## **Next: Production Features**

Once live, you can add:
- [ ] Custom domain (e.g., myagent.com)
- [ ] Email notifications on completion
- [ ] Scheduled daily/weekly runs
- [ ] Analytics dashboard
- [ ] Team access (Streamlit Pro)

---

**Ready?** Go to https://share.streamlit.io/ and follow **Step 2** above!

**Questions?** Check the logs in Streamlit Cloud or reply here.
