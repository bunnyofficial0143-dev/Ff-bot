# FF Match Result Bot — Setup Guide

## ফাইল গুলো কী?
- `bot.py` — মূল bot code
- `requirements.txt` — Python packages
- `railway.toml` — Free hosting config

## Deploy করার Steps (Railway — সম্পূর্ণ ফ্রি)

### Step 1 — GitHub এ upload করো
1. github.com এ account করো (free)
2. New repository বানাও — নাম দাও `ff-bot`
3. এই ৩টা file upload করো

### Step 2 — Railway তে deploy করো
1. railway.app এ যাও
2. GitHub দিয়ে login করো
3. "New Project" → "Deploy from GitHub repo" → তোমার repo select করো

### Step 3 — Environment Variables দাও
Railway dashboard এ "Variables" tab এ গিয়ে দুটো variable যোগ করো:

| Key | Value |
|-----|-------|
| TELEGRAM_TOKEN | তোমার BotFather এর token |
| ANTHROPIC_API_KEY | তোমার Anthropic API key |

### Step 4 — Deploy!
Save করলেই automatically deploy হবে। Bot চালু!

## Bot use করা
Telegram এ তোমার bot খুঁজে নাও → Start → Screenshot পাঠাও → .txt file পাবে!
