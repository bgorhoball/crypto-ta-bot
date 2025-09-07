# Python + GitHub Actions: Automated Crypto Technical Analysis

## Overview
This solution uses Python scripts with GitHub Actions to automatically analyze BTC, ETH, and CRO every 5 minutes. It fetches OHLCV data from Binance API, uses Gemini API for comprehensive technical analysis, and sends Telegram notifications when conditions are met.

## Prerequisites
- GitHub account (free)
- Gemini API key (get from: https://aistudio.google.com/app/apikey)
- Telegram bot token and chat ID (already set up)
- Basic understanding of Python and GitHub

## Technical Indicators Analyzed
- **RSI (14-period)**: Momentum oscillator for overbought/oversold signals
- **SMA20**: Short-term trend direction
- **SMA50**: Medium-term trend direction  
- **EMA20**: Fast-responding moving average
- **SMA200**: Long-term trend (bull/bear market indicator)
- **MACD (12,26,9)**: Trend and momentum convergence/divergence

## Alert Conditions
- **RSI > 70**: Overbought warning
- **RSI < 30**: Oversold opportunity
- **Golden Cross**: SMA20 crosses above SMA50 (bullish)
- **Death Cross**: SMA20 crosses below SMA50 (bearish)
- **Price above SMA200**: Bull market confirmation
- **MACD bullish/bearish crossover**: Momentum shifts

## Step-by-Step Setup

### Step 1: Create GitHub Repository
1. Go to GitHub and create a new repository
2. Name it: `crypto-technical-analysis`
3. Make it **Private** (to protect API keys)
4. Clone to your local machine

### Step 2: Set Up Repository Structure

Create these files in your repository:

```
crypto-technical-analysis/
├── .github/
│   └── workflows/
│       └── crypto-analysis.yml    # GitHub Actions workflow
├── crypto_analysis.py             # Main Python script
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation
```

### Step 3: Configure GitHub Secrets

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Add these repository secrets:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### Step 4: Copy Files to Repository

**Files provided in this repository:**
1. **crypto_analysis.py** - Main Python script with full analysis logic
2. **requirements.txt** - Python dependencies
3. **.github/workflows/crypto-analysis.yml** - GitHub Actions workflow

Copy these files to your `crypto-technical-analysis` repository.

### Step 5: Test and Deploy

#### Manual Test (Optional):
1. Set environment variables locally:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   export TELEGRAM_BOT_TOKEN="your_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id_here"
   ```
2. Run: `python crypto_analysis.py`
3. Check for any errors or missing dependencies

#### Deploy to GitHub Actions:
1. Push all files to your repository
2. Go to **Actions** tab in GitHub
3. You should see "Crypto Technical Analysis" workflow
4. Click **Run workflow** to test manually first
5. The workflow will then run automatically every 5 minutes

---

## How It Works

### Data Collection
1. **Binance API**: Fetches 200 recent 5-minute OHLCV candles for BTC, ETH, CRO
2. **Free & Unlimited**: No API key required, no rate limits for market data

### Technical Analysis
1. **Gemini AI**: Processes OHLCV data and calculates all technical indicators
2. **Smart Analysis**: Uses AI to determine support/resistance levels and market conditions
3. **JSON Response**: Structured data with all indicators and signals

### Notification Logic
Sends Telegram messages when any of these conditions are met:
- RSI above 70 (overbought) or below 30 (oversold)
- Strong buy/sell signals from overall analysis
- Golden cross or death cross (SMA20 vs SMA50)
- Strong MACD signals with significant histogram values

### Sample Telegram Message
```
🚀 **Bitcoin (BTCUSDT)** Analysis

💲 **Price:** $67,234.56

📊 **Technical Indicators:**
• RSI(14): 72.3 ⚠️ Overbought
• SMA20: $66,180.45
• SMA50: $64,890.23
• EMA20: $66,891.12
• SMA200: $58,234.67

📈 **MACD:**
• Line: 234.56
• Signal: 198.23
• Histogram: 36.33

🎯 **Signals:**
• RSI: Overbought
• Short Trend: 🟢 Bullish
• Long Trend: 🟢 Bullish
• SMA Cross: Golden Cross
• MACD: 🟢 Bullish

🔔 **Overall Signal:** 🟢 **STRONG BUY**

📝 **Analysis:** Bitcoin shows strong bullish momentum with golden cross formation and bullish MACD, though RSI indicates short-term overbought conditions.

🕐 2024-01-15 14:25:32 UTC
```

## Advantages Over iOS Shortcuts

✅ **Much Simpler Setup**: No complex JSON builders or variable management  
✅ **Reliable Execution**: Cloud-based, doesn't depend on your phone  
✅ **Better Error Handling**: Proper logging and error recovery  
✅ **Version Control**: All code is tracked in git  
✅ **Easy Modifications**: Change coins, indicators, or thresholds easily  
✅ **Free**: GitHub Actions provides 2000 free minutes/month  
✅ **Professional**: Real development workflow with proper CI/CD  

## Costs
- **Binance API**: Free, unlimited
- **Gemini API**: ~$0.0015 per 1K tokens (input), ~$0.006 per 1K tokens (output)
- **GitHub Actions**: Free (2000 minutes/month)
- **Telegram**: Free
- **Total cost**: ~$3-5/month for continuous 5-minute analysis

## Monitoring and Maintenance

### View Logs
1. Go to GitHub repo → **Actions** tab
2. Click on any workflow run to see logs
3. Check for errors or API failures

### Modify Settings
1. Edit `crypto_analysis.py` to:
   - Add/remove coins (change `self.coins` list)
   - Adjust notification thresholds
   - Modify analysis prompt for Gemini
2. Push changes to trigger automatic updates

### Pause/Resume
1. Go to **Actions** tab → **Crypto Technical Analysis** workflow
2. Click **Disable workflow** to pause
3. Click **Enable workflow** to resume

## Troubleshooting

### Common Issues:

**Workflow Not Running:**
- Check GitHub Secrets are set correctly
- Verify workflow file is in `.github/workflows/` directory
- Check Actions are enabled for your repository

**API Errors:**
- Verify Gemini API key is valid and has quota
- Check Telegram bot token and chat ID
- Review logs in GitHub Actions for specific error messages

**Missing Notifications:**
- Check notification conditions in `should_send_notification()` function
- Verify Telegram bot has permission to send messages to your chat
- Review analysis results in GitHub Actions logs

**Rate Limiting:**
- GitHub Actions: 5-minute minimum interval (already set)
- Gemini API: Built-in rate limiting with sleep delays
- Binance API: No limits on market data

### Customization Examples:

**Add More Coins:**
```python
self.coins = ['BTCUSDT', 'ETHUSDT', 'CROUSDT', 'ADAUSDT', 'SOLUSDT']
self.coin_names = {
    'BTCUSDT': 'Bitcoin', 
    'ETHUSDT': 'Ethereum', 
    'CROUSDT': 'Cronos',
    'ADAUSDT': 'Cardano',
    'SOLUSDT': 'Solana'
}
```

**Change Analysis Frequency:**
```yaml
# In .github/workflows/crypto-analysis.yml
schedule:
  - cron: '*/10 * * * *'  # Every 10 minutes
  - cron: '0 * * * *'     # Every hour
  - cron: '0 9,17 * * *'  # 9 AM and 5 PM daily
```

**Adjust Notification Thresholds:**
```python
def should_send_notification(self, analysis):
    # More sensitive - notify on any significant signal
    if indicators['rsi'] > 65 or indicators['rsi'] < 35:  # Wider RSI range
        return True
    
    # Less sensitive - only extreme conditions
    if indicators['rsi'] > 80 or indicators['rsi'] < 20:  # Narrower RSI range
        return True
```

This Python + GitHub Actions solution provides a robust, professional approach to automated crypto technical analysis that's much more reliable and maintainable than iOS Shortcuts.