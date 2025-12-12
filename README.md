# 🤖 AI Trading Agent - Enterprise-Grade Trading Intelligence Engine

A professional-grade AI-powered trading system that analyzes charts, generates signals, and manages risk across multiple assets and timeframes.

## 🎯 Features

- **Multi-Asset Support**: Crypto, Forex, Stocks, Commodities
- **Advanced Technical Analysis**: 10+ indicators (RSI, MACD, Bollinger Bands, Fibonacci, etc.)
- **Chart Image Analysis**: AI-powered pattern recognition using OpenCV and deep learning
- **Signal Quality Scoring**: 0-100 confidence with confluence validation
- **Professional Risk Management**: Dynamic SL/TP, position sizing, portfolio hedging
- **Real-time Streaming**: WebSocket support for live signals
- **Multi-Timeframe Analysis**: Daily, 4H, 1H, 15M coordination
- **Database Integration**: PostgreSQL/TimescaleDB for historical data

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- TA-Lib library

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd TradeAIAgent
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker

```bash
docker-compose up -d
```

### 3. Access the API

- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/signals

## 📁 Project Structure

```
TradeAIAgent/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── core/
│   │   ├── technical_analysis.py  # Technical indicators
│   │   ├── chart_analyzer.py      # Image processing
│   │   ├── signal_generator.py    # Signal logic
│   │   ├── risk_manager.py        # Risk calculations
│   │   └── trading_agent.py       # Main orchestrator
│   ├── models/
│   │   ├── database.py            # DB models
│   │   └── schemas.py             # Pydantic schemas
│   ├── api/
│   │   └── routes.py              # API endpoints
│   └── utils/
│       └── logger.py              # Logging utilities
├── tests/
│   └── test_trading_agent.py
├── examples/
│   └── example_usage.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🔧 API Endpoints

### POST /analyze

Analyze a trading chart and generate signals.

**Request:**

```json
{
  "image_base64": "base64_encoded_chart_image",
  "symbol": "BTC/USD",
  "timeframe": "1H",
  "capital": 10000,
  "risk_percent": 2.0
}
```

**Response:**

```json
{
  "signal": {
    "type": "BUY",
    "confidence": 82,
    "strength": "STRONG",
    "quality_score": 82,
    "confluence_count": 5
  },
  "entry": {
    "price": 42500,
    "description": "Bullish engulfing at MA200 support",
    "trigger": "IMMEDIATE"
  },
  "stop_loss": {
    "price": 41200,
    "distance_pips": 1300,
    "method": "LEVEL"
  },
  "take_profit": {
    "tp1": { "price": 43800, "ratio": 1.0 },
    "tp2": { "price": 45100, "ratio": 2.0 },
    "tp3": { "price": 46400, "ratio": 3.0 }
  },
  "risk_reward": {
    "ratio": 3.0,
    "status": "EXCELLENT"
  }
}
```

### WebSocket /ws/signals

Real-time signal streaming for live market monitoring.

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

## 📊 Technical Indicators Supported

- **RSI** (Relative Strength Index): Overbought/Oversold detection
- **MACD** (Moving Average Convergence Divergence): Trend momentum
- **Bollinger Bands**: Volatility analysis
- **Moving Averages**: EMA21, SMA50, SMA200
- **ATR** (Average True Range): Volatility measurement
- **Fibonacci**: Retracement and extension levels
- **ADX** (Average Directional Index): Trend strength
- **Stochastic**: Momentum oscillator
- **Volume Analysis**: Above/below average confirmation

## 🛡️ Risk Management Features

- **Dynamic Stop Loss**: ATR-based, level-based, percentage-based
- **Multi-Target Take Profit**: TP1 (1:1), TP2 (1:2), TP3 (1:3)
- **Position Sizing**: Automatic calculation based on risk %
- **Portfolio Limits**: Max 5 positions, correlation checking
- **Drawdown Protection**: Daily loss limits (5%), account max (15%)
- **Trailing Stop**: Automatic trailing after profit milestones

## 📈 Signal Quality Scoring

| Score Range | Quality      | Confluences | Action                  |
| ----------- | ------------ | ----------- | ----------------------- |
| 80-100      | Professional | 3+          | Strong recommendation   |
| 60-80       | Good         | 2+          | Moderate recommendation |
| 40-60       | Acceptable   | 1+          | Caution advised         |
| <40         | Weak         | 0           | Avoid trade             |

## 🔒 Safety & Ethics

✅ Always includes Stop Loss  
✅ Always validates Risk/Reward ratio  
✅ Confidence scoring on all signals  
✅ Position sizing recommendations  
✅ No guaranteed profit promises  
✅ Educational use disclaimer

## 🔐 Environment Variables

See `.env.example` for all configuration options.

**Critical Variables:**

- `DEFAULT_CAPITAL`: Trading capital amount
- `MAX_RISK_PERCENT`: Maximum risk per trade (2%)
- `MAX_DAILY_LOSS_PERCENT`: Daily loss limit (5%)
- `BINANCE_API_KEY/SECRET`: Exchange credentials

## 📞 Support

For issues, questions, or contributions, please open a GitHub issue.

## ⚖️ Disclaimer

**This software is for educational and professional use only.**  
Trading financial instruments involves substantial risk of loss. Past performance is not indicative of future results. Always conduct your own research and consider consulting a financial advisor.

## 📄 License

MIT License - See LICENSE file for details

---

Built with ❤️ for professional traders
