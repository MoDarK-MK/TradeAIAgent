"""
Chart Image Analyzer
Uses OpenCV and pattern recognition to analyze trading chart images
"""

import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class CandlePattern(Enum):
    """Recognized candlestick patterns"""
    HAMMER = "Hammer"
    INVERTED_HAMMER = "Inverted Hammer"
    BULLISH_ENGULFING = "Bullish Engulfing"
    BEARISH_ENGULFING = "Bearish Engulfing"
    MORNING_STAR = "Morning Star"
    EVENING_STAR = "Evening Star"
    DOJI = "Doji"
    SHOOTING_STAR = "Shooting Star"
    HANGING_MAN = "Hanging Man"
    PIERCING_PATTERN = "Piercing Pattern"
    DARK_CLOUD_COVER = "Dark Cloud Cover"
    THREE_WHITE_SOLDIERS = "Three White Soldiers"
    THREE_BLACK_CROWS = "Three Black Crows"
    INSIDE_BAR = "Inside Bar"
    PIN_BAR = "Pin Bar"


@dataclass
class SupportResistance:
    """Support/Resistance level data"""
    price: float
    level_type: str  # SUPPORT or RESISTANCE
    strength: int  # 1-10
    touches: int  # Number of times price touched this level
    recent: bool  # If level was touched recently


@dataclass
class ChartPattern:
    """Identified chart pattern"""
    pattern_name: str
    pattern_type: str  # CONTINUATION or REVERSAL
    confidence: float  # 0-100
    target_price: Optional[float]
    signal: str  # BUY, SELL, NEUTRAL


class ChartAnalyzer:
    """
    Analyzes trading chart images for patterns, support/resistance levels
    """

    def __init__(self):
        self.patterns_detected = []
        self.support_resistance_levels = []

    def decode_base64_image(self, base64_string: str) -> np.ndarray:
        """
        Decode base64 image string to numpy array
        
        Args:
            base64_string: Base64 encoded image
        
        Returns:
            OpenCV image array (numpy)
        """
        # Remove header if present
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # Decode
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        return opencv_image

    def detect_candles(self, image: np.ndarray) -> List[Dict]:
        """
        Detect individual candlesticks in the chart
        
        Args:
            image: OpenCV image array
        
        Returns:
            List of detected candles with properties
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours (simplified detection)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        candles = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by aspect ratio (candles are vertical)
            if h > w * 2 and h > 10:  # Basic candle shape detection
                candles.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "body_top": y,
                    "body_bottom": y + h
                })
        
        return candles

    def identify_candlestick_patterns(
        self,
        open_prices: np.ndarray,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray
    ) -> List[ChartPattern]:
        """
        Identify candlestick patterns using TA-Lib pattern recognition
        
        Args:
            open_prices, high, low, close: OHLC data
        
        Returns:
            List of identified patterns
        """
        import talib
        
        patterns = []

        # Hammer
        hammer = talib.CDLHAMMER(open_prices, high, low, close)
        if hammer[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Hammer",
                pattern_type="REVERSAL",
                confidence=abs(hammer[-1]),
                target_price=None,
                signal="BUY" if hammer[-1] > 0 else "NEUTRAL"
            ))

        # Engulfing
        engulfing = talib.CDLENGULFING(open_prices, high, low, close)
        if engulfing[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Bullish Engulfing" if engulfing[-1] > 0 else "Bearish Engulfing",
                pattern_type="REVERSAL",
                confidence=abs(engulfing[-1]),
                target_price=None,
                signal="BUY" if engulfing[-1] > 0 else "SELL"
            ))

        # Morning Star / Evening Star
        morning_star = talib.CDLMORNINGSTAR(open_prices, high, low, close)
        if morning_star[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Morning Star",
                pattern_type="REVERSAL",
                confidence=abs(morning_star[-1]),
                target_price=None,
                signal="BUY"
            ))

        evening_star = talib.CDLEVENINGSTAR(open_prices, high, low, close)
        if evening_star[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Evening Star",
                pattern_type="REVERSAL",
                confidence=abs(evening_star[-1]),
                target_price=None,
                signal="SELL"
            ))

        # Doji
        doji = talib.CDLDOJI(open_prices, high, low, close)
        if doji[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Doji",
                pattern_type="REVERSAL",
                confidence=abs(doji[-1]),
                target_price=None,
                signal="NEUTRAL"
            ))

        # Shooting Star
        shooting_star = talib.CDLSHOOTINGSTAR(open_prices, high, low, close)
        if shooting_star[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Shooting Star",
                pattern_type="REVERSAL",
                confidence=abs(shooting_star[-1]),
                target_price=None,
                signal="SELL"
            ))

        # Three White Soldiers / Three Black Crows
        three_white = talib.CDL3WHITESOLDIERS(open_prices, high, low, close)
        if three_white[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Three White Soldiers",
                pattern_type="CONTINUATION",
                confidence=abs(three_white[-1]),
                target_price=None,
                signal="BUY"
            ))

        three_black = talib.CDL3BLACKCROWS(open_prices, high, low, close)
        if three_black[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Three Black Crows",
                pattern_type="CONTINUATION",
                confidence=abs(three_black[-1]),
                target_price=None,
                signal="SELL"
            ))

        # Piercing Pattern
        piercing = talib.CDLPIERCING(open_prices, high, low, close)
        if piercing[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Piercing Pattern",
                pattern_type="REVERSAL",
                confidence=abs(piercing[-1]),
                target_price=None,
                signal="BUY"
            ))

        # Dark Cloud Cover
        dark_cloud = talib.CDLDARKCLOUDCOVER(open_prices, high, low, close)
        if dark_cloud[-1] != 0:
            patterns.append(ChartPattern(
                pattern_name="Dark Cloud Cover",
                pattern_type="REVERSAL",
                confidence=abs(dark_cloud[-1]),
                target_price=None,
                signal="SELL"
            ))

        return patterns

    def detect_support_resistance(
        self,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        lookback: int = 50
    ) -> List[SupportResistance]:
        """
        Detect support and resistance levels
        
        Args:
            high, low, close: Price data
            lookback: Number of periods to analyze
        
        Returns:
            List of support/resistance levels
        """
        levels = []
        
        # Use recent data
        recent_high = high[-lookback:] if len(high) > lookback else high
        recent_low = low[-lookback:] if len(low) > lookback else low
        recent_close = close[-lookback:] if len(close) > lookback else close
        
        # Find local maxima (resistance)
        for i in range(2, len(recent_high) - 2):
            if (recent_high[i] > recent_high[i-1] and 
                recent_high[i] > recent_high[i-2] and
                recent_high[i] > recent_high[i+1] and
                recent_high[i] > recent_high[i+2]):
                
                # Check how many times price touched this level
                touches = self._count_touches(recent_close, recent_high[i], tolerance=0.02)
                
                levels.append(SupportResistance(
                    price=recent_high[i],
                    level_type="RESISTANCE",
                    strength=min(touches * 2, 10),
                    touches=touches,
                    recent=(i >= len(recent_high) - 10)
                ))
        
        # Find local minima (support)
        for i in range(2, len(recent_low) - 2):
            if (recent_low[i] < recent_low[i-1] and 
                recent_low[i] < recent_low[i-2] and
                recent_low[i] < recent_low[i+1] and
                recent_low[i] < recent_low[i+2]):
                
                touches = self._count_touches(recent_close, recent_low[i], tolerance=0.02)
                
                levels.append(SupportResistance(
                    price=recent_low[i],
                    level_type="SUPPORT",
                    strength=min(touches * 2, 10),
                    touches=touches,
                    recent=(i >= len(recent_low) - 10)
                ))
        
        # Sort by strength and remove duplicates
        levels = self._remove_close_levels(levels)
        levels.sort(key=lambda x: x.strength, reverse=True)
        
        return levels[:10]  # Return top 10 levels

    def _count_touches(
        self, prices: np.ndarray, level: float, tolerance: float = 0.02
    ) -> int:
        """
        Count how many times price touched a specific level
        
        Args:
            prices: Price array
            level: Price level to check
            tolerance: Percentage tolerance (default 2%)
        
        Returns:
            Number of touches
        """
        upper_bound = level * (1 + tolerance)
        lower_bound = level * (1 - tolerance)
        
        touches = np.sum((prices >= lower_bound) & (prices <= upper_bound))
        return int(touches)

    def _remove_close_levels(
        self, levels: List[SupportResistance], min_distance: float = 0.01
    ) -> List[SupportResistance]:
        """
        Remove levels that are too close to each other
        
        Args:
            levels: List of levels
            min_distance: Minimum distance between levels (1% default)
        
        Returns:
            Filtered list
        """
        if not levels:
            return []
        
        filtered = [levels[0]]
        
        for level in levels[1:]:
            is_far_enough = True
            for existing in filtered:
                distance = abs(level.price - existing.price) / existing.price
                if distance < min_distance:
                    is_far_enough = False
                    break
            
            if is_far_enough:
                filtered.append(level)
        
        return filtered

    def detect_trend_channels(
        self, high: np.ndarray, low: np.ndarray, close: np.ndarray
    ) -> Dict:
        """
        Detect trend channels (uptrend, downtrend, sideways)
        
        Returns:
            Dict with trend channel information
        """
        # Simple linear regression on closing prices
        x = np.arange(len(close))
        
        # Calculate trend line
        z = np.polyfit(x, close, 1)
        p = np.poly1d(z)
        trend_line = p(x)
        
        # Calculate slope
        slope = z[0]
        slope_percent = (slope / close[0]) * 100
        
        # Classify trend
        if slope_percent > 0.5:
            trend_type = "UPTREND"
            signal = "BUY"
        elif slope_percent < -0.5:
            trend_type = "DOWNTREND"
            signal = "SELL"
        else:
            trend_type = "SIDEWAYS"
            signal = "NEUTRAL"
        
        # Calculate channel width (standard deviation from trend line)
        deviations = close - trend_line
        upper_channel = trend_line + np.std(deviations) * 2
        lower_channel = trend_line - np.std(deviations) * 2
        
        return {
            "trend_type": trend_type,
            "slope": slope,
            "slope_percent": slope_percent,
            "signal": signal,
            "trend_line": trend_line[-1],
            "upper_channel": upper_channel[-1],
            "lower_channel": lower_channel[-1],
            "channel_width": upper_channel[-1] - lower_channel[-1]
        }

    def full_chart_analysis(
        self,
        image_base64: Optional[str],
        open_prices: np.ndarray,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray
    ) -> Dict:
        """
        Perform complete chart analysis
        
        Args:
            image_base64: Optional base64 encoded chart image
            open_prices, high, low, close: OHLC data
        
        Returns:
            Comprehensive chart analysis
        """
        # Pattern recognition
        patterns = self.identify_candlestick_patterns(open_prices, high, low, close)
        
        # Support/Resistance
        sr_levels = self.detect_support_resistance(high, low, close)
        
        # Trend channels
        trend_info = self.detect_trend_channels(high, low, close)
        
        # Find current position relative to S/R levels
        current_price = close[-1]
        nearest_support = None
        nearest_resistance = None
        
        for level in sr_levels:
            if level.level_type == "SUPPORT" and level.price < current_price:
                if nearest_support is None or level.price > nearest_support.price:
                    nearest_support = level
            elif level.level_type == "RESISTANCE" and level.price > current_price:
                if nearest_resistance is None or level.price < nearest_resistance.price:
                    nearest_resistance = level
        
        return {
            "patterns": [
                {
                    "name": p.pattern_name,
                    "type": p.pattern_type,
                    "confidence": p.confidence,
                    "signal": p.signal
                }
                for p in patterns
            ],
            "support_resistance": [
                {
                    "price": level.price,
                    "type": level.level_type,
                    "strength": level.strength,
                    "touches": level.touches,
                    "recent": level.recent
                }
                for level in sr_levels
            ],
            "nearest_support": {
                "price": nearest_support.price,
                "strength": nearest_support.strength
            } if nearest_support else None,
            "nearest_resistance": {
                "price": nearest_resistance.price,
                "strength": nearest_resistance.strength
            } if nearest_resistance else None,
            "trend": trend_info,
            "current_price": current_price
        }
