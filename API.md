# 📖 API Documentation

Complete API reference for the AI Trading Agent.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API is open for development. In production, implement JWT authentication using the `SECRET_KEY` in `.env`.

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the service is running.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

---

### 2. Root Information

**GET** `/`

Get basic API information.

**Response:**

```json
{
  "message": "Welcome to AI Trading Agent",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 3. Analyze Trading Signal

**POST** `/analyze`

Perform comprehensive trading analysis.

**Request Body:**

```json
{
  "symbol": "BTC/USD",
  "timeframe": "1H",
  "ohlcv": {
    "open": [42000, 42100, 42200, ...],
    "high": [42200, 42300, 42400, ...],
    "low": [41900, 42000, 42100, ...],
    "close": [42100, 42200, 42300, ...],
    "volume": [1000000, 1200000, 1100000, ...]
  },
  "image_base64": "optional_base64_encoded_chart",
  "capital": 10000,
  "risk_percent": 2.0
}
```

**Parameters:**

- `symbol` (string, required): Trading pair (e.g., "BTC/USD", "EUR/USD")
- `timeframe` (string, required): Chart timeframe ("15M", "1H", "4H", "Daily")
- `ohlcv` (object, required): Price data with minimum 50 candles
  - `open` (array[float]): Opening prices
  - `high` (array[float]): High prices
  - `low` (array[float]): Low prices
  - `close` (array[float]): Closing prices
  - `volume` (array[float]): Volume data
- `image_base64` (string, optional): Base64 encoded chart image for visual analysis
- `capital` (float, optional, default=10000): Trading capital
- `risk_percent` (float, optional, default=2.0): Risk percentage per trade

**Response:**

```json
{
  "metadata": {
    "symbol": "BTC/USD",
    "timeframe": "1H",
    "timestamp": "2024-01-01T12:00:00.000000",
    "current_price": 42500.0
  },
  "signal": {
    "type": "BUY",
    "confidence": 82.5,
    "strength": "STRONG",
    "quality_score": 85.0,
    "confluence_count": 5
  },
  "entry": {
    "price": 42500.0,
    "description": "Price above EMA21 (42350.50) | RSI: 55.3",
    "trigger": "IMMEDIATE"
  },
  "stop_loss": {
    "price": 41200.0,
    "distance_pips": 1300.0,
    "distance_percent": 3.05,
    "method": "LEVEL",
    "invalidation_logic": "Price breaks below support at 41250.00"
  },
  "take_profit": {
    "tp1": {
      "price": 43800.0,
      "distance_pips": 1300.0,
      "ratio": 1.0,
      "position_percent": 50
    },
    "tp2": {
      "price": 45100.0,
      "distance_pips": 2600.0,
      "ratio": 2.0,
      "position_percent": 30
    },
    "tp3": {
      "price": 46400.0,
      "distance_pips": 3900.0,
      "ratio": 3.0,
      "position_percent": 20
    }
  },
  "risk_reward": {
    "ratio": 3.0,
    "risk_amount": 200.0,
    "profit_target": 600.0,
    "status": "EXCELLENT"
  },
  "position_sizing": {
    "units": 0.15,
    "lot_size": 0.0015,
    "position_value": 6375.0,
    "leverage_required": 0.64
  },
  "technical_details": {
    "indicators": {
      "RSI": {
        "value": 55.3,
        "interpretation": "Moderate (55.3)"
      },
      "MACD": {
        "value": 125.5,
        "signal": 98.2,
        "interpretation": "Bullish momentum"
      },
      "MA_crossover": {
        "EMA21": 42350.5,
        "SMA50": 42100.0,
        "SMA200": 41500.0,
        "trend": "UPTREND"
      },
      "ATR": {
        "value": 850.0,
        "volatility": "NORMAL"
      },
      "ADX": {
        "value": 32.5,
        "strength": "MODERATE",
        "direction": "BULLISH"
      },
      "Support": 41250.0,
      "Resistance": 44000.0,
      "Volume": "Above average"
    },
    "patterns": [
      {
        "name": "Bullish Engulfing",
        "type": "REVERSAL",
        "confidence": 100,
        "signal": "BUY"
      }
    ],
    "timeframe": "1H"
  },
  "execution_checklist": {
    "price_action_confirmed": true,
    "momentum_aligned": true,
    "volatility_acceptable": true,
    "trend_strength_ok": true,
    "risk_reward_positive": true,
    "risk_limits_ok": true,
    "all_ready": true
  },
  "recommendations": [
    "✓ Entry: BUY at current price 42500.00",
    "📊 Risk/Reward: 3.0:1 (EXCELLENT)",
    "📈 UPTREND - favorable conditions for trend following",
    "🎯 Strong patterns detected: Bullish Engulfing",
    "✅ All checks passed - This setup meets professional trading standards"
  ],
  "warnings": [],
  "quality_validation": {
    "passed": true,
    "quality_score": 85.0,
    "confluence_count": 5,
    "issues": [],
    "recommendation": "TRADE"
  },
  "risk_checks": {
    "daily_limit": {
      "allowed": true,
      "current_daily_loss": 0.0,
      "potential_loss": 200.0,
      "max_daily_loss": 500.0,
      "remaining_allowance": 500.0,
      "message": "Trade allowed"
    },
    "portfolio_limit": {
      "position_count_ok": true,
      "current_positions": 0,
      "max_positions": 5,
      "total_risk": 200.0,
      "total_risk_percent": 2.0,
      "max_drawdown_percent": 15.0,
      "within_limits": true,
      "all_checks_passed": true
    },
    "all_passed": true
  }
}
```

**Status Codes:**

- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid input (e.g., insufficient data)
- `500 Internal Server Error`: Server error during analysis

---

### 4. Get Analysis Summary

**GET** `/summary`

Get summary statistics of recent analyses.

**Response:**

```json
{
  "total_analyses": 15,
  "signal_distribution": {
    "BUY": 8,
    "SELL": 5,
    "HOLD": 2
  },
  "average_confidence": 75.3,
  "recent_analyses": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "symbol": "BTC/USD",
      "signal": "BUY",
      "confidence": 82.5
    }
  ]
}
```

---

### 5. List Technical Indicators

**GET** `/indicators/list`

Get list of all available technical indicators.

**Response:**

```json
{
  "total_indicators": 9,
  "indicators": {
    "RSI": {
      "name": "Relative Strength Index",
      "description": "Momentum oscillator measuring overbought/oversold conditions",
      "range": "0-100",
      "signals": "Overbought >70, Oversold <30"
    },
    "MACD": {
      "name": "Moving Average Convergence Divergence",
      "description": "Trend-following momentum indicator",
      "signals": "Crossovers, divergences"
    }
  }
}
```

---

### 6. WebSocket: Real-time Signals

**WebSocket** `/ws/signals`

Connect to receive real-time trading signals.

**Connection:**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/signals");

ws.onopen = () => {
  console.log("Connected to signal stream");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};

ws.onclose = () => {
  console.log("Connection closed");
};
```

**Messages Received:**

```json
{
  "type": "connection",
  "message": "Connected to AI Trading Agent signal stream",
  "timestamp": "2024-01-01T12:00:00"
}
```

```json
{
  "type": "new_analysis",
  "symbol": "BTC/USD",
  "signal": "BUY",
  "confidence": 82.5,
  "timestamp": "2024-01-01T12:01:00"
}
```

---

## Signal Types

- `BUY`: Long position recommendation
- `SELL`: Short position recommendation
- `HOLD`: No clear direction, wait for better setup

## Signal Strength

- `STRONG`: 80-100 quality score, 3+ confluences
- `MODERATE`: 60-80 quality score, 2+ confluences
- `WEAK`: 40-60 quality score, 1+ confluences

## Entry Triggers

- `IMMEDIATE`: Enter immediately (4+ confluences, 70+ quality)
- `WAIT_CONFIRMATION`: Wait for additional confirmation (2+ confluences)
- `PULLBACK`: Wait for price pullback before entry

## Risk/Reward Status

- `EXCELLENT`: R:R ratio ≥ 2.5
- `GOOD`: R:R ratio ≥ 2.0
- `ACCEPTABLE`: R:R ratio ≥ 1.5
- `REJECT`: R:R ratio < 1.5

## Stop Loss Methods

- `ATR`: Based on Average True Range (1.5x ATR)
- `LEVEL`: Based on support/resistance levels
- `PERCENTAGE`: Fixed percentage (2-3%)

---

## Error Responses

All errors return JSON in this format:

```json
{
  "error": "Error message",
  "detail": "Detailed information",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Common Errors:**

- `400 Bad Request`: Invalid input data
- `404 Not Found`: Endpoint doesn't exist
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

Currently no rate limiting implemented. For production, consider:

- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## Example Usage

### Python

```python
import requests

data = {
    "symbol": "BTC/USD",
    "timeframe": "1H",
    "ohlcv": {
        "open": [...],
        "high": [...],
        "low": [...],
        "close": [...],
        "volume": [...]
    }
}

response = requests.post(
    "http://localhost:8000/analyze",
    json=data
)

if response.status_code == 200:
    analysis = response.json()
    print(f"Signal: {analysis['signal']['type']}")
    print(f"Confidence: {analysis['signal']['confidence']}%")
```

### JavaScript

```javascript
fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        symbol: 'BTC/USD',
        timeframe: '1H',
        ohlcv: {
            open: [...],
            high: [...],
            low: [...],
            close: [...],
            volume: [...]
        }
    })
})
.then(response => response.json())
.then(data => {
    console.log('Signal:', data.signal.type);
    console.log('Confidence:', data.signal.confidence);
});
```

### cURL

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USD",
    "timeframe": "1H",
    "ohlcv": {
      "open": [42000, 42100],
      "high": [42200, 42300],
      "low": [41900, 42000],
      "close": [42100, 42200],
      "volume": [1000000, 1200000]
    }
  }'
```

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation where you can test endpoints directly.

---

## Support

For issues or questions, please refer to:

- Main README: [README.md](README.md)
- Setup Guide: [SETUP.md](SETUP.md)
- GitHub Issues: Create an issue for bug reports
