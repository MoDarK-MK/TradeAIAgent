"""
Pydantic Schemas for API requests/responses
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class OHLCVData(BaseModel):
    """OHLCV price data"""
    open: List[float] = Field(..., description="Opening prices")
    high: List[float] = Field(..., description="High prices")
    low: List[float] = Field(..., description="Low prices")
    close: List[float] = Field(..., description="Closing prices")
    volume: List[float] = Field(..., description="Volume data")


class AnalysisRequest(BaseModel):
    """Request for trading analysis"""
    symbol: str = Field(..., example="BTC/USD", description="Trading symbol")
    timeframe: str = Field(..., example="1H", description="Timeframe (1H, 4H, Daily)")
    ohlcv: OHLCVData = Field(..., description="OHLCV price data")
    image_base64: Optional[str] = Field(None, description="Base64 encoded chart image")
    capital: Optional[float] = Field(10000, description="Trading capital")
    risk_percent: Optional[float] = Field(2.0, description="Risk percentage per trade")


class SignalResponse(BaseModel):
    """Trading signal information"""
    type: str = Field(..., example="BUY", description="Signal type")
    confidence: float = Field(..., example=82.5, description="Confidence score 0-100")
    strength: str = Field(..., example="STRONG", description="Signal strength")
    quality_score: float = Field(..., example=85.0, description="Quality score 0-100")
    confluence_count: int = Field(..., example=5, description="Number of confluences")


class EntryResponse(BaseModel):
    """Entry information"""
    price: float = Field(..., example=42500.0, description="Entry price")
    description: str = Field(..., description="Entry description")
    trigger: str = Field(..., example="IMMEDIATE", description="Entry trigger type")


class StopLossResponse(BaseModel):
    """Stop loss information"""
    price: float = Field(..., example=41200.0, description="Stop loss price")
    distance_pips: float = Field(..., example=1300.0, description="Distance in pips")
    distance_percent: float = Field(..., example=3.05, description="Distance in percent")
    method: str = Field(..., example="LEVEL", description="Calculation method")
    invalidation_logic: str = Field(..., description="Invalidation logic")


class TakeProfitLevel(BaseModel):
    """Individual take profit level"""
    price: float = Field(..., example=43800.0)
    distance_pips: float = Field(..., example=1300.0)
    ratio: float = Field(..., example=1.0, description="Risk:Reward ratio")
    position_percent: int = Field(..., example=50, description="% of position to close")


class TakeProfitResponse(BaseModel):
    """Take profit targets"""
    tp1: TakeProfitLevel
    tp2: TakeProfitLevel
    tp3: TakeProfitLevel


class RiskRewardResponse(BaseModel):
    """Risk/Reward analysis"""
    ratio: float = Field(..., example=3.0, description="Risk:Reward ratio")
    risk_amount: float = Field(..., example=200.0, description="Risk amount in currency")
    profit_target: float = Field(..., example=600.0, description="Profit target")
    status: str = Field(..., example="EXCELLENT", description="Status classification")


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    metadata: Dict[str, Any] = Field(..., description="Analysis metadata")
    signal: SignalResponse
    entry: EntryResponse
    stop_loss: Optional[StopLossResponse]
    take_profit: Optional[TakeProfitResponse]
    risk_reward: Optional[RiskRewardResponse]
    technical_details: Dict[str, Any] = Field(..., description="Technical indicator details")
    execution_checklist: Dict[str, bool] = Field(..., description="Execution checklist")
    recommendations: List[str] = Field(..., description="Trading recommendations")
    warnings: List[str] = Field(default=[], description="Warnings")
    quality_validation: Dict[str, Any] = Field(..., description="Quality validation results")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., example="healthy")
    version: str = Field(..., example="1.0.0")
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
