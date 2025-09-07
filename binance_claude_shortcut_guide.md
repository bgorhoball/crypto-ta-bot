# iOS Shortcut: Binance + Claude API for Technical Analysis

## Overview
This approach uses Binance API (free, unlimited) to get OHLCV data, then sends it to Claude API for technical indicator calculations (RSI, MACD, SMA), and triggers notifications based on the results.

## Prerequisites
- Anthropic Claude API key (get from: https://console.anthropic.com/)
- iOS Shortcuts app
- Basic understanding of iOS Shortcuts

## Step-by-Step Setup

### Step 1: Get Claude API Key
1. Go to: https://console.anthropic.com/
2. Sign up/login
3. Navigate to "API Keys"
4. Create new key
5. **Copy and save** your API key

### Step 2: Create the Shortcut

#### 2.1: Get OHLCV Data from Binance
```
Add Action: Get Contents of URL
URL: https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit=21
Method: GET
```
*This gets 21 days of daily candles (enough for 20-day SMA + current day)*

#### 2.2: Format Data for Claude
```
Add Action: Get Value for
Dictionary: Contents of URL
Get Value for: (This will be an array of OHLCV data)
Set Variable: Raw_Data

Add Action: Set Variable
Variable Name: Claude_Prompt
Value: "Calculate technical indicators for ETH based on this OHLCV data: [Raw_Data]

Please calculate and return ONLY a JSON response with:
- Current Price
- RSI (14-period) 
- SMA20 (20-day Simple Moving Average)
- MACD (12,26,9)

Format response as:
{
  "current_price": number,
  "rsi": number,
  "sma20": number,
  "macd_line": number,
  "macd_signal": number,
  "macd_histogram": number
}

IMPORTANT: Return ONLY the JSON, no other text."
```

#### 2.3: Send to Claude API
```
Add Action: Get Contents of URL
URL: https://api.anthropic.com/v1/messages
Method: POST
Headers:
  - Content-Type: application/json
  - x-api-key: YOUR_CLAUDE_API_KEY
  - anthropic-version: 2023-06-01

Request Body: {
  "model": "claude-3-sonnet-20240229",
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "[Claude_Prompt variable]"
    }
  ]
}
```

#### 2.4: Parse Claude Response
```
Add Action: Get Value for
Dictionary: Contents of URL (Claude response)
Get Value for: content → 0 → text
Set Variable: Claude_Response

Add Action: Get Dictionary from Input
Input: Claude_Response
Set Variable: Indicators

Add Action: Get Value for
Dictionary: Indicators
Get Value for: current_price
Set Variable: ETH_Price

Add Action: Get Value for  
Dictionary: Indicators
Get Value for: rsi
Set Variable: ETH_RSI

Add Action: Get Value for
Dictionary: Indicators  
Get Value for: sma20
Set Variable: ETH_SMA20
```

#### 2.5: Alert Logic
```
// RSI Alerts
If ETH_RSI > 70
  → Show Notification: "⚠️ ETH Overbought - RSI: [ETH_RSI]"
  
Otherwise If ETH_RSI < 30
  → Show Notification: "💰 ETH Oversold - RSI: [ETH_RSI]"

// Price vs SMA Alert  
If ETH_Price > ETH_SMA20
  → Show Notification: "📈 ETH above SMA20 - Bullish trend"
Otherwise  
  → Show Notification: "📉 ETH below SMA20 - Bearish trend"

// Price Level Alerts
If ETH_Price > 5000
  → Show Notification: "🚨 ETH hit $5000!"
```

## Sample Claude Prompt (Optimized)

```
Based on this ETH OHLCV data from Binance, calculate technical indicators:

[OHLCV Array Data]

Calculate and return ONLY this JSON structure:
{
  "current_price": 3245.67,
  "rsi": 52.4,
  "sma20": 3180.23,
  "macd_line": 12.45,
  "macd_signal": 8.32,
  "macd_histogram": 4.13,
  "analysis": {
    "rsi_signal": "neutral",
    "trend": "bullish",
    "recommendation": "hold"
  }
}

CRITICAL: Respond with ONLY valid JSON, no markdown, no explanations.
```

## Advanced Features

### 2.6: Enhanced Alert Logic with Claude Analysis
```
Add Action: Get Value for
Dictionary: Indicators
Get Value for: analysis → recommendation  
Set Variable: Claude_Recommendation

If Claude_Recommendation equals "buy"
  → Show Notification: "💚 Claude Recommends: BUY ETH"
  → Send to Telegram Bot
  
If Claude_Recommendation equals "sell"  
  → Show Notification: "🔴 Claude Recommends: SELL ETH"
  → Send to Telegram Bot
```

### 2.7: Multi-Timeframe Analysis
```
// Get multiple timeframes
1h data: &interval=1h&limit=24
4h data: &interval=4h&limit=24  
1d data: &interval=1d&limit=30

// Send all to Claude for comprehensive analysis
Prompt: "Analyze ETH across 1h, 4h, and daily timeframes. 
Provide overall signal strength and confidence level."
```

### 2.8: Multiple Coins
```
// Get data for ETH, BTC, CRO
ETH: symbol=ETHUSDT
BTC: symbol=BTCUSDT  
CRO: symbol=CROUSDT

// Send all to Claude
Prompt: "Calculate RSI for ETH, BTC, and CRO. 
Return which coins are overbought/oversold."
```

## Shortcut Structure Summary
```
1. Get OHLCV from Binance (ETH) ✅ Unlimited
2. Format prompt for Claude ✅  
3. Send to Claude API ✅ Gets RSI, SMA, MACD
4. Parse Claude's JSON response ✅
5. Extract indicators (RSI, SMA, etc.) ✅
6. Alert logic based on thresholds ✅
7. Send notifications ✅
```

## Advantages of This Approach

✅ **Unlimited API calls** (Binance is free)
✅ **Accurate calculations** (Claude does the math)  
✅ **Flexible indicators** (ask Claude for any indicator)
✅ **Natural language analysis** (Claude can explain signals)
✅ **Multiple timeframes** (1m, 5m, 1h, 4h, 1d)
✅ **Multiple cryptocurrencies** 
✅ **No complex parsing** (Claude returns structured JSON)

## Costs
- **Binance API**: Free, unlimited
- **Claude API**: ~$0.003 per request (very cheap)
- **Total cost**: ~$0.09/month for 30 daily checks

## Error Handling
```
Add Action: If (check if Gemini response is valid)
If Gemini_Response contains "current_price"  
  → Continue with alerts
Otherwise
  → Show Notification: "⚠️ Technical analysis failed, check manually"
```

## Pro Tips

1. **Batch multiple coins** in one Gemini request to save API calls
2. **Use specific prompts** for consistent JSON responses  
3. **Add confidence levels** - ask Gemini how confident it is
4. **Historical backtesting** - ask Gemini to analyze past patterns
5. **Risk management** - include position sizing recommendations
6. **Use temperature 0.1** for consistent mathematical calculations

## Testing Your Shortcut

1. **Test Binance API** - verify OHLCV data loads
2. **Test Gemini prompt** - ensure JSON response format
3. **Test parsing** - verify indicators extract correctly  
4. **Test alerts** - confirm notifications trigger
5. **Test automation** - set up recurring execution

## Sample Complete Prompt for Gemini

```
You are a crypto technical analyst. Based on this ETH OHLCV data from Binance:

[OHLCV_DATA]

Calculate these indicators and provide analysis:
- RSI (14-period)
- SMA20 (20-day simple moving average)  
- MACD (12,26,9)
- Support/Resistance levels

Return ONLY this JSON:
{
  "current_price": number,
  "rsi": number,
  "sma20": number, 
  "macd_line": number,
  "macd_signal": number,
  "support": number,
  "resistance": number,
  "signals": {
    "rsi_signal": "overbought|oversold|neutral",
    "trend": "bullish|bearish|sideways", 
    "recommendation": "strong_buy|buy|hold|sell|strong_sell",
    "confidence": "high|medium|low"
  },
  "summary": "brief analysis in 1 sentence"
}
```

This approach gives you unlimited, accurate technical analysis with the flexibility to ask Gemini for any kind of market insight!