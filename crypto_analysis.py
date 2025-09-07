#!/usr/bin/env python3
"""
Crypto Technical Analysis Bot
Analyzes BTC, ETH, CRO using Gemini AI and sends Telegram notifications
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class CryptoAnalyzer:
    def __init__(self):
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        self.coins = ['BTCUSDT', 'ETHUSDT', 'CROUSDT']
        self.coin_names = {'BTCUSDT': 'Bitcoin', 'ETHUSDT': 'Ethereum', 'CROUSDT': 'Cronos'}
        
        if not all([self.gemini_api_key, self.telegram_token, self.telegram_chat_id]):
            raise ValueError("Missing required environment variables")
    
    def get_binance_data(self, symbol: str, interval: str = '5m', limit: int = 200) -> Optional[List]:
        """Fetch OHLCV data from Binance API"""
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {symbol} data: {e}")
            return None
    
    def analyze_with_gemini(self, symbol: str, ohlcv_data: List) -> Optional[Dict]:
        """Send data to Gemini for technical analysis"""
        if not ohlcv_data:
            return None
            
        # Format data for Gemini (last 200 5-minute candles)
        formatted_data = []
        for candle in ohlcv_data:
            formatted_data.append({
                'timestamp': candle[0],
                'open': float(candle[1]),
                'high': float(candle[2]),
                'low': float(candle[3]),
                'close': float(candle[4]),
                'volume': float(candle[5])
            })
        
        prompt = f"""
Analyze {symbol} technical indicators based on this 5-minute OHLCV data:
{json.dumps(formatted_data[-50:], indent=2)}  

Calculate these indicators:
- RSI (14-period)
- SMA20, SMA50, EMA20, SMA200
- MACD (12,26,9)
- Support/Resistance levels

Analyze current market conditions and return ONLY this JSON:
{{
  "symbol": "{symbol}",
  "current_price": number,
  "timestamp": "{datetime.now().isoformat()}",
  "indicators": {{
    "rsi": number,
    "sma20": number,
    "sma50": number,
    "ema20": number,
    "sma200": number,
    "macd_line": number,
    "macd_signal": number,
    "macd_histogram": number
  }},
  "levels": {{
    "support": number,
    "resistance": number
  }},
  "signals": {{
    "rsi_signal": "overbought|oversold|neutral",
    "trend_short": "bullish|bearish|neutral",
    "trend_long": "bullish|bearish|neutral", 
    "sma_cross": "golden_cross|death_cross|neutral",
    "macd_signal": "bullish|bearish|neutral",
    "overall_signal": "strong_buy|buy|hold|sell|strong_sell"
  }},
  "analysis": "Brief 1-2 sentence market analysis"
}}
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            
            # Parse JSON from response
            return json.loads(text_response)
            
        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
            print(f"Error analyzing {symbol} with Gemini: {e}")
            return None
    
    def format_analysis_message(self, analysis: Dict) -> str:
        """Format analysis data into readable Telegram message"""
        symbol = analysis['symbol']
        coin_name = self.coin_names.get(symbol, symbol)
        indicators = analysis['indicators']
        signals = analysis['signals']
        
        # Create emoji indicators
        def get_trend_emoji(signal):
            if signal == 'bullish' or signal == 'buy' or signal == 'strong_buy':
                return '🟢'
            elif signal == 'bearish' or signal == 'sell' or signal == 'strong_sell':
                return '🔴'
            else:
                return '🟡'
        
        def get_rsi_emoji(rsi):
            if rsi > 70:
                return '⚠️ Overbought'
            elif rsi < 30:
                return '💰 Oversold'
            else:
                return '➡️ Neutral'
        
        message = f"""
🚀 **{coin_name} ({symbol})** Analysis

💲 **Price:** ${analysis['current_price']:.2f}

📊 **Technical Indicators:**
• RSI(14): {indicators['rsi']:.1f} {get_rsi_emoji(indicators['rsi'])}
• SMA20: ${indicators['sma20']:.2f}
• SMA50: ${indicators['sma50']:.2f}
• EMA20: ${indicators['ema20']:.2f}
• SMA200: ${indicators['sma200']:.2f}

📈 **MACD:**
• Line: {indicators['macd_line']:.3f}
• Signal: {indicators['macd_signal']:.3f}
• Histogram: {indicators['macd_histogram']:.3f}

🎯 **Signals:**
• RSI: {signals['rsi_signal'].title()}
• Short Trend: {get_trend_emoji(signals['trend_short'])} {signals['trend_short'].title()}
• Long Trend: {get_trend_emoji(signals['trend_long'])} {signals['trend_long'].title()}
• SMA Cross: {signals['sma_cross'].replace('_', ' ').title()}
• MACD: {get_trend_emoji(signals['macd_signal'])} {signals['macd_signal'].title()}

🔔 **Overall Signal:** {get_trend_emoji(signals['overall_signal'])} **{signals['overall_signal'].replace('_', ' ').upper()}**

📝 **Analysis:** {analysis['analysis']}

🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """
        
        return message.strip()
    
    def send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        
        data = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def should_send_notification(self, analysis: Dict) -> bool:
        """Determine if analysis warrants a notification"""
        if not analysis:
            return False
            
        signals = analysis['signals']
        indicators = analysis['indicators']
        
        # Send notification for:
        # 1. Extreme RSI conditions
        if indicators['rsi'] > 70 or indicators['rsi'] < 30:
            return True
            
        # 2. Strong buy/sell signals
        if signals['overall_signal'] in ['strong_buy', 'strong_sell']:
            return True
            
        # 3. Golden/Death cross
        if signals['sma_cross'] in ['golden_cross', 'death_cross']:
            return True
            
        # 4. Strong MACD signals
        if signals['macd_signal'] in ['bullish', 'bearish'] and abs(indicators['macd_histogram']) > 0.1:
            return True
            
        return False
    
    def analyze_all_coins(self):
        """Main function to analyze all coins and send notifications"""
        print(f"Starting crypto analysis at {datetime.now()}")
        
        for symbol in self.coins:
            try:
                # Get market data
                ohlcv_data = self.get_binance_data(symbol)
                if not ohlcv_data:
                    continue
                
                # Analyze with Gemini
                analysis = self.analyze_with_gemini(symbol, ohlcv_data)
                if not analysis:
                    continue
                
                # Check if notification needed
                if self.should_send_notification(analysis):
                    message = self.format_analysis_message(analysis)
                    success = self.send_telegram_message(message)
                    
                    if success:
                        print(f"✅ Sent notification for {symbol}")
                    else:
                        print(f"❌ Failed to send notification for {symbol}")
                else:
                    print(f"ℹ️ No significant signals for {symbol}")
                
                # Rate limiting - wait between API calls
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        print("Analysis complete")

def main():
    """Entry point for the script"""
    try:
        analyzer = CryptoAnalyzer()
        analyzer.analyze_all_coins()
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()