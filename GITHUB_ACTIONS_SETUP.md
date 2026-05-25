# GitHub Actions Setup Guide

Your repository now has automated CI/CD workflows. Follow these steps to fully configure them.

## 1. Add GitHub Secrets

Go to: **Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets with your API keys:

### Required Secrets

| Secret Name | Value | Where to Get |
|------------|-------|--------------|
| `OPENAI_API_KEY` | Your OpenAI API key | https://platform.openai.com/api-keys |
| `PERPLEXITY_API_KEY` | Your Perplexity API key | https://www.perplexity.ai/pro |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key | https://elevenlabs.io/app/speech-synthesis |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | From @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Send a message to your bot, check updates |

### Optional Secrets

| Secret Name | Value | Notes |
|------------|-------|-------|
| `GOOGLE_DRIVE_CREDENTIALS` | Google Drive OAuth JSON (base64) | Export from Google Cloud Console |
| `NICHE` | Your content niche (e.g., "AI Technology") | Defaults to "AI Technology" if not set |

## 2. Encode Google Drive Credentials (if using Google Drive)

If using Google Drive for uploads:

```bash
# Convert credentials.json to base64
cat credentials.json | base64 | xclip -selection clipboard

# Then paste into GitHub Actions secret
```

## 3. Available Workflows

### A. Python Tests & Lint (`python-tests.yml`)
- **Triggers**: Every push to `main` or `develop`
- **Actions**:
  - ✓ Installs dependencies
  - ✓ Runs code linting (flake8)
  - ✓ Checks code format (black)
  - ✓ Runs unit tests
  - ✓ Scans for vulnerabilities (Trivy)

### B. Weekly Content Pipeline (`content-pipeline.yml`)
- **Triggers**: 
  - Every Monday at 9 AM UTC (configurable)
  - Manual trigger via "Run workflow" button
- **Actions**:
  - ✓ Installs all dependencies
  - ✓ Runs full content generation pipeline
  - ✓ Uploads outputs as artifacts
  - ✓ Notifies on failures

## 4. Customizing Schedules

To change the weekly pipeline schedule, edit `.github/workflows/content-pipeline.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

Common cron examples:
- `0 9 * * 1` = Monday 9 AM UTC
- `0 18 * * 0` = Sunday 6 PM UTC
- `30 2 * * *` = Daily at 2:30 AM UTC

## 5. Monitoring Workflows

1. Go to your GitHub repo → **Actions**
2. View running/completed workflows
3. Click workflow to see detailed logs
4. Check "Artifacts" tab for output files

## 6. Troubleshooting

### "Workflow failed: API key not found"
→ Verify secret name matches exactly (case-sensitive)
→ Re-check API key is correct

### "FFmpeg not found"
→ Fixed in `content-pipeline.yml` (auto-installs via apt)

### "Module not found"
→ Check `requirements.txt` is up-to-date
→ Verify Python version is 3.10+

### "Rate limit exceeded"
→ Stagger workflow schedules
→ Add delays between API calls in main.py
→ Upgrade API plans if needed

## 7. Branch Protection Rules (Optional)

To require tests pass before merging:

1. Go to **Settings → Branches**
2. Under "Branch protection rules" → **Add rule**
3. Set pattern to `main`
4. Enable:
   - ✓ "Require status checks to pass before merging"
   - ✓ Select `python-tests` workflow

## 8. Notification Setup

### Telegram Notifications
When pipeline completes, bot sends summary to your Telegram:

1. Create Telegram bot: `/start @BotFather`
2. Get token and chat ID
3. Add to GitHub Actions secrets
4. Bot will notify on completion/failure

### GitHub Notifications
- Go to **Settings → Notifications**
- Configure email alerts for workflow failures

## 9. Next Steps

- [ ] Add all required secrets
- [ ] Verify workflows trigger on next push
- [ ] Test manual pipeline run: **Actions → Weekly Content Pipeline → Run workflow**
- [ ] Monitor first run for errors
- [ ] Adjust schedule if needed
- [ ] Set up branch protection (optional)

---

**Questions?** Check workflow logs in **Actions** tab for detailed error messages.
