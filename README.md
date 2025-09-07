# Crypto Technical Analysis Bot

Automated cryptocurrency technical analysis using Python, GitHub Actions, and AI-powered insights.

## Overview

This bot automatically analyzes **Bitcoin (BTC)**, **Ethereum (ETH)**, and **Cronos (CRO)** every 5 minutes using:
- 🔄 **Binance API** for real-time OHLCV data
- 🤖 **Google Gemini AI** for technical analysis
- 📱 **Telegram notifications** for alerts
- ☁️ **GitHub Actions** for cloud execution

## Features

### 📊 Technical Indicators
- **RSI (14-period)**: Overbought/oversold momentum
- **Moving Averages**: SMA20, SMA50, EMA20, SMA200
- **MACD (12,26,9)**: Trend and momentum analysis
- **Support/Resistance**: AI-calculated levels

### 🚨 Smart Alerts
- RSI extremes (>70 overbought, <30 oversold)
- Golden/Death cross signals (SMA20 vs SMA50)
- Strong buy/sell recommendations
- MACD momentum shifts

### 🎯 Sample Notification
```
🚀 **Bitcoin (BTCUSDT)** Analysis

💲 **Price:** $67,234.56

📊 **Technical Indicators:**
• RSI(14): 72.3 ⚠️ Overbought
• SMA20: $66,180.45
• SMA50: $64,890.23

🔔 **Overall Signal:** 🟢 **STRONG BUY**

📝 **Analysis:** Strong bullish momentum with golden cross formation, though RSI shows short-term overbought conditions.
```

## Quick Setup

### 1. Configure Secrets
Go to **Settings** → **Secrets and variables** → **Actions** and add:
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### 2. Enable Actions
- Go to **Actions** tab
- Click **"I understand my workflows, go ahead and enable them"**
- The bot will start running automatically every 5 minutes

### 3. Manual Test (Optional)
Click **Actions** → **Crypto Technical Analysis** → **Run workflow** to test immediately.

## Files Structure

```
├── .github/workflows/crypto-analysis.yml  # GitHub Actions workflow
├── crypto_analysis.py                     # Main Python bot
├── requirements.txt                       # Dependencies
├── claude.md                             # Detailed setup guide
└── README.md                             # This file
```

## Costs

- **Binance API**: Free, unlimited
- **GitHub Actions**: Free (2000 minutes/month)
- **Telegram**: Free  
- **Gemini API**: ~$3-5/month for continuous analysis

## Customization

### Add More Cryptocurrencies
Edit `crypto_analysis.py`:
```python
self.coins = ['BTCUSDT', 'ETHUSDT', 'CROUSDT', 'ADAUSDT', 'SOLUSDT']
```

### Change Frequency
Edit `.github/workflows/crypto-analysis.yml`:
```yaml
schedule:
  - cron: '*/10 * * * *'  # Every 10 minutes
  - cron: '0 * * * *'     # Every hour
```

### Adjust Alert Sensitivity
Modify the `should_send_notification()` function in `crypto_analysis.py`.

## Monitoring

- **View Logs**: Actions tab → Latest workflow run
- **Pause Bot**: Actions → Crypto Technical Analysis → Disable workflow
- **Resume Bot**: Actions → Crypto Technical Analysis → Enable workflow

## Troubleshooting

**Bot Not Running?**
- Check GitHub Secrets are set correctly
- Verify Actions are enabled
- Check workflow logs for errors

**No Notifications?**
- Verify Telegram bot permissions
- Check notification conditions in code
- Review analysis results in logs

**API Errors?**
- Confirm Gemini API key is valid
- Check API quotas and billing
- Review error messages in workflow logs

## Support

See the detailed setup guide in `claude.md` for comprehensive instructions and troubleshooting tips.

---

**⚡ Powered by GitHub Actions + Python + AI**