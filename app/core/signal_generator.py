"""
Signal Generator
Generates trading signals with confluence checking and quality scoring
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from app.core.llm_provider import llm_provider


class SignalType(Enum):
    """Trading signal types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    WAIT = "WAIT"


class SignalStrength(Enum):
    """Signal strength classification"""
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"


class TriggerType(Enum):
    """Entry trigger types"""
    IMMEDIATE = "IMMEDIATE"
    WAIT_CONFIRMATION = "WAIT_CONFIRMATION"
    PULLBACK = "PULLBACK"


@dataclass
class TradingSignal:
    """Complete trading signal data"""
    signal_type: str
    confidence: float  # 0-100
    strength: str
    quality_score: float  # 0-100
    confluence_count: int
    entry_price: float
    entry_description: str
    entry_trigger: str
    reasons: List[str]
    warnings: List[str]


class SignalGenerator:
    """
    Generates high-quality trading signals with multiple confluence checks
    """

    def __init__(self):
        self.min_confluence_for_trade = 2
        self.min_quality_score = 50

    def generate_signal(
        self,
        technical_data: Dict,
        chart_data: Dict,
        current_price: float
    ) -> TradingSignal:
        """
        Generate trading signal from technical and chart analysis
        
        Args:
            technical_data: Output from TechnicalAnalysis.full_analysis()
            chart_data: Output from ChartAnalyzer.full_chart_analysis()
            current_price: Current market price
        
        Returns:
            TradingSignal with complete information
        """
        bullish_signals = 0
        bearish_signals = 0
        confluences = []
        warnings = []

        ma_data = technical_data.get("moving_averages", {})
        trend = ma_data.get("trend", "SIDEWAYS")
        ma_signal = ma_data.get("signal", "NEUTRAL")

        if "UPTREND" in trend:
            bullish_signals += 2
            confluences.append(f"Trend: {trend}")
        elif "DOWNTREND" in trend:
            bearish_signals += 2
            confluences.append(f"Trend: {trend}")
        else:
            warnings.append("Market in sideways consolidation")

        if ma_data.get("crossover"):
            if "Golden" in ma_data["crossover"]:
                bullish_signals += 1
                confluences.append(ma_data["crossover"])
            elif "Death" in ma_data["crossover"]:
                bearish_signals += 1
                confluences.append(ma_data["crossover"])

        rsi_data = technical_data.get("rsi", {})
        rsi_value = rsi_data.get("value", 50)
        rsi_signal = rsi_data.get("signal", "NEUTRAL")

        if rsi_signal == "BUY":
            bullish_signals += 1
            confluences.append(f"RSI oversold ({rsi_value:.1f})")
        elif rsi_signal == "SELL":
            bearish_signals += 1
            confluences.append(f"RSI overbought ({rsi_value:.1f})")
        elif 40 <= rsi_value <= 60:
            confluences.append(f"RSI neutral ({rsi_value:.1f})")

        macd_data = technical_data.get("macd", {})
        macd_signal = macd_data.get("signal_type", "NEUTRAL")

        if macd_signal == "BUY":
            bullish_signals += 1
            confluences.append(f"MACD: {macd_data.get('interpretation', 'Bullish')}")
        elif macd_signal == "SELL":
            bearish_signals += 1
            confluences.append(f"MACD: {macd_data.get('interpretation', 'Bearish')}")

        bb_data = technical_data.get("bollinger_bands", {})
        bb_signal = bb_data.get("signal", "NEUTRAL")

        if bb_signal == "BUY":
            bullish_signals += 1
            confluences.append("Price at lower Bollinger Band")
        elif bb_signal == "SELL":
            bearish_signals += 1
            confluences.append("Price at upper Bollinger Band")

        if "squeeze" in bb_data.get("interpretation", "").lower():
            warnings.append("Volatility squeeze - await breakout direction")

        adx_data = technical_data.get("adx", {})
        adx_value = adx_data.get("adx", 0)
        adx_strength = adx_data.get("strength", "WEAK")
        adx_direction = adx_data.get("direction", "NEUTRAL")

        if adx_strength in ["STRONG", "VERY STRONG"]:
            if adx_direction == "BULLISH":
                bullish_signals += 1
                confluences.append(f"ADX: Strong uptrend ({adx_value:.1f})")
            elif adx_direction == "BEARISH":
                bearish_signals += 1
                confluences.append(f"ADX: Strong downtrend ({adx_value:.1f})")
        elif adx_strength == "WEAK":
            warnings.append(f"Weak trend strength (ADX {adx_value:.1f})")

        stoch_data = technical_data.get("stochastic", {})
        stoch_signal = stoch_data.get("signal", "NEUTRAL")

        if stoch_signal == "BUY":
            bullish_signals += 1
            confluences.append(f"Stochastic: {stoch_data.get('interpretation', 'Bullish')}")
        elif stoch_signal == "SELL":
            bearish_signals += 1
            confluences.append(f"Stochastic: {stoch_data.get('interpretation', 'Bearish')}")

        volume_data = technical_data.get("volume", {})
        volume_signal = volume_data.get("signal", "NEUTRAL")

        if volume_signal == "CONFIRM":
            confluences.append("High volume confirmation")
        elif volume_signal == "CAUTION":
            warnings.append("Low volume - weak confirmation")

        patterns = chart_data.get("patterns", [])
        for pattern in patterns:
            pattern_signal = pattern.get("signal", "NEUTRAL")
            pattern_name = pattern.get("name", "Unknown")
            
            if pattern_signal == "BUY":
                bullish_signals += 1
                confluences.append(f"Pattern: {pattern_name}")
            elif pattern_signal == "SELL":
                bearish_signals += 1
                confluences.append(f"Pattern: {pattern_name}")

        nearest_support = chart_data.get("nearest_support")
        nearest_resistance = chart_data.get("nearest_resistance")

        if nearest_support:
            distance_to_support = (current_price - nearest_support["price"]) / current_price * 100
            if distance_to_support < 1:  # Within 1% of support
                bullish_signals += 1
                confluences.append(f"Price at support level ({nearest_support['price']:.2f})")

        if nearest_resistance:
            distance_to_resistance = (nearest_resistance["price"] - current_price) / current_price * 100
            if distance_to_resistance < 1:  # Within 1% of resistance
                bearish_signals += 1
                confluences.append(f"Price at resistance level ({nearest_resistance['price']:.2f})")

        fib_data = technical_data.get("fibonacci", {})
        nearest_fib = fib_data.get("nearest_level")
        
        if nearest_fib in ["38.2", "50.0", "61.8"]:  # Key retracement levels
            confluences.append(f"Price near Fibonacci {nearest_fib}%")

        atr_data = technical_data.get("atr", {})
        volatility = atr_data.get("volatility", "NORMAL")
        
        if volatility in ["HIGH", "EXTREME"]:
            warnings.append(f"{volatility} volatility - wider stops recommended")

        confluence_count = len(confluences)
        
        if bullish_signals > bearish_signals:
            signal_type = SignalType.BUY.value
            confidence = min(100, (bullish_signals / max(1, bearish_signals)) * 30 + confluence_count * 10)
        elif bearish_signals > bullish_signals:
            signal_type = SignalType.SELL.value
            confidence = min(100, (bearish_signals / max(1, bullish_signals)) * 30 + confluence_count * 10)
        else:
            signal_type = SignalType.HOLD.value
            confidence = 40

        quality_score = self._calculate_quality_score(
            confluence_count=confluence_count,
            trend_strength=adx_value,
            volume_signal=volume_signal,
            pattern_count=len(patterns)
        )

        if quality_score >= 80:
            strength = SignalStrength.STRONG.value
        elif quality_score >= 60:
            strength = SignalStrength.MODERATE.value
        else:
            strength = SignalStrength.WEAK.value

        if confluence_count >= 4 and quality_score >= 70:
            trigger = TriggerType.IMMEDIATE.value
        elif confluence_count >= 2:
            trigger = TriggerType.WAIT_CONFIRMATION.value
        else:
            trigger = TriggerType.PULLBACK.value

        entry_description = self._create_entry_description(
            signal_type, technical_data, chart_data, confluences[:3]
        )

        return TradingSignal(
            signal_type=signal_type,
            confidence=round(confidence, 2),
            strength=strength,
            quality_score=round(quality_score, 2),
            confluence_count=confluence_count,
            entry_price=current_price,
            entry_description=entry_description,
            entry_trigger=trigger,
            reasons=confluences,
            warnings=warnings
        )

    def _calculate_quality_score(
        self,
        confluence_count: int,
        trend_strength: float,
        volume_signal: str,
        pattern_count: int
    ) -> float:
        """
        Calculate signal quality score (0-100)
        
        Args:
            confluence_count: Number of confluences
            trend_strength: ADX value
            volume_signal: Volume confirmation signal
            pattern_count: Number of patterns detected
        
        Returns:
            Quality score 0-100
        """
        score = 0

        score += min(confluence_count * 8, 40)

        if trend_strength > 40:
            score += 30
        elif trend_strength > 25:
            score += 20
        elif trend_strength > 15:
            score += 10

        if volume_signal == "CONFIRM":
            score += 15
        elif volume_signal == "NEUTRAL":
            score += 7

        score += min(pattern_count * 5, 15)

        return min(score, 100)

    def _create_entry_description(
        self,
        signal_type: str,
        technical_data: Dict,
        chart_data: Dict,
        top_confluences: List[str]
    ) -> str:
        """
        Create human-readable entry description
        
        Returns:
            Descriptive string
        """
        ma_data = technical_data.get("moving_averages", {})
        rsi_data = technical_data.get("rsi", {})
        
        ema21 = ma_data.get("ema21", 0)
        rsi_value = rsi_data.get("value", 50)
        
        description_parts = []
        
        if signal_type == "BUY":
            description_parts.append(f"Price above EMA21 ({ema21:.2f})")
            description_parts.append(f"RSI: {rsi_value:.1f}")
        elif signal_type == "SELL":
            description_parts.append(f"Price below EMA21 ({ema21:.2f})")
            description_parts.append(f"RSI: {rsi_value:.1f}")
        else:
            description_parts.append("No clear directional bias")
        
        if top_confluences:
            description_parts.append(f"Confluences: {', '.join(top_confluences[:2])}")
        
        return " | ".join(description_parts)

    def check_multi_timeframe_alignment(
        self,
        daily_signal: TradingSignal,
        h4_signal: TradingSignal,
        h1_signal: TradingSignal
    ) -> Dict:
        """
        Check if signals align across multiple timeframes
        
        Args:
            daily_signal: Daily timeframe signal
            h4_signal: 4-hour timeframe signal
            h1_signal: 1-hour timeframe signal
        
        Returns:
            Dict with alignment status and recommendation
        """
        signals = [daily_signal.signal_type, h4_signal.signal_type, h1_signal.signal_type]
        
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")
        
        if buy_count >= 2:
            alignment = "BULLISH"
            aligned = True
            recommendation = "Strong multi-timeframe BUY alignment"
        elif sell_count >= 2:
            alignment = "BEARISH"
            aligned = True
            recommendation = "Strong multi-timeframe SELL alignment"
        else:
            alignment = "MIXED"
            aligned = False
            recommendation = "Timeframes not aligned - wait for clarity"
        
        avg_confidence = (
            daily_signal.confidence + h4_signal.confidence + h1_signal.confidence
        ) / 3
        
        return {
            "aligned": aligned,
            "alignment": alignment,
            "average_confidence": round(avg_confidence, 2),
            "recommendation": recommendation,
            "daily": daily_signal.signal_type,
            "h4": h4_signal.signal_type,
            "h1": h1_signal.signal_type
        }

    def validate_signal_quality(self, signal: TradingSignal) -> Dict:
        """
        Validate if signal meets minimum quality standards
        
        Args:
            signal: TradingSignal to validate
        
        Returns:
            Dict with validation result
        """
        passed = True
        issues = []
        
        if signal.confluence_count < self.min_confluence_for_trade:
            passed = False
            issues.append(f"Insufficient confluences ({signal.confluence_count} < {self.min_confluence_for_trade})")
        
        if signal.quality_score < self.min_quality_score:
            passed = False
            issues.append(f"Quality score too low ({signal.quality_score} < {self.min_quality_score})")
        
        critical_warnings = [w for w in signal.warnings if "EXTREME" in w.upper() or "CAUTION" in w.upper()]
        if critical_warnings:
            issues.append(f"Critical warnings present: {', '.join(critical_warnings)}")
        
        return {
            "passed": passed,
            "quality_score": signal.quality_score,
            "confluence_count": signal.confluence_count,
            "issues": issues,
            "recommendation": "TRADE" if passed else "SKIP"
        }
    def generate_llm_analysis(
        self,
        technical_data: Dict,
        chart_data: Dict,
        current_price: float,
        symbol: str,
        timeframe: str
    ) -> Dict:
        market_analysis = {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": current_price,
            "technical_indicators": technical_data,
            "chart_patterns": chart_data.get("patterns", []),
            "support_resistance": {
                "support": chart_data.get("nearest_support"),
                "resistance": chart_data.get("nearest_resistance")
            }
        }
        
        llm_recommendation = llm_provider.generate_trading_recommendation(
            market_analysis=market_analysis,
            technical_indicators=technical_data,
            chart_patterns=chart_data.get("patterns", [])
        )
        
        return {
            "llm_analysis": llm_recommendation,
            "timestamp": str(datetime.now()),
            "model": "g4f"
        }