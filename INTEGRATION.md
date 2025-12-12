# Frontend-Backend Integration Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│               Frontend Dashboard                        │
│  (HTML/CSS/JS - c:\frontend\)                           │
│                                                         │
│  ├─ index.html      (Main dashboard)                   │
│  ├─ js/             (JavaScript logic)                 │
│  │  ├─ api.js       (API client + WebSocket)           │
│  │  ├─ dashboard.js (UI management)                    │
│  │  └─ utils.js     (Helper functions)                 │
│  └─ css/            (Styling)                          │
└────────────┬────────────────────────────────────────────┘
             │
      HTTP + WebSocket
             │
┌────────────▼────────────────────────────────────────────┐
│            FastAPI Backend Server                       │
│  (Python - c:\app\main.py)                              │
│                                                         │
│  API Endpoints:                                         │
│  ├─ GET  /               → Serve dashboard             │
│  ├─ GET  /health         → Health check                │
│  ├─ POST /analyze        → Analyze chart & signals     │
│  ├─ GET  /market/data    → Market data                 │
│  ├─ GET  /market/symbols → Available symbols           │
│  ├─ GET  /signals/recent → Recent signals history      │
│  ├─ GET  /signals/statistics → Performance stats       │
│  └─ WS   /ws/signals     → Real-time signal stream     │
└────────────┬────────────────────────────────────────────┘
             │
      Internal Modules
             │
┌────────────▼────────────────────────────────────────────┐
│        Trading Agent Core Modules                       │
│                                                         │
│  ├─ TradingAgent         → Main orchestrator            │
│  ├─ TechnicalAnalysis    → Indicators (RSI, MACD...)   │
│  ├─ ChartAnalyzer        → Pattern recognition         │
│  ├─ SignalGenerator      → Trading signals             │
│  ├─ LLMProvider          → g4f integration              │
│  └─ RiskManager          → Risk calculations           │
└─────────────────────────────────────────────────────────┘
```

## Frontend Components

### 1. API Client (js/api.js)

**Class: TradingAPI**

- `analyzeChart(data)` - Send chart for analysis
- `getMarketData(symbol, limit)` - Fetch market data
- `getAvailableSymbols()` - Get symbol list
- `getRecentSignals(limit)` - Get recent signals
- `getSignalsStatistics()` - Get performance stats
- `healthCheck()` - Check API availability

**Class: SignalWebSocket**

- `connect()` - Connect to WebSocket
- `disconnect()` - Close connection
- `send(data)` - Send message to server
- `on(event, callback)` - Listen for events
- `isConnected()` - Check connection status

### 2. Dashboard Manager (js/dashboard.js)

**Main Class: Dashboard**

- UI initialization and event handling
- Chart upload and preview
- Form validation
- Results display management
- Theme toggling
- WebSocket integration

**Key Methods:**

- `analyzeChart()` - Send chart to backend
- `displayResults(analysis)` - Show results on dashboard
- `loadRecentSignals()` - Load signal history
- `setupWebSocket()` - Initialize real-time updates
- `loadSignalStatistics()` - Load performance metrics

### 3. Utilities (js/utils.js)

Helper functions:

- `showToast()` - Display notifications
- `formatCurrency()`, `formatNumber()` - Formatting
- `formatNumberWithCommas()` - Number formatting
- `debounce()`, `debounceAsync()` - Rate limiting
- `throttle()` - Throttle functions
- `retryAsync()` - Retry mechanism
- `isValidEmail()`, `isValidNumber()` - Validation

## Backend Endpoints

### Analysis Endpoint

```
POST /analyze
Content-Type: application/json

Request:
{
  "symbol": "BTC/USD",
  "timeframe": "1H",
  "capital": 10000,
  "risk_percent": 2.0,
  "ohlcv": {
    "open": [40000, 40100, ...],
    "high": [40200, 40300, ...],
    "low": [39900, 40000, ...],
    "close": [40100, 40200, ...],
    "volume": [1000, 1100, ...]
  },
  "image_base64": "..." (optional)
}

Response:
{
  "metadata": {
    "symbol": "BTC/USD",
    "timeframe": "1H",
    "timestamp": "2025-12-12T10:30:00",
    "current_price": 42500
  },
  "signal": {
    "type": "BUY",
    "confidence": 85,
    "strength": 8.5,
    "quality_score": 87,
    "confluence_count": 5
  },
  "entry": {
    "price": 42500,
    "description": "Break above resistance",
    "trigger": "Close above 42400"
  },
  "stop_loss": {...},
  "take_profit": {...},
  "indicators": {...},
  "technical_data": {...},
  "chart_data": {...},
  "llm_analysis": {...},
  "risk_reward": {...},
  "position_size": "0.25"
}
```

### Market Data Endpoint

```
GET /market/data?symbol=BTC/USD&limit=100

Response:
{
  "symbol": "BTC/USD",
  "current_price": 42500.00,
  "24h_change": 2.5,
  "24h_high": 43200.00,
  "24h_low": 41500.00,
  "volume": 28500.75,
  "timestamp": "2025-12-12T10:30:00"
}
```

### Recent Signals Endpoint

```
GET /signals/recent?limit=10

Response:
[
  {
    "symbol": "BTC/USD",
    "signal": "BUY",
    "confidence": 85,
    "timestamp": "2025-12-12T10:30:00",
    "entry_price": 42500
  },
  ...
]
```

### WebSocket Connection

```
WS ws://localhost:8000/ws/signals

Events:
- connection: Initial connection
- new_analysis: New trading signal
- market_update: Market data update
- error: Error occurred
- disconnected: Connection closed
```

## Integration Flow

### 1. Page Load

1. Browser loads `http://localhost:8000/`
2. FastAPI serves `frontend/index.html`
3. HTML loads JS files (utils.js → api.js → dashboard.js)
4. Dashboard initializes and connects WebSocket
5. Frontend checks API health

### 2. User Analysis

1. User uploads chart image
2. Dashboard validates form inputs
3. Calls `api.analyzeChart()` with form data
4. FastAPI receives request at `/analyze`
5. Trading agent processes chart:
   - Technical analysis
   - Chart pattern recognition
   - LLM analysis via g4f
   - Signal generation
   - Risk calculations
6. Response returned to frontend
7. Results displayed on dashboard
8. WebSocket broadcasts signal to all connected clients

### 3. Real-time Updates

1. WebSocket maintains persistent connection
2. When new analysis completes, server broadcasts
3. All connected clients receive signal update
4. Dashboard updates in real-time
5. Toast notification shown to user

## Configuration

### Frontend (config.js)

```javascript
const API_CONFIGURATION = {
  development: {
    baseUrl: "http://localhost:8000",
    wsUrl: "ws://localhost:8000",
  },
  production: {
    baseUrl: "https://api.modtrade.com",
    wsUrl: "wss://api.modtrade.com",
  },
};
```

### Backend (app/config.py)

```python
use_g4f: bool = True
g4f_provider: str = "gpt-4-free"
gpt_model: str = "gpt-4"
default_capital: float = 10000
max_risk_percent: float = 2.0
max_daily_loss_percent: float = 5.0
```

## Running the Integrated System

### Option 1: Direct Python

```bash
python run_integrated.py
```

### Option 2: With Uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Docker Compose

```bash
docker-compose -f docker-compose-prod.yml up
```

### Option 4: Quick Batch Script

```bash
quick_start.bat
```

## Testing the Integration

### 1. Test Health Check

```bash
curl http://localhost:8000/health
```

### 2. Test Dashboard Load

```bash
Open http://localhost:8000 in browser
```

### 3. Test API Docs

```bash
Open http://localhost:8000/docs in browser
```

### 4. Test WebSocket

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/signals");
ws.onopen = () => console.log("Connected");
ws.onmessage = (e) => console.log("Message:", e.data);
```

### 5. Test Analysis

```javascript
const api = new TradingAPI();
const result = await api.analyzeChart({
  symbol: "BTC/USD",
  timeframe: "1H",
  ohlcv: {...}
});
```

## Features Implemented

✅ **Frontend Dashboard**

- Professional UI/UX design
- Chart upload and preview
- Real-time analysis display
- WebSocket integration
- Theme switching (light/dark)
- Responsive design

✅ **Backend API**

- REST endpoints for all functions
- WebSocket for real-time signals
- Error handling and validation
- Static file serving
- CORS enabled
- Health checks

✅ **Trading Analysis**

- Technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Chart pattern recognition
- LLM-powered analysis via g4f
- Risk/Reward calculations
- Position sizing
- Signal confidence scoring

✅ **Real-time Updates**

- WebSocket signal streaming
- Broadcast to all connected clients
- Automatic reconnection
- Event-based architecture

✅ **Database**

- In-memory analysis history
- Signal statistics
- Recent signals tracking
- Performance metrics

## Deployment Checklist

- [ ] Update API_CONFIGURATION for production domain
- [ ] Set CORS origins appropriately
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Set up authentication if needed
- [ ] Test with production data
- [ ] Configure environment variables
- [ ] Set up backup strategy
- [ ] Create deployment documentation

## Performance Optimization

1. **Frontend:**

   - Lazy load resources
   - Debounce WebSocket messages
   - Cache API responses
   - Minimize bundle size

2. **Backend:**

   - Implement caching layer
   - Optimize database queries
   - Use connection pooling
   - Set up CDN for static files

3. **WebSocket:**
   - Message compression
   - Connection pooling
   - Graceful degradation
   - Reconnection strategy

## Troubleshooting

### WebSocket Connection Failed

1. Check if port 8000 is open
2. Verify server is running
3. Check CORS settings
4. Look at browser console for errors

### API Not Responding

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check API endpoint URL matches config
3. Check network tab in browser dev tools
4. Look at FastAPI logs

### Chart Analysis Not Working

1. Ensure image is valid format (PNG, JPG)
2. Check file size (max 10MB)
3. Verify OHLCV data is present
4. Check backend logs for errors

### Real-time Updates Not Showing

1. Check WebSocket connection status
2. Verify connection manager is working
3. Check browser console for errors
4. Test WebSocket directly

## Additional Resources

- FastAPI Docs: http://localhost:8000/docs
- API Schema: http://localhost:8000/openapi.json
- Frontend Code: `/frontend` directory
- Backend Code: `/app` directory
- Configuration: `app/config.py`
- Logs: `/logs` directory

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review browser console and server logs
3. Test individual components
4. Consult FastAPI documentation
5. Check g4f documentation for LLM issues

---

**Last Updated:** December 12, 2025
**Version:** 1.0.0
**Status:** Production Ready ✅
