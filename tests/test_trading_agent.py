"""
Unit tests for Trading Agent
"""

import pytest
import numpy as np
from app.core.technical_analysis import TechnicalAnalysis
from app.core.chart_analyzer import ChartAnalyzer
from app.core.signal_generator import SignalGenerator
from app.core.risk_manager import RiskManager, StopLossMethod
from app.core.trading_agent import TradingAgent


@pytest.fixture
def sample_ohlcv():
    """Generate sample OHLCV data for testing"""
    length = 100
    base_price = 42000
    
    close = np.linspace(base_price, base_price + 1000, length) + np.random.randn(length) * 100
    open_prices = close + np.random.randn(length) * 50
    high = np.maximum(open_prices, close) + np.abs(np.random.randn(length) * 100)
    low = np.minimum(open_prices, close) - np.abs(np.random.randn(length) * 100)
    volume = np.random.randint(1000000, 5000000, length).astype(float)
    
    return {
        "open": open_prices,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume
    }


class TestTechnicalAnalysis:
    """Test technical analysis module"""
    
    def test_rsi_calculation(self, sample_ohlcv):
        """Test RSI calculation"""
        ta = TechnicalAnalysis()
        result = ta.calculate_rsi(sample_ohlcv["close"])
        
        assert result.value >= 0
        assert result.value <= 100
        assert result.interpretation is not None
        assert result.signal in ["BUY", "SELL", "NEUTRAL"]
    
    def test_macd_calculation(self, sample_ohlcv):
        """Test MACD calculation"""
        ta = TechnicalAnalysis()
        result = ta.calculate_macd(sample_ohlcv["close"])
        
        assert "macd" in result
        assert "signal" in result
        assert "histogram" in result
        assert result["signal_type"] in ["BUY", "SELL", "NEUTRAL"]
    
    def test_moving_averages(self, sample_ohlcv):
        """Test moving averages calculation"""
        ta = TechnicalAnalysis()
        result = ta.calculate_moving_averages(sample_ohlcv["close"])
        
        assert "ema21" in result
        assert "sma50" in result
        assert "sma200" in result
        assert result["trend"] is not None
    
    def test_atr_calculation(self, sample_ohlcv):
        """Test ATR calculation"""
        ta = TechnicalAnalysis()
        result = ta.calculate_atr(
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"]
        )
        
        assert result["atr"] > 0
        assert result["volatility"] in ["LOW", "NORMAL", "HIGH", "EXTREME"]


class TestChartAnalyzer:
    """Test chart analyzer module"""
    
    def test_support_resistance_detection(self, sample_ohlcv):
        """Test support/resistance detection"""
        ca = ChartAnalyzer()
        levels = ca.detect_support_resistance(
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"]
        )
        
        assert isinstance(levels, list)
        if levels:
            assert levels[0].level_type in ["SUPPORT", "RESISTANCE"]
            assert levels[0].strength > 0
    
    def test_trend_detection(self, sample_ohlcv):
        """Test trend channel detection"""
        ca = ChartAnalyzer()
        result = ca.detect_trend_channels(
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"]
        )
        
        assert result["trend_type"] in ["UPTREND", "DOWNTREND", "SIDEWAYS"]
        assert "slope" in result


class TestSignalGenerator:
    """Test signal generator module"""
    
    def test_signal_generation(self, sample_ohlcv):
        """Test signal generation"""
        ta = TechnicalAnalysis()
        ca = ChartAnalyzer()
        sg = SignalGenerator()
        
        technical_data = ta.full_analysis(
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"],
            sample_ohlcv["volume"]
        )
        
        chart_data = ca.full_chart_analysis(
            None,
            sample_ohlcv["open"],
            sample_ohlcv["high"],
            sample_ohlcv["low"],
            sample_ohlcv["close"]
        )
        
        signal = sg.generate_signal(
            technical_data,
            chart_data,
            sample_ohlcv["close"][-1]
        )
        
        assert signal.signal_type in ["BUY", "SELL", "HOLD"]
        assert 0 <= signal.confidence <= 100
        assert signal.strength in ["WEAK", "MODERATE", "STRONG"]


class TestRiskManager:
    """Test risk manager module"""
    
    def test_stop_loss_calculation(self):
        """Test stop loss calculation"""
        rm = RiskManager(capital=10000)
        
        sl = rm.calculate_stop_loss(
            entry_price=42000,
            signal_type="BUY",
            atr=500,
            method=StopLossMethod.ATR_BASED
        )
        
        assert sl.price < 42000  # SL should be below entry for BUY
        assert sl.distance_pips > 0
        assert sl.method == "ATR"
    
    def test_take_profit_calculation(self):
        """Test take profit calculation"""
        rm = RiskManager(capital=10000)
        
        sl = rm.calculate_stop_loss(
            entry_price=42000,
            signal_type="BUY",
            atr=500
        )
        
        tp = rm.calculate_take_profits(
            entry_price=42000,
            stop_loss=sl,
            signal_type="BUY"
        )
        
        assert "tp1" in tp
        assert "tp2" in tp
        assert "tp3" in tp
        assert tp["tp1"].price > 42000  # TP should be above entry for BUY
        assert tp["tp2"].ratio == 2.0
        assert tp["tp3"].ratio >= 2.0
    
    def test_position_sizing(self):
        """Test position sizing calculation"""
        rm = RiskManager(capital=10000, max_risk_percent=2.0)
        
        sl = rm.calculate_stop_loss(
            entry_price=42000,
            signal_type="BUY",
            atr=500
        )
        
        position = rm.calculate_position_size(
            entry_price=42000,
            stop_loss=sl
        )
        
        assert position.risk_amount == 200  # 2% of 10000
        assert position.units > 0


class TestTradingAgent:
    """Test main trading agent"""
    
    def test_full_analysis(self, sample_ohlcv):
        """Test complete trading analysis"""
        agent = TradingAgent(capital=10000)
        
        analysis = agent.analyze(
            symbol="BTC/USD",
            timeframe="1H",
            open_prices=sample_ohlcv["open"],
            high=sample_ohlcv["high"],
            low=sample_ohlcv["low"],
            close=sample_ohlcv["close"],
            volume=sample_ohlcv["volume"]
        )
        
        assert "metadata" in analysis
        assert "signal" in analysis
        assert "entry" in analysis
        assert "technical_details" in analysis
        assert "recommendations" in analysis
        
        assert analysis["signal"]["type"] in ["BUY", "SELL", "HOLD"]
        assert 0 <= analysis["signal"]["confidence"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
