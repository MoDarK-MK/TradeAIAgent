"""
Trading Agent - Main Orchestrator
Coordinates all modules to generate complete trading analysis
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

from app.core.technical_analysis import TechnicalAnalysis
from app.core.chart_analyzer import ChartAnalyzer
from app.core.signal_generator import SignalGenerator, TradingSignal
from app.core.risk_manager import RiskManager


class TradingAgent:
    """
    Enterprise-Grade Trading Intelligence Engine
    Orchestrates technical analysis, chart analysis, signal generation, and risk management
    """

    def __init__(
        self,
        capital: float = 10000,
        max_risk_percent: float = 2.0,
        max_daily_loss_percent: float = 5.0
    ):
        self.technical_analyzer = TechnicalAnalysis()
        self.chart_analyzer = ChartAnalyzer()
        self.signal_generator = SignalGenerator()
        self.risk_manager = RiskManager(
            capital=capital,
            max_risk_percent=max_risk_percent,
            max_daily_loss_percent=max_daily_loss_percent
        )
        
        self.capital = capital
        self.analysis_history = []

    def analyze(
        self,
        symbol: str,
        timeframe: str,
        open_prices: np.ndarray,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        volume: np.ndarray,
        image_base64: Optional[str] = None
    ) -> Dict:
        """
        Perform complete trading analysis
        
        Args:
            symbol: Trading symbol (e.g., "BTC/USD", "EUR/USD")
            timeframe: Timeframe (e.g., "1H", "4H", "Daily")
            open_prices, high, low, close, volume: OHLCV data arrays
            image_base64: Optional base64 encoded chart image
        
        Returns:
            Complete analysis dictionary with all recommendations
        """
        current_price = close[-1]
        
        technical_data = self.technical_analyzer.full_analysis(
            open_prices=open_prices,
            high=high,
            low=low,
            close=close,
            volume=volume
        )

        chart_data = self.chart_analyzer.full_chart_analysis(
            image_base64=image_base64,
            open_prices=open_prices,
            high=high,
            low=low,
            close=close
        )

        signal = self.signal_generator.generate_signal(
            technical_data=technical_data,
            chart_data=chart_data,
            current_price=current_price
        )

        quality_validation = self.signal_generator.validate_signal_quality(signal)

        risk_data = None
        if quality_validation["passed"]:
            atr_value = technical_data["atr"]["atr"]
            
            support_level = None
            resistance_level = None
            if chart_data.get("nearest_support"):
                support_level = chart_data["nearest_support"]["price"]
            if chart_data.get("nearest_resistance"):
                resistance_level = chart_data["nearest_resistance"]["price"]

            risk_data = self.risk_manager.full_risk_analysis(
                entry_price=current_price,
                signal_type=signal.signal_type,
                atr=atr_value,
                support_level=support_level,
                resistance_level=resistance_level
            )

        recommendations = self._generate_recommendations(
            signal=signal,
            technical_data=technical_data,
            chart_data=chart_data,
            risk_data=risk_data,
            quality_validation=quality_validation
        )
        
        llm_analysis = self.signal_generator.generate_llm_analysis(
            technical_data=technical_data,
            chart_data=chart_data,
            current_price=current_price,
            symbol=symbol,
            timeframe=timeframe
        )

        execution_checklist = self._create_execution_checklist(
            signal=signal,
            technical_data=technical_data,
            risk_data=risk_data
        )

        analysis = {
            "metadata": {
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": datetime.utcnow().isoformat(),
                "current_price": round(current_price, 2)
            },
            "signal": {
                "type": signal.signal_type,
                "confidence": signal.confidence,
                "strength": signal.strength,
                "quality_score": signal.quality_score,
                "confluence_count": signal.confluence_count
            },
            "entry": {
                "price": signal.entry_price,
                "description": signal.entry_description,
                "trigger": signal.entry_trigger
            },
            "stop_loss": risk_data["stop_loss"] if risk_data else None,
            "take_profit": risk_data["take_profit"] if risk_data else None,
            "risk_reward": risk_data["risk_reward"] if risk_data else None,
            "position_sizing": risk_data["position_sizing"] if risk_data else None,
            "technical_details": {
                "indicators": {
                    "RSI": {
                        "value": technical_data["rsi"]["value"],
                        "interpretation": technical_data["rsi"]["interpretation"]
                    },
                    "MACD": {
                        "value": technical_data["macd"]["macd"],
                        "signal": technical_data["macd"]["signal"],
                        "interpretation": technical_data["macd"]["interpretation"]
                    },
                    "MA_crossover": {
                        "EMA21": technical_data["moving_averages"]["ema21"],
                        "SMA50": technical_data["moving_averages"]["sma50"],
                        "SMA200": technical_data["moving_averages"]["sma200"],
                        "trend": technical_data["moving_averages"]["trend"]
                    },
                    "ATR": {
                        "value": technical_data["atr"]["atr"],
                        "volatility": technical_data["atr"]["volatility"]
                    },
                    "ADX": {
                        "value": technical_data["adx"]["adx"],
                        "strength": technical_data["adx"]["strength"],
                        "direction": technical_data["adx"]["direction"]
                    },
                    "Bollinger_Bands": {
                        "upper": technical_data["bollinger_bands"]["upper"],
                        "middle": technical_data["bollinger_bands"]["middle"],
                        "lower": technical_data["bollinger_bands"]["lower"],
                        "interpretation": technical_data["bollinger_bands"]["interpretation"]
                    },
                    "Stochastic": {
                        "k": technical_data["stochastic"]["k"],
                        "d": technical_data["stochastic"]["d"],
                        "interpretation": technical_data["stochastic"]["interpretation"]
                    },
                    "Support": chart_data.get("nearest_support", {}).get("price"),
                    "Resistance": chart_data.get("nearest_resistance", {}).get("price"),
                    "Volume": technical_data["volume"]["interpretation"]
                },
                "patterns": chart_data.get("patterns", []),
                "fibonacci": technical_data["fibonacci"],
                "timeframe": timeframe
            },
            "execution_checklist": execution_checklist,
            "recommendations": recommendations,
            "llm_analysis": llm_analysis,
            "warnings": signal.warnings,
            "quality_validation": quality_validation,
            "risk_checks": risk_data["risk_checks"] if risk_data else None
        }

        self.analysis_history.append({
            "timestamp": analysis["metadata"]["timestamp"],
            "symbol": symbol,
            "signal": signal.signal_type,
            "confidence": signal.confidence
        })

        return analysis

    def _generate_recommendations(
        self,
        signal: TradingSignal,
        technical_data: Dict,
        chart_data: Dict,
        risk_data: Optional[Dict],
        quality_validation: Dict
    ) -> List[str]:
        """
        Generate actionable recommendations
        
        Returns:
            List of recommendation strings
        """
        recommendations = []

        if signal.entry_trigger == "IMMEDIATE":
            recommendations.append(
                f"✓ Entry: {signal.signal_type} at current price {signal.entry_price:.2f}"
            )
        elif signal.entry_trigger == "WAIT_CONFIRMATION":
            recommendations.append(
                f"⏳ Entry: Wait for confirmation before {signal.signal_type}"
            )
        else:
            recommendations.append(
                f"⚠ Entry: Wait for pullback before entering {signal.signal_type}"
            )

        if risk_data:
            rr_ratio = risk_data["risk_reward"]["ratio"]
            rr_status = risk_data["risk_reward"]["status"]
            recommendations.append(
                f"📊 Risk/Reward: {rr_ratio}:1 ({rr_status})"
            )

        volatility = technical_data["atr"]["volatility"]
        if volatility in ["HIGH", "EXTREME"]:
            recommendations.append(
                f"⚡ {volatility} volatility detected - consider reducing position size by 50%"
            )

        trend = technical_data["moving_averages"]["trend"]
        if "STRONG" in trend:
            recommendations.append(
                f"📈 {trend} - favorable conditions for trend following"
            )
        elif trend == "SIDEWAYS":
            recommendations.append(
                "↔ Sideways market - wait for breakout or reduce position size"
            )

        patterns = chart_data.get("patterns", [])
        if patterns:
            strong_patterns = [p for p in patterns if p.get("confidence", 0) >= 80]
            if strong_patterns:
                pattern_names = ", ".join([p["name"] for p in strong_patterns[:2]])
                recommendations.append(
                    f"🎯 Strong patterns detected: {pattern_names}"
                )

        if not quality_validation["passed"]:
            recommendations.append(
                "⛔ Signal quality below threshold - recommend SKIP this trade"
            )
            if quality_validation["issues"]:
                recommendations.append(
                    f"Issues: {', '.join(quality_validation['issues'][:2])}"
                )

        if quality_validation["passed"] and risk_data:
            if risk_data["risk_checks"]["all_passed"]:
                recommendations.append(
                    "✅ All checks passed - This setup meets professional trading standards"
                )
            else:
                recommendations.append(
                    "⚠ Risk limits exceeded - Skip or reduce position size"
                )

        return recommendations

    def _create_execution_checklist(
        self,
        signal: TradingSignal,
        technical_data: Dict,
        risk_data: Optional[Dict]
    ) -> Dict:
        """
        Create execution checklist
        
        Returns:
            Dict with boolean checks
        """
        checklist = {
            "price_action_confirmed": signal.confluence_count >= 2,
            "momentum_aligned": (
                technical_data["rsi"]["signal"] != "NEUTRAL" or
                technical_data["macd"]["signal_type"] != "NEUTRAL"
            ),
            "volatility_acceptable": technical_data["atr"]["volatility"] != "EXTREME",
            "trend_strength_ok": technical_data["adx"]["strength"] != "WEAK",
            "risk_reward_positive": False,
            "all_ready": False
        }

        if risk_data:
            checklist["risk_reward_positive"] = risk_data["risk_reward"]["ratio"] >= 1.5
            checklist["risk_limits_ok"] = risk_data["risk_checks"]["all_passed"]
        else:
            checklist["risk_limits_ok"] = False

        checklist["all_ready"] = all([
            checklist["price_action_confirmed"],
            checklist["momentum_aligned"],
            checklist["volatility_acceptable"],
            checklist.get("risk_reward_positive", False),
            checklist.get("risk_limits_ok", False)
        ])

        return checklist

    def analyze_from_dict(self, data: Dict) -> Dict:
        """
        Convenience method to analyze from dictionary input
        
        Args:
            data: Dict with keys: symbol, timeframe, ohlcv, image_base64 (optional)
        
        Returns:
            Complete analysis
        """
        ohlcv = data.get("ohlcv", {})
        
        return self.analyze(
            symbol=data.get("symbol", "UNKNOWN"),
            timeframe=data.get("timeframe", "1H"),
            open_prices=np.array(ohlcv.get("open", [])),
            high=np.array(ohlcv.get("high", [])),
            low=np.array(ohlcv.get("low", [])),
            close=np.array(ohlcv.get("close", [])),
            volume=np.array(ohlcv.get("volume", [])),
            image_base64=data.get("image_base64")
        )

    def get_analysis_summary(self) -> Dict:
        """
        Get summary of recent analysis history
        
        Returns:
            Summary statistics
        """
        if not self.analysis_history:
            return {"message": "No analysis history available"}

        total_analyses = len(self.analysis_history)
        buy_signals = sum(1 for a in self.analysis_history if a["signal"] == "BUY")
        sell_signals = sum(1 for a in self.analysis_history if a["signal"] == "SELL")
        hold_signals = sum(1 for a in self.analysis_history if a["signal"] == "HOLD")
        
        avg_confidence = np.mean([a["confidence"] for a in self.analysis_history])

        return {
            "total_analyses": total_analyses,
            "signal_distribution": {
                "BUY": buy_signals,
                "SELL": sell_signals,
                "HOLD": hold_signals
            },
            "average_confidence": round(avg_confidence, 2),
            "recent_analyses": self.analysis_history[-5:]
        }
