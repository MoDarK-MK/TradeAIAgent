"""
Technical Analysis Engine
Implements all core technical indicators for trading signal generation.
"""

import numpy as np
import pandas as pd
import talib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class IndicatorResult:
    """Standard result format for indicator calculations"""
    value: float
    interpretation: str
    signal: str  # BUY, SELL, NEUTRAL


class TechnicalAnalysis:
    """
    Professional-grade technical analysis engine
    Implements RSI, MACD, Bollinger Bands, Moving Averages, ATR, Fibonacci, ADX, Stochastic
    """

    def __init__(self):
        self.indicators = {}

    def calculate_rsi(
        self, prices: np.ndarray, period: int = 14
    ) -> IndicatorResult:
        """
        Calculate Relative Strength Index
        
        Args:
            prices: Array of closing prices
            period: RSI period (default 14)
        
        Returns:
            IndicatorResult with RSI value and interpretation
        """
        rsi = talib.RSI(prices, timeperiod=period)
        current_rsi = rsi[-1]

        if current_rsi > 70:
            interpretation = f"Overbought ({current_rsi:.2f})"
            signal = "SELL"
        elif current_rsi < 30:
            interpretation = f"Oversold ({current_rsi:.2f})"
            signal = "BUY"
        elif 40 <= current_rsi <= 60:
            interpretation = f"Neutral zone ({current_rsi:.2f})"
            signal = "NEUTRAL"
        else:
            interpretation = f"Moderate ({current_rsi:.2f})"
            signal = "NEUTRAL"

        return IndicatorResult(
            value=current_rsi,
            interpretation=interpretation,
            signal=signal
        )

    def calculate_macd(
        self,
        prices: np.ndarray,
        fast: int = 12,
        slow: int = 26,
        signal_period: int = 9
    ) -> Dict:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Returns:
            Dict with MACD line, signal line, histogram, and interpretation
        """
        macd, signal, histogram = talib.MACD(
            prices, fastperiod=fast, slowperiod=slow, signalperiod=signal_period
        )

        current_macd = macd[-1]
        current_signal = signal[-1]
        current_hist = histogram[-1]
        prev_hist = histogram[-2] if len(histogram) > 1 else 0

        if current_hist > 0 and prev_hist <= 0:
            interpretation = "Bullish crossover"
            signal_type = "BUY"
        elif current_hist < 0 and prev_hist >= 0:
            interpretation = "Bearish crossover"
            signal_type = "SELL"
        elif current_macd > current_signal and current_hist > 0:
            interpretation = "Bullish momentum"
            signal_type = "BUY"
        elif current_macd < current_signal and current_hist < 0:
            interpretation = "Bearish momentum"
            signal_type = "SELL"
        else:
            interpretation = "Neutral"
            signal_type = "NEUTRAL"

        return {
            "macd": current_macd,
            "signal": current_signal,
            "histogram": current_hist,
            "interpretation": interpretation,
            "signal_type": signal_type
        }

    def calculate_bollinger_bands(
        self, prices: np.ndarray, period: int = 20, std_dev: int = 2
    ) -> Dict:
        """
        Calculate Bollinger Bands
        
        Returns:
            Dict with upper, middle, lower bands and interpretation
        """
        upper, middle, lower = talib.BBANDS(
            prices, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev
        )

        current_price = prices[-1]
        current_upper = upper[-1]
        current_middle = middle[-1]
        current_lower = lower[-1]

        band_width = current_upper - current_lower
        position = (current_price - current_lower) / band_width * 100

        if current_price >= current_upper:
            interpretation = "Price at upper band - overbought"
            signal = "SELL"
        elif current_price <= current_lower:
            interpretation = "Price at lower band - oversold"
            signal = "BUY"
        elif band_width < (current_middle * 0.02):  # Squeeze detection
            interpretation = "Volatility squeeze - breakout pending"
            signal = "NEUTRAL"
        else:
            interpretation = f"Price at {position:.1f}% of band width"
            signal = "NEUTRAL"

        return {
            "upper": current_upper,
            "middle": current_middle,
            "lower": current_lower,
            "current_price": current_price,
            "bandwidth": band_width,
            "position_percent": position,
            "interpretation": interpretation,
            "signal": signal
        }

    def calculate_moving_averages(
        self, prices: np.ndarray
    ) -> Dict:
        """
        Calculate multiple moving averages (EMA21, SMA50, SMA200)
        
        Returns:
            Dict with MA values and trend determination
        """
        ema21 = talib.EMA(prices, timeperiod=21)
        sma50 = talib.SMA(prices, timeperiod=50)
        sma200 = talib.SMA(prices, timeperiod=200)

        current_price = prices[-1]
        current_ema21 = ema21[-1]
        current_sma50 = sma50[-1]
        current_sma200 = sma200[-1]

        if current_price > current_ema21 > current_sma50 > current_sma200:
            trend = "STRONG UPTREND"
            signal = "BUY"
        elif current_price < current_ema21 < current_sma50 < current_sma200:
            trend = "STRONG DOWNTREND"
            signal = "SELL"
        elif current_price > current_ema21 > current_sma50:
            trend = "UPTREND"
            signal = "BUY"
        elif current_price < current_ema21 < current_sma50:
            trend = "DOWNTREND"
            signal = "SELL"
        else:
            trend = "SIDEWAYS"
            signal = "NEUTRAL"

        crossover = None
        if len(ema21) > 1 and len(sma50) > 1:
            if ema21[-2] < sma50[-2] and current_ema21 > current_sma50:
                crossover = "Golden Cross (EMA21 > SMA50)"
            elif ema21[-2] > sma50[-2] and current_ema21 < current_sma50:
                crossover = "Death Cross (EMA21 < SMA50)"

        return {
            "ema21": current_ema21,
            "sma50": current_sma50,
            "sma200": current_sma200,
            "current_price": current_price,
            "trend": trend,
            "signal": signal,
            "crossover": crossover
        }

    def calculate_atr(
        self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14
    ) -> Dict:
        """
        Calculate Average True Range for volatility measurement
        
        Returns:
            Dict with ATR value and volatility classification
        """
        atr = talib.ATR(high, low, close, timeperiod=period)
        current_atr = atr[-1]
        current_price = close[-1]

        atr_percent = (current_atr / current_price) * 100

        if atr_percent < 1:
            volatility = "LOW"
            interpretation = "Low volatility - tight stops possible"
        elif atr_percent < 3:
            volatility = "NORMAL"
            interpretation = "Normal volatility"
        elif atr_percent < 5:
            volatility = "HIGH"
            interpretation = "High volatility - wider stops needed"
        else:
            volatility = "EXTREME"
            interpretation = "Extreme volatility - caution advised"

        return {
            "atr": current_atr,
            "atr_percent": atr_percent,
            "volatility": volatility,
            "interpretation": interpretation
        }

    def calculate_fibonacci_levels(
        self, prices: np.ndarray, lookback: int = 100
    ) -> Dict:
        """
        Calculate Fibonacci retracement levels
        
        Args:
            prices: Price array
            lookback: Number of periods to look back for high/low
        
        Returns:
            Dict with Fibonacci levels
        """
        recent_prices = prices[-lookback:] if len(prices) > lookback else prices
        high = np.max(recent_prices)
        low = np.min(recent_prices)
        diff = high - low

        levels = {
            "0.0": high,
            "23.6": high - (diff * 0.236),
            "38.2": high - (diff * 0.382),
            "50.0": high - (diff * 0.5),
            "61.8": high - (diff * 0.618),
            "78.6": high - (diff * 0.786),
            "100.0": low
        }

        current_price = prices[-1]
        
        nearest_level = min(levels.items(), key=lambda x: abs(x[1] - current_price))

        return {
            "levels": levels,
            "high": high,
            "low": low,
            "current_price": current_price,
            "nearest_level": nearest_level[0],
            "nearest_price": nearest_level[1]
        }

    def calculate_adx(
        self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14
    ) -> Dict:
        """
        Calculate ADX (Average Directional Index) for trend strength
        
        Returns:
            Dict with ADX value and trend strength classification
        """
        adx = talib.ADX(high, low, close, timeperiod=period)
        plus_di = talib.PLUS_DI(high, low, close, timeperiod=period)
        minus_di = talib.MINUS_DI(high, low, close, timeperiod=period)

        current_adx = adx[-1]
        current_plus_di = plus_di[-1]
        current_minus_di = minus_di[-1]

        if current_adx < 20:
            strength = "WEAK"
            interpretation = "Weak or no trend - avoid trend-following strategies"
        elif current_adx < 40:
            strength = "MODERATE"
            interpretation = "Moderate trend strength"
        elif current_adx < 60:
            strength = "STRONG"
            interpretation = "Strong trend - good for trend following"
        else:
            strength = "VERY STRONG"
            interpretation = "Very strong trend - potential exhaustion soon"

        if current_plus_di > current_minus_di:
            direction = "BULLISH"
        else:
            direction = "BEARISH"

        return {
            "adx": current_adx,
            "plus_di": current_plus_di,
            "minus_di": current_minus_di,
            "strength": strength,
            "direction": direction,
            "interpretation": interpretation
        }

    def calculate_stochastic(
        self,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        k_period: int = 14,
        d_period: int = 3
    ) -> Dict:
        """
        Calculate Stochastic Oscillator
        
        Returns:
            Dict with %K, %D values and interpretation
        """
        slowk, slowd = talib.STOCH(
            high, low, close,
            fastk_period=k_period,
            slowk_period=d_period,
            slowd_period=d_period
        )

        current_k = slowk[-1]
        current_d = slowd[-1]
        prev_k = slowk[-2] if len(slowk) > 1 else current_k
        prev_d = slowd[-2] if len(slowd) > 1 else current_d

        if prev_k < prev_d and current_k > current_d and current_k < 20:
            interpretation = "Bullish crossover in oversold zone"
            signal = "BUY"
        elif prev_k > prev_d and current_k < current_d and current_k > 80:
            interpretation = "Bearish crossover in overbought zone"
            signal = "SELL"
        elif current_k > 80:
            interpretation = "Overbought"
            signal = "SELL"
        elif current_k < 20:
            interpretation = "Oversold"
            signal = "BUY"
        else:
            interpretation = "Neutral"
            signal = "NEUTRAL"

        return {
            "k": current_k,
            "d": current_d,
            "interpretation": interpretation,
            "signal": signal
        }

    def analyze_volume(
        self, volume: np.ndarray, period: int = 20
    ) -> Dict:
        """
        Analyze volume relative to average
        
        Returns:
            Dict with volume analysis
        """
        avg_volume = talib.SMA(volume, timeperiod=period)
        current_volume = volume[-1]
        current_avg = avg_volume[-1]

        ratio = current_volume / current_avg

        if ratio > 1.5:
            interpretation = "High volume - strong interest"
            signal = "CONFIRM"
        elif ratio < 0.5:
            interpretation = "Low volume - weak interest"
            signal = "CAUTION"
        else:
            interpretation = "Normal volume"
            signal = "NEUTRAL"

        return {
            "current_volume": current_volume,
            "average_volume": current_avg,
            "ratio": ratio,
            "interpretation": interpretation,
            "signal": signal
        }

    def full_analysis(
        self,
        open_prices: np.ndarray,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        volume: np.ndarray
    ) -> Dict:
        """
        Perform complete technical analysis with all indicators
        
        Returns:
            Comprehensive analysis dictionary
        """
        return {
            "rsi": self.calculate_rsi(close).__dict__,
            "macd": self.calculate_macd(close),
            "bollinger_bands": self.calculate_bollinger_bands(close),
            "moving_averages": self.calculate_moving_averages(close),
            "atr": self.calculate_atr(high, low, close),
            "fibonacci": self.calculate_fibonacci_levels(close),
            "adx": self.calculate_adx(high, low, close),
            "stochastic": self.calculate_stochastic(high, low, close),
            "volume": self.analyze_volume(volume)
        }
