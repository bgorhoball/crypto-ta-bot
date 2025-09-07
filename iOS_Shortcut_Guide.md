# Complete iOS Shortcut Build Guide: Crypto Technical Analysis

## Prerequisites Setup

### Get Your Gemini API Key
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")
5. Save it securely

## Building the Shortcut: Step-by-Step

### Open iOS Shortcuts App
1. Open **Shortcuts** app on your iPhone/iPad
2. Tap **"+"** to create new shortcut
3. Tap shortcut name at top, rename to: **"Crypto Analysis"**

---

## Action 1: Get Binance Data

**Add Action:**
1. Search: **"Get Contents of URL"**
2. Tap to add it

**Configure:**
- **URL:** `https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit=21`
- **Method:** GET
- **Headers:** (leave empty)

---

## Action 2: Store Raw Data

**Add Action:**
1. Search: **"Set Variable"** 
2. Tap to add it

**Configure:**
- **Variable Name:** `RawData`
- **Value:** Tap and select **"Contents of URL"** from previous action

---

## Action 3: Create Gemini Prompt

**Add Action:**
1. Search: **"Text"**
2. Tap to add it

**Configure Text Content:** (copy the text below, DO NOT include the backticks ```):

Calculate technical indicators for ETH based on this OHLCV data: [tap here and select "RawData" variable]

Please calculate and return ONLY a JSON response with:
- Current Price (from latest close)
- RSI (14-period)
- SMA20 (20-day Simple Moving Average)
- MACD (12,26,9)

Format response as valid JSON:
{
  "current_price": number,
  "rsi": number,
  "sma20": number,
  "macd_line": number,
  "macd_signal": number,
  "macd_histogram": number
}

CRITICAL: Return ONLY the JSON object, no markdown, no explanations, no extra text.

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `GeminiPrompt`
- **Value:** Select "Text" from previous action

---

## Action 4: Call Gemini API

### Method 1: Direct URL Input (Try This First)

**Add Action:**
1. Search: **"Get Contents of URL"**
2. Tap to add it

**Configure:**
- **URL:** Try pasting this (replace YOUR_GEMINI_API_KEY with your actual key):
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_GEMINI_API_KEY`

### Method 2: If URL Input Fails (Use This Alternative)

**Add Action:**
1. Search: **"Text"**
2. Tap to add it

**Configure Text Content:**
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_GEMINI_API_KEY

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `GeminiURL`
- **Value:** Select "Text" from previous action

**Add Action:**
1. Search: **"Get Contents of URL"**
2. Tap to add it

**Configure:**
- **URL:** Select "GeminiURL" variable

### Continue Configuration (Both Methods):
- **Method:** POST
- **Headers:** 
  - Tap "Add Field"
  - **Name:** `Content-Type`
  - **Value:** `application/json`

**Request Body:** (tap "Request Body" then "JSON", DO NOT include the json or backticks):
{
  "contents": [{
    "parts": [{
      "text": "GeminiPrompt"
    }]
  }],
  "generationConfig": {
    "temperature": 0.1,
    "topK": 1,
    "topP": 1,
    "maxOutputTokens": 1000
  }
}

*Note: For the "text" value, tap "GeminiPrompt" and select the variable*

---

## Action 5: Extract Gemini Response

**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Contents of URL" (from Gemini API call)
- **Get Value for:** Type: `candidates`

**Add Action:**
1. Search: **"Get Item from List"**
2. Tap to add it

**Configure:**
- **List:** Select previous "Get Value for" result
- **Item:** First Item

**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Get Item from List" result
- **Get Value for:** Type: `content`

**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select previous "Get Value for" result  
- **Get Value for:** Type: `parts`

**Add Action:**
1. Search: **"Get Item from List"**
2. Tap to add it

**Configure:**
- **List:** Select previous "Get Value for" result
- **Item:** First Item

**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Get Item from List" result
- **Get Value for:** Type: `text`

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `GeminiResponse`
- **Value:** Select previous "Get Value for" result

---

## Action 6: Parse JSON Response

**Add Action:**
1. Search: **"Get Dictionary from Input"**
2. Tap to add it

**Configure:**
- **Input:** Select "GeminiResponse" variable

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `Indicators`
- **Value:** Select "Get Dictionary from Input" result

---

## Action 7: Extract Individual Values

**For Current Price:**
**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Indicators" variable
- **Get Value for:** Type: `current_price`

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `ETHPrice`
- **Value:** Select previous "Get Value for" result

**For RSI:**
**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Indicators" variable
- **Get Value for:** Type: `rsi`

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `ETHRSI`
- **Value:** Select previous "Get Value for" result

**For SMA20:**
**Add Action:**
1. Search: **"Get Value for"**
2. Tap to add it

**Configure:**
- **Dictionary:** Select "Indicators" variable
- **Get Value for:** Type: `sma20`

**Add Action:**
1. Search: **"Set Variable"**
2. Tap to add it

**Configure:**
- **Variable Name:** `ETHSMA20`
- **Value:** Select previous "Get Value for" result

---

## Action 8: RSI Alert Logic

**Add Action:**
1. Search: **"If"**
2. Tap to add it

**Configure:**
- **If:** Select "ETHRSI" variable
- **Condition:** is greater than
- **Value:** Type: `70`

**Inside the "If" block:**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Overbought Alert`
- **Body:** Type: `⚠️ ETH RSI: ` then tap to add "ETHRSI" variable

**Add "Otherwise If":**
1. Tap "Add to If" at bottom of If block
2. Select "Otherwise If"

**Configure:**
- **If:** Select "ETHRSI" variable  
- **Condition:** is less than
- **Value:** Type: `30`

**Inside the "Otherwise If" block:**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Oversold Alert`
- **Body:** Type: `💰 ETH RSI: ` then tap to add "ETHRSI" variable

---

## Action 9: Price vs SMA Alert

**Add Action:**
1. Search: **"If"**
2. Tap to add it

**Configure:**
- **If:** Select "ETHPrice" variable
- **Condition:** is greater than  
- **Value:** Select "ETHSMA20" variable

**Inside the "If" block:**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Trend Alert`
- **Body:** `📈 ETH above SMA20 - Bullish trend`

**Add "Otherwise":**
1. Tap "Add to If" at bottom of If block
2. Select "Otherwise"

**Inside the "Otherwise" block:**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Trend Alert`  
- **Body:** `📉 ETH below SMA20 - Bearish trend`

---

## Action 10: Price Level Alert

**Add Action:**
1. Search: **"If"**
2. Tap to add it

**Configure:**
- **If:** Select "ETHPrice" variable
- **Condition:** is greater than
- **Value:** Type: `5000`

**Inside the "If" block:**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Price Alert`
- **Body:** `🚨 ETH hit $5000!`

---

## Action 11: Summary Notification

**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `ETH Analysis Complete`
- **Body:** Tap and create text like: `Price: $` [ETHPrice] ` | RSI: ` [ETHRSI] ` | SMA20: $` [ETHSMA20]

---

## Testing Your Shortcut

### Manual Test:
1. Tap shortcut name at top
2. Tap "Play" button (▶️)  
3. Watch for notifications

### Expected Results:
- Should get Binance data successfully
- Gemini should return JSON with indicators
- Notifications should appear based on current ETH conditions

---

## Error Handling (Optional Enhancement)

**Before Action 6, add error checking:**

**Add Action:**
1. Search: **"If"**
2. Tap to add it

**Configure:**
- **If:** Select "GeminiResponse" variable
- **Condition:** contains
- **Value:** Type: `current_price`

**Inside "If" block:** Continue with Actions 6-11

**Add "Otherwise":**
**Add Action:**
1. Search: **"Show Notification"**
2. Tap to add it

**Configure:**
- **Title:** `Analysis Failed`
- **Body:** `⚠️ Technical analysis failed, check manually`

---

## Automation Setup

**To run automatically:**
1. Go to **Automation** tab in Shortcuts app
2. Tap **"+"** 
3. Select **"Time of Day"**
4. Set desired schedule (e.g., 9 AM daily)
5. Select your "Crypto Analysis" shortcut
6. Toggle **"Ask Before Running"** OFF

---

## Troubleshooting

### Common Issues:

**Cannot Input Long URL (Step 4):**
- Try Method 2: Use Text action to build URL first
- Make sure you replace YOUR_GEMINI_API_KEY with actual key
- Copy URL in smaller chunks if needed
- Use Notes app to prepare the URL, then copy/paste

**"Invalid JSON" Error:**
- Check Gemini API key is correct
- Ensure request body JSON is properly formatted (don't include ```json or backticks)
- Verify variable selections are correct

**"No Data" Error:**  
- Test Binance API URL in browser first
- Check internet connection
- Verify ETHUSDT symbol is correct

**Variables Not Found:**
- Ensure variable names match exactly
- Check that "Set Variable" actions completed successfully
- Verify variable selections in subsequent actions

**Notifications Not Appearing:**
- Check iOS notification permissions for Shortcuts app
- Ensure "Show Notification" actions are properly configured
- Test with simple notification first

**Text Formatting Issues:**
- Never include backticks (```) when copying code
- Backticks are just markdown formatting in the guide
- Copy only the actual content between the backticks

### Testing Individual Parts:

**Test Binance API:**
- Create simple shortcut with just Action 1
- Check output shows OHLCV array data

**Test Gemini API:**
- Create shortcut with Actions 3-4 only  
- Use simple prompt like "Return JSON: {\"test\": 123}"
- Verify response structure

**Test JSON Parsing:**
- Use known good JSON string
- Test "Get Dictionary from Input" action
- Verify value extraction works

---

## Advanced Customizations

### Multiple Cryptocurrencies:
Change Binance URL symbol parameter:
- Bitcoin: `symbol=BTCUSDT`
- Cardano: `symbol=ADAUSDT` 
- Solana: `symbol=SOLUSDT`

### Different Timeframes:
Change interval parameter:
- 1 hour: `interval=1h`
- 4 hours: `interval=4h`
- 1 week: `interval=1w`

### Additional Indicators:
Modify Gemini prompt to request:
- Bollinger Bands
- Stochastic RSI  
- Volume analysis
- Support/resistance levels

### Enhanced Notifications:
- Add sound alerts
- Send to Telegram bot
- Log to Notes app
- Email summaries

---

This complete guide provides everything needed to manually build the crypto technical analysis shortcut in your iOS Shortcuts app. Follow each step carefully and test frequently to ensure proper functionality.