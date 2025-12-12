"""
FastAPI Main Application
Provides REST API and WebSocket endpoints for trading analysis
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
import numpy as np
import json

from app.config import settings
from app.core.trading_agent import TradingAgent
from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    HealthResponse,
    ErrorResponse
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise-Grade Trading Intelligence Engine",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trading_agent = TradingAgent(
    capital=settings.default_capital,
    max_risk_percent=settings.max_risk_percent,
    max_daily_loss_percent=settings.max_daily_loss_percent
)

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_trading_signal(request: AnalysisRequest):
    """
    Analyze trading chart and generate signals
    
    This endpoint performs comprehensive analysis including:
    - Technical indicators (RSI, MACD, Bollinger Bands, etc.)
    - Chart pattern recognition
    - Support/Resistance levels
    - Signal generation with confidence scoring
    - Risk management (SL/TP calculation)
    - Position sizing recommendations
    
    Args:
        request: AnalysisRequest with symbol, timeframe, OHLCV data, optional chart image
    
    Returns:
        AnalysisResponse with complete trading analysis
    
    Raises:
        HTTPException: If analysis fails
    """
    try:
        if not request.ohlcv.close:
            raise HTTPException(status_code=400, detail="OHLCV data is required")
        
        if len(request.ohlcv.close) < 50:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data. Minimum 50 candles required for accurate analysis"
            )
        
        if request.capital:
            trading_agent.risk_manager.capital = request.capital
            trading_agent.capital = request.capital
        
        analysis = trading_agent.analyze(
            symbol=request.symbol,
            timeframe=request.timeframe,
            open_prices=np.array(request.ohlcv.open),
            high=np.array(request.ohlcv.high),
            low=np.array(request.ohlcv.low),
            close=np.array(request.ohlcv.close),
            volume=np.array(request.ohlcv.volume),
            image_base64=request.image_base64
        )
        
        await manager.broadcast({
            "type": "new_analysis",
            "symbol": request.symbol,
            "signal": analysis["signal"]["type"],
            "confidence": analysis["signal"]["confidence"],
            "timestamp": analysis["metadata"]["timestamp"]
        })
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/summary", response_model=dict)
async def get_analysis_summary():
    """
    Get summary of recent analysis history
    
    Returns:
        Summary statistics of recent analyses
    """
    try:
        summary = trading_agent.get_analysis_summary()
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get summary: {str(e)}"
        )


@app.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket):
    """
    WebSocket endpoint for real-time signal streaming
    
    Connect to this endpoint to receive real-time trading signals as they are generated.
    
    Example client code (JavaScript):
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/ws/signals');
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('New signal:', data);
    };
    ```
    """
    await manager.connect(websocket)
    try:
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to AI Trading Agent signal stream",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        while True:
            data = await websocket.receive_text()
            
            await websocket.send_json({
                "type": "echo",
                "message": f"Received: {data}",
                "timestamp": datetime.utcnow().isoformat()
            })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.post("/backtest", response_model=dict)
async def backtest_strategy(request: dict):
    """
    Backtest a trading strategy (placeholder for future implementation)
    
    Args:
        request: Backtest parameters
    
    Returns:
        Backtest results
    """
    return {
        "message": "Backtesting feature coming soon",
        "status": "not_implemented"
    }


@app.get("/indicators/list", response_model=dict)
async def list_indicators():
    """
    List all available technical indicators
    
    Returns:
        Dict of available indicators with descriptions
    """
    indicators = {
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
        },
        "Bollinger Bands": {
            "name": "Bollinger Bands",
            "description": "Volatility indicator with upper/lower bands",
            "signals": "Band touches, squeezes"
        },
        "Moving Averages": {
            "name": "Moving Averages (EMA21, SMA50, SMA200)",
            "description": "Trend identification and support/resistance",
            "signals": "Crossovers, price position"
        },
        "ATR": {
            "name": "Average True Range",
            "description": "Volatility measurement",
            "usage": "Stop loss placement, position sizing"
        },
        "ADX": {
            "name": "Average Directional Index",
            "description": "Trend strength indicator",
            "range": "0-100",
            "signals": ">25 strong trend, <20 weak trend"
        },
        "Stochastic": {
            "name": "Stochastic Oscillator",
            "description": "Momentum indicator for range-bound markets",
            "range": "0-100",
            "signals": "Overbought >80, Oversold <20"
        },
        "Fibonacci": {
            "name": "Fibonacci Retracement",
            "description": "Support/resistance levels based on Fibonacci ratios",
            "levels": "23.6%, 38.2%, 50%, 61.8%, 78.6%"
        },
        "Volume": {
            "name": "Volume Analysis",
            "description": "Confirmation of price movements",
            "signals": "Above/below average confirmation"
        }
    }
    
    return {
        "total_indicators": len(indicators),
        "indicators": indicators
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
