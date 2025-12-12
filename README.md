# 🤖 AI Trading Agent - Enterprise-Grade Trading Intelligence Engine

[![GitHub stars](https://img.shields.io/github/stars/MoDarK-MK/TradeAIAgent?style=social)](https://github.com/MoDarK-MK/TradeAIAgent)
[![GitHub forks](https://img.shields.io/github/forks/MoDarK-MK/TradeAIAgent?style=social)](https://github.com/MoDarK-MK/TradeAIAgent)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-enabled-blue?logo=docker)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009485.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![GitHub last commit](https://img.shields.io/github/last-commit/MoDarK-MK/TradeAIAgent?color=green)](https://github.com/MoDarK-MK/TradeAIAgent)
[![GitHub contributors](https://img.shields.io/github/contributors/MoDarK-MK/TradeAIAgent?color=blue)](https://github.com/MoDarK-MK/TradeAIAgent/graphs/contributors)

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
git clone https://github.com/MoDarK-MK/TradeAIAgent.git
cd TradeAIAgent
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker

```bash
docker-compose up -d
```

### 3. Access Services

- **FastAPI Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/signals
- **Health Check**: http://localhost:8000/health
- **Dashboard**: http://localhost:3000 (After running frontend)

### 4. Run Frontend (Optional)

```bash
cd frontend

# Using Python
python -m http.server 3000

# Or using Node.js
npx http-server -p 3000

# Then open http://localhost:3000 in your browser
```

## 📊 Dashboard UI/UX

Professional enterprise-grade dashboard with:

- ✨ Modern glassmorphism design with cyan/dark theme
- 📱 Fully responsive (mobile, tablet, desktop, ultra-wide)
- ♿ WCAG 2.1 AA accessibility compliance
- 🎨 Complete design system with 60+ components
- ⚡ Real-time chart analysis and visualization
- 🌙 Light/Dark mode theme toggle
- 🔄 Drag-and-drop chart upload
- 📊 Trade setup ladder with TP/SL visualization
- 📈 Technical indicators breakdown
- 🎯 Signal quality meter and badges
- 💾 Local storage persistence
- 🌐 WebSocket real-time updates

[See Frontend Documentation](frontend/README.md) for detailed UI/UX specs.

## 📁 Project Structure

```
TradeAIAgent/
├── app/                           # FastAPI Backend
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── core/
│   │   ├── technical_analysis.py  # Technical indicators (9 types)
│   │   ├── chart_analyzer.py      # Pattern recognition & S/R detection
│   │   ├── signal_generator.py    # Signal generation with confluence
│   │   ├── risk_manager.py        # SL/TP & position sizing
│   │   └── trading_agent.py       # Main orchestrator
│   ├── models/
│   │   ├── database.py            # PostgreSQL/TimescaleDB models
│   │   └── schemas.py             # Pydantic schemas
│   └── utils/
│       └── logger.py              # Logging configuration
├── frontend/                      # Professional Web Dashboard
│   ├── index.html                 # Main dashboard page
│   ├── css/
│   │   ├── design-system.css      # Color palette, typography, components
│   │   ├── dashboard.css          # Page-specific styles
│   │   └── responsive.css         # Mobile/tablet/desktop breakpoints
│   ├── js/
│   │   ├── utils.js               # Helper functions
│   │   ├── api.js                 # API client & WebSocket
│   │   └── dashboard.js           # Main application logic
│   ├── assets/                    # Images and fonts
│   ├── components/                # Reusable component templates
│   ├── pages/                     # Additional pages
│   └── README.md                  # Frontend documentation
├── tests/
│   └── test_trading_agent.py      # Unit tests
├── examples/
│   ├── example_usage.py           # Usage example
│   └── test_api.py                # API testing script
├── docker-compose.yml             # Docker services
├── Dockerfile                      # Application container
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── SETUP.md                        # Detailed setup guide
├── API.md                          # API documentation
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## �️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1 with Uvicorn
- **Technical Analysis**: TA-Lib 0.4.28, pandas-ta
- **Image Processing**: OpenCV 4.8.1, PIL
- **Database**: PostgreSQL 15, TimescaleDB (optional)
- **Cache**: Redis 7
- **ORM**: SQLAlchemy
- **Language**: Python 3.11+

### Frontend
- **HTML5**: Semantic markup with accessibility
- **CSS3**: Advanced features (Grid, Flexbox, CSS Variables)
- **JavaScript**: Vanilla JS (no frameworks required)
- **Design System**: Complete component library
- **API Client**: Fetch API with error handling
- **WebSocket**: Real-time signal streaming
- **Responsive**: Mobile-first design

## �🔧 API Endpoints

### POST /analyze

Analyze a trading chart and generate signals.

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

### GET /summary

Get analysis history summary.

### GET /indicators/list

List all available technical indicators.

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/

# Run example
python examples/example_usage.py

# Test API
python examples/test_api.py
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
✅ Always validates Risk/Reward ratio (minimum 1.5:1)  
✅ Confidence scoring on all signals  
✅ Position sizing recommendations  
✅ No guaranteed profit promises  
✅ Educational use disclaimer  
✅ Professional standards enforced

## 🔐 Environment Variables

See `.env.example` for all configuration options.

**Critical Variables:**

- `DEFAULT_CAPITAL`: Trading capital amount
- `MAX_RISK_PERCENT`: Maximum risk per trade (2%)
- `MAX_DAILY_LOSS_PERCENT`: Daily loss limit (5%)
- `BINANCE_API_KEY/SECRET`: Exchange credentials

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup and installation guide
- **[API.md](API.md)** - Complete API reference
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview

## 🙌 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:

- Open a [GitHub Issue](https://github.com/MoDarK-MK/TradeAIAgent/issues)
- Check [API Documentation](API.md)
- Review [Setup Guide](SETUP.md)

## 📊 Repository Stats

[![GitHub repo size](https://img.shields.io/github/repo-size/MoDarK-MK/TradeAIAgent)](https://github.com/MoDarK-MK/TradeAIAgent)
[![GitHub code size](https://img.shields.io/github/languages/code-size/MoDarK-MK/TradeAIAgent)](https://github.com/MoDarK-MK/TradeAIAgent)
[![GitHub top language](https://img.shields.io/github/languages/top/MoDarK-MK/TradeAIAgent)](https://github.com/MoDarK-MK/TradeAIAgent)

## ⚖️ Disclaimer

**This software is for educational and professional use only.**

Trading financial instruments involves substantial risk of loss. Past performance is not indicative of future results. Always conduct your own research and consider consulting a financial advisor before making any trading decisions.

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

Give a ⭐️ if you find this project helpful!

---

Built with ❤️ for professional traders | © 2025 TradeAIAgent
