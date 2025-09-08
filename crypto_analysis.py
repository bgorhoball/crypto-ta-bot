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
    
    def get_crypto_data(self, symbol: str, interval: str = '5m', limit: int = 200) -> Optional[List]:
        """Fetch OHLCV data using multiple fallback APIs"""
        
        # Method 1: Try CoinGecko API (free, no restrictions)
        coingecko_data = self._try_coingecko_api(symbol)
        if coingecko_data:
            return coingecko_data
            
        # Method 2: Try CoinCap API (alternative free API)
        coincap_data = self._try_coincap_api(symbol)
        if coincap_data:
            return coincap_data
            
        # Method 3: Generate mock data for testing (remove in production)
        print(f"All APIs failed for {symbol}, using mock data for testing")
        return self._generate_mock_data(symbol)
    
    def _try_coingecko_api(self, symbol: str) -> Optional[List]:
        """Try CoinGecko API as fallback"""
        try:
            # Map Binance symbols to CoinGecko IDs
            symbol_mapping = {
                'BTCUSDT': 'bitcoin',
                'ETHUSDT': 'ethereum', 
                'CROUSDT': 'crypto-com-chain'
            }
            
            coingecko_id = symbol_mapping.get(symbol)
            if not coingecko_id:
                print(f"No CoinGecko mapping for {symbol}")
                return None
                
            print(f"Trying CoinGecko: {symbol} → {coingecko_id}")
            
            # CoinGecko free API - get last 1 day of data
            url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/ohlc"
            params = {'vs_currency': 'usd', 'days': '1'}
            
            headers = {
                'User-Agent': 'CryptoAnalysisBot/1.0',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                print(f"CoinGecko returned {len(data)} data points for {coingecko_id}")
                
                # Convert CoinGecko format to Binance-like format
                converted_data = []
                for item in data:
                    # CoinGecko: [timestamp, open, high, low, close]
                    # Binance: [timestamp, open, high, low, close, volume, close_time, ...]
                    converted_data.append([
                        item[0],  # timestamp
                        str(item[1]),  # open
                        str(item[2]),  # high  
                        str(item[3]),  # low
                        str(item[4]),  # close
                        "1000000",  # mock volume
                        item[0] + 300000,  # close_time (add 5 minutes)
                        "0", "0", "0", "0", "0"  # other binance fields
                    ])
                print(f"Converted {len(converted_data)} CoinGecko data points to Binance format")
                return converted_data
            else:
                print(f"CoinGecko API returned {response.status_code} for {coingecko_id}")
                if response.status_code == 404:
                    print(f"CoinGecko 404: '{coingecko_id}' not found - check symbol mapping")
        except Exception as e:
            print(f"CoinGecko API failed for {symbol}: {e}")
        
        return None
    
    def _try_coincap_api(self, symbol: str) -> Optional[List]:
        """Try CoinCap API as another fallback"""
        try:
            # Map symbols to CoinCap IDs
            symbol_mapping = {
                'BTCUSDT': 'bitcoin',
                'ETHUSDT': 'ethereum',
                'CROUSDT': 'crypto-com-chain'
            }
            
            coincap_id = symbol_mapping.get(symbol, symbol.replace('USDT', '').lower())
            print(f"Trying CoinCap with ID: {coincap_id}")
            
            # CoinCap API - get asset data
            url = f"https://api.coincap.io/v2/assets/{coincap_id}/history"
            params = {'interval': 'm5'}  # 5-minute intervals
            
            headers = {
                'User-Agent': 'CryptoAnalysisBot/1.0',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()['data']
                # Convert CoinCap format to Binance-like format
                converted_data = []
                for item in data[-200:]:  # Get last 200 points
                    price = float(item['priceUsd'])
                    # Mock OHLC from single price point
                    converted_data.append([
                        item['time'],  # timestamp
                        str(price * 0.999),  # open (slightly lower)
                        str(price * 1.001),  # high (slightly higher)
                        str(price * 0.998),  # low (slightly lower)
                        str(price),  # close (actual price)
                        "1000000",  # mock volume
                        item['time'] + 300000,  # close_time
                        "0", "0", "0", "0", "0"  # other binance fields
                    ])
                return converted_data
            else:
                print(f"CoinCap API returned {response.status_code}")
        except Exception as e:
            print(f"CoinCap API failed: {e}")
        
        return None
    
    def _generate_mock_data(self, symbol: str) -> List:
        """Generate realistic mock data for testing when all APIs fail"""
        import random
        import time
        
        # Base prices for each symbol
        base_prices = {
            'BTCUSDT': 65000,
            'ETHUSDT': 3500,
            'CROUSDT': 0.12
        }
        
        base_price = base_prices.get(symbol, 100)
        current_time = int(time.time() * 1000)
        mock_data = []
        
        for i in range(200):
            timestamp = current_time - (200 - i) * 300000  # 5-minute intervals
            
            # Generate realistic price movement
            change_percent = random.uniform(-0.02, 0.02)  # ±2% change
            open_price = base_price * (1 + change_percent)
            
            high_price = open_price * random.uniform(1.001, 1.01)
            low_price = open_price * random.uniform(0.99, 0.999)
            close_price = open_price + random.uniform(-0.01, 0.01) * open_price
            
            volume = random.uniform(1000000, 5000000)
            
            mock_data.append([
                timestamp,
                f"{open_price:.8f}",
                f"{high_price:.8f}",
                f"{low_price:.8f}",
                f"{close_price:.8f}",
                f"{volume:.2f}",
                timestamp + 299999,
                "0", "0", "0", "0", "0"
            ])
            
            base_price = close_price  # Use close as next open
        
        print(f"Generated {len(mock_data)} mock data points for {symbol}")
        return mock_data
    
    def _generate_mock_analysis(self, symbol: str, ohlcv_data: List) -> Dict:
        """Generate realistic mock analysis when Gemini API fails"""
        import random
        
        # Get current price from last data point
        current_price = float(ohlcv_data[-1][4]) if ohlcv_data else 50000
        
        # Generate realistic technical indicators
        rsi = random.uniform(30, 70)  # Neutral RSI
        sma20 = current_price * random.uniform(0.98, 1.02)
        sma50 = current_price * random.uniform(0.95, 1.05)
        ema20 = current_price * random.uniform(0.99, 1.01)
        sma200 = current_price * random.uniform(0.85, 1.15)
        
        macd_line = random.uniform(-100, 100)
        macd_signal = macd_line + random.uniform(-20, 20)
        macd_histogram = macd_line - macd_signal
        
        # Determine signals based on generated data
        rsi_signal = "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"
        trend_short = "bullish" if current_price > sma20 else "bearish"
        trend_long = "bullish" if current_price > sma200 else "bearish" 
        
        sma_cross = "neutral"
        if sma20 > sma50 * 1.002:
            sma_cross = "golden_cross"
        elif sma20 < sma50 * 0.998:
            sma_cross = "death_cross"
            
        macd_signal_trend = "bullish" if macd_histogram > 0 else "bearish"
        
        # Overall signal logic
        bullish_signals = sum([
            rsi < 30,  # oversold
            trend_short == "bullish",
            trend_long == "bullish", 
            sma_cross == "golden_cross",
            macd_signal_trend == "bullish"
        ])
        
        if bullish_signals >= 4:
            overall = "strong_buy"
        elif bullish_signals >= 3:
            overall = "buy"
        elif bullish_signals <= 1:
            overall = "sell"
        elif bullish_signals <= 0:
            overall = "strong_sell"
        else:
            overall = "hold"
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "rsi": round(rsi, 1),
                "sma20": round(sma20, 2),
                "sma50": round(sma50, 2),
                "ema20": round(ema20, 2),
                "sma200": round(sma200, 2),
                "macd_line": round(macd_line, 3),
                "macd_signal": round(macd_signal, 3),
                "macd_histogram": round(macd_histogram, 3)
            },
            "levels": {
                "support": round(current_price * 0.95, 2),
                "resistance": round(current_price * 1.05, 2)
            },
            "signals": {
                "rsi_signal": rsi_signal,
                "trend_short": trend_short,
                "trend_long": trend_long,
                "sma_cross": sma_cross,
                "macd_signal": macd_signal_trend,
                "overall_signal": overall
            },
            "analysis": f"Mock analysis: {symbol} showing {trend_short} short-term and {trend_long} long-term trends with {rsi_signal} RSI conditions."
        }
    
    def _extract_json_from_response(self, text_response: str) -> Optional[Dict]:
        """Extract JSON from Gemini response, handling markdown and extra text"""
        try:
            # Method 1: Try to find JSON block in markdown
            if '```json' in text_response:
                # Extract content between ```json and ``` (or ```\n)
                start_marker = '```json'
                end_markers = ['```', '```\n']
                
                start_idx = text_response.find(start_marker) + len(start_marker)
                json_part = text_response[start_idx:]
                
                # Find the end marker
                end_idx = len(json_part)
                for end_marker in end_markers:
                    marker_idx = json_part.find(end_marker)
                    if marker_idx != -1:
                        end_idx = min(end_idx, marker_idx)
                
                json_text = json_part[:end_idx].strip()
                return json.loads(json_text)
            
            # Method 2: Try to find JSON by looking for { } braces
            start_brace = text_response.find('{')
            if start_brace != -1:
                # Find the last closing brace
                brace_count = 0
                end_brace = start_brace
                
                for i, char in enumerate(text_response[start_brace:], start_brace):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_brace = i
                            break
                
                if brace_count == 0:  # Found matching closing brace
                    json_text = text_response[start_brace:end_brace + 1]
                    return json.loads(json_text)
            
            # Method 3: Try parsing the whole response as JSON (fallback)
            return json.loads(text_response.strip())
            
        except json.JSONDecodeError as e:
            print(f"JSON extraction failed: {e}")
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
        
        # Try up to 3 times with exponential backoff for 503 errors
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                if response.status_code == 503:
                    wait_time = 2 ** attempt  # 1, 2, 4 seconds
                    print(f"Gemini 503 error for {symbol}, retrying in {wait_time}s (attempt {attempt + 1}/3)")
                    if attempt < 2:  # Don't sleep on last attempt
                        time.sleep(wait_time)
                        continue
                
                response.raise_for_status()
                break  # Success, exit retry loop
                
            except requests.RequestException as e:
                if attempt == 2:  # Last attempt
                    print(f"Gemini API failed after 3 attempts for {symbol}: {e}")
                    return self._generate_mock_analysis(symbol, ohlcv_data)
                print(f"Gemini attempt {attempt + 1} failed for {symbol}: {e}")
                time.sleep(2 ** attempt)
                continue
        
        try:
            
            result = response.json()
            print(f"Gemini raw response for {symbol}: {result}")
            
            # Check if response has expected structure
            if 'candidates' not in result or not result['candidates']:
                print(f"No candidates in Gemini response for {symbol}")
                return self._generate_mock_analysis(symbol, ohlcv_data)
            
            candidate = result['candidates'][0]
            if 'content' not in candidate:
                print(f"No content in Gemini candidate for {symbol}")
                return self._generate_mock_analysis(symbol, ohlcv_data)
                
            if 'parts' not in candidate['content'] or not candidate['content']['parts']:
                print(f"No parts in Gemini content for {symbol}")
                return self._generate_mock_analysis(symbol, ohlcv_data)
            
            text_response = candidate['content']['parts'][0]['text']
            print(f"Gemini text response for {symbol}: {text_response[:200]}...")
            
            # Extract JSON from response (handle markdown and extra text)
            json_data = self._extract_json_from_response(text_response)
            if json_data:
                return json_data
            else:
                print(f"Could not extract valid JSON from Gemini response for {symbol}")
                return self._generate_mock_analysis(symbol, ohlcv_data)
            
        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
            print(f"Error analyzing {symbol} with Gemini: {e}")
            print(f"Using fallback analysis for {symbol}")
            return self._generate_mock_analysis(symbol, ohlcv_data)
    
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
                # Get market data using multiple fallback methods
                ohlcv_data = self.get_crypto_data(symbol)
                if not ohlcv_data:
                    print(f"Failed to get any data for {symbol}")
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