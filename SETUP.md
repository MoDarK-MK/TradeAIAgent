# 🚀 AI Trading Agent - Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Docker & Docker Compose**
- **TA-Lib** (Technical Analysis Library)

## 🔧 Installation

### Option 1: Docker (Recommended)

1. **Clone and navigate to the project:**

   ```powershell
   cd c:\Users\modark\Desktop\mobile\TradeAIAgent
   ```

2. **Create environment file:**

   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your settings
   ```

3. **Build and start services:**

   ```powershell
   docker-compose up -d
   ```

4. **Access the application:**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Option 2: Local Development

1. **Create virtual environment:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install TA-Lib (Windows):**
   Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

   ```powershell
   pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment:**

   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your settings
   ```

5. **Start PostgreSQL and Redis** (or use Docker for just these):

   ```powershell
   docker-compose up -d postgres redis
   ```

6. **Run the application:**
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📝 Running Examples

### Example 1: Basic Usage (with g4f LLM)

```powershell
python run_agent.py
```

This will:

- Initialize the trading agent with g4f
- Generate sample BTC/USD data
- Perform technical analysis
- Generate AI-powered trading recommendations via g4f
- Display LLM analysis
- **No API key required!**

### Example 2: API Usage

```python
import requests
import numpy as np

data = {
    "symbol": "BTC/USD",
    "timeframe": "1H",
    "ohlcv": {
        "open": [42000, 42100, 42200],
        "high": [42200, 42300, 42400],
        "low": [41900, 42000, 42100],
        "close": [42100, 42200, 42300],
        "volume": [1000000, 1200000, 1100000]
    },
    "capital": 10000,
    "risk_percent": 2.0
}

response = requests.post("http://localhost:8000/analyze", json=data)
analysis = response.json()

print(f"Signal: {analysis['signal']['type']}")
print(f"LLM Analysis: {analysis.get('llm_analysis')}")
```

## 🧪 Running Tests

```powershell
# Install pytest if not already installed
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

## 🌐 API Endpoints

### POST /analyze

Analyze trading chart and generate signals.

**Request:**

```json
{
  "symbol": "BTC/USD",
  "timeframe": "1H",
  "ohlcv": {
    "open": [...],
    "high": [...],
    "low": [...],
    "close": [...],
    "volume": [...]
  },
  "image_base64": "optional_base64_string",
  "capital": 10000,
  "risk_percent": 2.0
}
```

**Response:**

```json
{
  "signal": {
    "type": "BUY",
    "confidence": 82.5,
    "strength": "STRONG",
    "quality_score": 85.0,
    "confluence_count": 5
  },
  "entry": {...},
  "stop_loss": {...},
  "take_profit": {...},
  "risk_reward": {...},
  "technical_details": {...},
  "recommendations": [...]
}
```

### WebSocket /ws/signals

Real-time signal streaming.

**JavaScript Example:**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/signals");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("New signal:", data);
};
```

### GET /summary

Get analysis history summary.

### GET /indicators/list

List all available technical indicators.

### GET /health

Health check endpoint.

## 🔧 Configuration

Edit [.env](.env) file to configure:

```env
# Trading Configuration
DEFAULT_CAPITAL=10000
MAX_RISK_PERCENT=2.0
MAX_DAILY_LOSS_PERCENT=5.0
MAX_DRAWDOWN_PERCENT=15.0

# Database
POSTGRES_HOST=localhost
POSTGRES_DB=trading_db

# Redis
REDIS_HOST=localhost

# API Keys (Optional)
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_secret
```

## 📊 Features

### Technical Indicators

- ✅ RSI (Relative Strength Index)
- ✅ MACD (Moving Average Convergence Divergence)
- ✅ Bollinger Bands
- ✅ Moving Averages (EMA21, SMA50, SMA200)
- ✅ ATR (Average True Range)
- ✅ Fibonacci Retracement
- ✅ ADX (Average Directional Index)
- ✅ Stochastic Oscillator
- ✅ Volume Analysis

### Signal Quality Features

- ✅ Confluence checking (multiple confirmation)
- ✅ Quality scoring (0-100)
- ✅ Multi-timeframe analysis
- ✅ Pattern recognition (15+ candlestick patterns)
- ✅ Support/Resistance detection

### Risk Management

- ✅ Dynamic Stop Loss (ATR, Level, Percentage)
- ✅ Multiple Take Profit targets (TP1, TP2, TP3)
- ✅ Position sizing calculator
- ✅ Risk/Reward ratio validation
- ✅ Daily loss limits
- ✅ Portfolio risk checks
- ✅ Trailing stop calculation

## 🔍 Troubleshooting

### TA-Lib Installation Issues

**Windows:**

1. Download wheel file from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. Install: `pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl`

**Linux:**

```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

### Docker Issues

If containers fail to start:

```powershell
docker-compose down -v
docker-compose up -d --build
```

### Port Already in Use

Change port in [.env](.env):

```env
PORT=8001
```

## 📚 Usage Examples

### Analyze Live Market Data

```python
from app.core.trading_agent import TradingAgent
import ccxt

# Initialize exchange
exchange = ccxt.binance()

# Fetch OHLCV data
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=100)

# Extract data
data = {
    'open': [x[1] for x in ohlcv],
    'high': [x[2] for x in ohlcv],
    'low': [x[3] for x in ohlcv],
    'close': [x[4] for x in ohlcv],
    'volume': [x[5] for x in ohlcv]
}

# Analyze
agent = TradingAgent(capital=10000)
analysis = agent.analyze(
    symbol='BTC/USDT',
    timeframe='1H',
    open_prices=np.array(data['open']),
    high=np.array(data['high']),
    low=np.array(data['low']),
    close=np.array(data['close']),
    volume=np.array(data['volume'])
)

print(f"Signal: {analysis['signal']['type']}")
print(f"Confidence: {analysis['signal']['confidence']}%")
```

## 🎯 Next Steps

1. **Integrate with Exchange APIs** - Connect to Binance, Forex brokers
2. **Add ML Models** - Pattern recognition enhancement
3. **Implement Backtesting** - Historical performance testing
4. **Build Frontend Dashboard** - React/Vue.js interface
5. **Add Alert System** - Email/SMS/Telegram notifications

## ⚠️ Disclaimer

**This software is for educational and professional use only.**

Trading financial instruments involves substantial risk of loss. Past performance is not indicative of future results. The developers of this software are not responsible for any financial losses incurred through its use. Always conduct your own research and consider consulting a financial advisor before making any trading decisions.

## 📞 Support

For issues, questions, or contributions:

- GitHub Issues: [Create an issue](https://github.com/yourusername/TradeAIAgent/issues)
- Documentation: [Read the docs](http://localhost:8000/docs)

## 📄 License

MIT License - See LICENSE file for details.

---

**Built with ❤️ for professional traders**
