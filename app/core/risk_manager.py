"""
Risk Manager
Handles Stop Loss, Take Profit calculations, position sizing, and portfolio risk management
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class StopLossMethod(Enum):
    """Stop loss calculation methods"""
    ATR_BASED = "ATR"
    LEVEL_BASED = "LEVEL"
    PERCENTAGE_BASED = "PERCENTAGE"


@dataclass
class StopLoss:
    """Stop loss data"""
    price: float
    distance_pips: float
    distance_percent: float
    method: str
    invalidation_logic: str


@dataclass
class TakeProfit:
    """Take profit target"""
    price: float
    distance_pips: float
    distance_percent: float
    ratio: float  # Risk:Reward ratio
    position_percentage: int  # % of position to close at this TP


@dataclass
class PositionSize:
    """Position sizing calculation"""
    units: float
    lot_size: float
    risk_amount: float
    position_value: float
    leverage_required: float


@dataclass
class RiskReward:
    """Risk/Reward analysis"""
    ratio: float
    risk_amount: float
    profit_target: float
    status: str  # EXCELLENT, GOOD, ACCEPTABLE, REJECT


class RiskManager:
    """
    Professional risk management system
    Calculates SL, TP, position sizes, and manages portfolio risk
    """

    def __init__(
        self,
        capital: float = 10000,
        max_risk_percent: float = 2.0,
        max_daily_loss_percent: float = 5.0,
        max_drawdown_percent: float = 15.0
    ):
        self.capital = capital
        self.max_risk_percent = max_risk_percent
        self.max_daily_loss_percent = max_daily_loss_percent
        self.max_drawdown_percent = max_drawdown_percent
        self.daily_losses = 0
        self.open_positions = []

    def calculate_stop_loss(
        self,
        entry_price: float,
        signal_type: str,
        atr: float,
        support_level: Optional[float] = None,
        resistance_level: Optional[float] = None,
        method: StopLossMethod = StopLossMethod.ATR_BASED
    ) -> StopLoss:
        """
        Calculate Stop Loss price
        
        Args:
            entry_price: Entry price for trade
            signal_type: BUY or SELL
            atr: Average True Range value
            support_level: Support price level
            resistance_level: Resistance price level
            method: Calculation method
        
        Returns:
            StopLoss object
        """
        if method == StopLossMethod.ATR_BASED:
            # ATR-based: 1.5x ATR from entry
            if signal_type == "BUY":
                sl_price = entry_price - (atr * 1.5)
                invalidation = f"Price closes below {sl_price:.2f} (1.5x ATR)"
            else:  # SELL
                sl_price = entry_price + (atr * 1.5)
                invalidation = f"Price closes above {sl_price:.2f} (1.5x ATR)"

        elif method == StopLossMethod.LEVEL_BASED:
            # Level-based: Just beyond support/resistance
            if signal_type == "BUY":
                if support_level is None:
                    support_level = entry_price - (atr * 2)
                sl_price = support_level - (atr * 0.2)  # Small buffer beyond support
                invalidation = f"Price breaks below support at {support_level:.2f}"
            else:  # SELL
                if resistance_level is None:
                    resistance_level = entry_price + (atr * 2)
                sl_price = resistance_level + (atr * 0.2)  # Small buffer beyond resistance
                invalidation = f"Price breaks above resistance at {resistance_level:.2f}"

        elif method == StopLossMethod.PERCENTAGE_BASED:
            # Percentage-based: 2-3% from entry
            stop_percent = 0.025  # 2.5%
            if signal_type == "BUY":
                sl_price = entry_price * (1 - stop_percent)
                invalidation = f"Price drops {stop_percent*100}% from entry"
            else:  # SELL
                sl_price = entry_price * (1 + stop_percent)
                invalidation = f"Price rises {stop_percent*100}% from entry"

        # Calculate distance
        distance = abs(entry_price - sl_price)
        distance_pips = distance
        distance_percent = (distance / entry_price) * 100

        return StopLoss(
            price=round(sl_price, 2),
            distance_pips=round(distance_pips, 2),
            distance_percent=round(distance_percent, 3),
            method=method.value,
            invalidation_logic=invalidation
        )

    def calculate_take_profits(
        self,
        entry_price: float,
        stop_loss: StopLoss,
        signal_type: str,
        resistance_level: Optional[float] = None,
        support_level: Optional[float] = None,
        fib_levels: Optional[Dict] = None
    ) -> Dict[str, TakeProfit]:
        """
        Calculate multiple Take Profit targets
        
        Args:
            entry_price: Entry price
            stop_loss: StopLoss object
            signal_type: BUY or SELL
            resistance_level: Resistance for SELL targets
            support_level: Support for BUY targets
            fib_levels: Fibonacci extension levels
        
        Returns:
            Dict with TP1, TP2, TP3 targets
        """
        risk_distance = stop_loss.distance_pips

        # TP1: 1:1 Risk/Reward (50% position)
        if signal_type == "BUY":
            tp1_price = entry_price + risk_distance
        else:
            tp1_price = entry_price - risk_distance

        tp1 = TakeProfit(
            price=round(tp1_price, 2),
            distance_pips=round(risk_distance, 2),
            distance_percent=round((risk_distance / entry_price) * 100, 3),
            ratio=1.0,
            position_percentage=50
        )

        # TP2: 1:2 Risk/Reward (30% position)
        if signal_type == "BUY":
            tp2_price = entry_price + (risk_distance * 2)
        else:
            tp2_price = entry_price - (risk_distance * 2)

        tp2 = TakeProfit(
            price=round(tp2_price, 2),
            distance_pips=round(risk_distance * 2, 2),
            distance_percent=round((risk_distance * 2 / entry_price) * 100, 3),
            ratio=2.0,
            position_percentage=30
        )

        # TP3: 1:3 Risk/Reward or next major level (20% position)
        if signal_type == "BUY":
            tp3_price = entry_price + (risk_distance * 3)
            # Adjust to resistance if available and closer
            if resistance_level and resistance_level > tp2_price and resistance_level < tp3_price * 1.2:
                tp3_price = resistance_level
        else:
            tp3_price = entry_price - (risk_distance * 3)
            # Adjust to support if available and closer
            if support_level and support_level < tp2_price and support_level > tp3_price * 0.8:
                tp3_price = support_level

        tp3 = TakeProfit(
            price=round(tp3_price, 2),
            distance_pips=round(abs(entry_price - tp3_price), 2),
            distance_percent=round((abs(entry_price - tp3_price) / entry_price) * 100, 3),
            ratio=round(abs(entry_price - tp3_price) / risk_distance, 2),
            position_percentage=20
        )

        return {
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3
        }

    def calculate_risk_reward(
        self,
        entry_price: float,
        stop_loss: StopLoss,
        take_profits: Dict[str, TakeProfit],
        capital: Optional[float] = None
    ) -> RiskReward:
        """
        Calculate overall Risk/Reward ratio
        
        Args:
            entry_price: Entry price
            stop_loss: StopLoss object
            take_profits: Dict of TakeProfit targets
            capital: Trading capital (uses self.capital if None)
        
        Returns:
            RiskReward analysis
        """
        if capital is None:
            capital = self.capital

        risk_amount = capital * (self.max_risk_percent / 100)

        # Calculate weighted average profit
        tp1 = take_profits["tp1"]
        tp2 = take_profits["tp2"]
        tp3 = take_profits["tp3"]

        # Weighted profit calculation
        total_profit = (
            (tp1.distance_pips * tp1.position_percentage / 100) +
            (tp2.distance_pips * tp2.position_percentage / 100) +
            (tp3.distance_pips * tp3.position_percentage / 100)
        )

        # Calculate actual ratio
        ratio = total_profit / stop_loss.distance_pips

        # Actual profit target in currency
        profit_target = risk_amount * ratio

        # Classify status
        if ratio >= 2.5:
            status = "EXCELLENT"
        elif ratio >= 2.0:
            status = "GOOD"
        elif ratio >= 1.5:
            status = "ACCEPTABLE"
        else:
            status = "REJECT"

        return RiskReward(
            ratio=round(ratio, 2),
            risk_amount=round(risk_amount, 2),
            profit_target=round(profit_target, 2),
            status=status
        )

    def calculate_position_size(
        self,
        entry_price: float,
        stop_loss: StopLoss,
        capital: Optional[float] = None,
        risk_percent: Optional[float] = None
    ) -> PositionSize:
        """
        Calculate appropriate position size
        
        Args:
            entry_price: Entry price
            stop_loss: StopLoss object
            capital: Trading capital
            risk_percent: Risk percentage per trade
        
        Returns:
            PositionSize calculation
        """
        if capital is None:
            capital = self.capital
        if risk_percent is None:
            risk_percent = self.max_risk_percent

        risk_amount = capital * (risk_percent / 100)
        sl_distance = stop_loss.distance_pips

        # Calculate position size
        # Position Size = Risk Amount / Stop Loss Distance
        units = risk_amount / sl_distance
        position_value = units * entry_price
        
        # Calculate lot size (for forex: 1 lot = 100,000 units)
        lot_size = units / 100000

        # Calculate leverage required
        leverage_required = position_value / capital

        return PositionSize(
            units=round(units, 2),
            lot_size=round(lot_size, 4),
            risk_amount=round(risk_amount, 2),
            position_value=round(position_value, 2),
            leverage_required=round(leverage_required, 2)
        )

    def check_daily_loss_limit(self, potential_loss: float) -> Dict:
        """
        Check if trade would exceed daily loss limit
        
        Args:
            potential_loss: Potential loss amount
        
        Returns:
            Dict with check result
        """
        max_daily_loss = self.capital * (self.max_daily_loss_percent / 100)
        current_plus_potential = self.daily_losses + potential_loss
        
        allowed = current_plus_potential <= max_daily_loss
        remaining = max_daily_loss - self.daily_losses

        return {
            "allowed": allowed,
            "current_daily_loss": round(self.daily_losses, 2),
            "potential_loss": round(potential_loss, 2),
            "max_daily_loss": round(max_daily_loss, 2),
            "remaining_allowance": round(remaining, 2),
            "message": "Trade allowed" if allowed else "Daily loss limit would be exceeded"
        }

    def check_portfolio_risk(
        self,
        new_position_risk: float,
        max_open_positions: int = 5
    ) -> Dict:
        """
        Check overall portfolio risk limits
        
        Args:
            new_position_risk: Risk amount for new position
            max_open_positions: Maximum allowed open positions
        
        Returns:
            Dict with portfolio risk check
        """
        current_positions = len(self.open_positions)
        total_risk = sum([p.get("risk_amount", 0) for p in self.open_positions]) + new_position_risk
        total_risk_percent = (total_risk / self.capital) * 100

        checks = {
            "position_count_ok": current_positions < max_open_positions,
            "current_positions": current_positions,
            "max_positions": max_open_positions,
            "total_risk": round(total_risk, 2),
            "total_risk_percent": round(total_risk_percent, 2),
            "max_drawdown_percent": self.max_drawdown_percent,
            "within_limits": total_risk_percent < self.max_drawdown_percent
        }

        checks["all_checks_passed"] = (
            checks["position_count_ok"] and checks["within_limits"]
        )

        return checks

    def calculate_trailing_stop(
        self,
        entry_price: float,
        current_price: float,
        signal_type: str,
        atr: float,
        profit_locked: float = 0.5
    ) -> Optional[float]:
        """
        Calculate trailing stop price
        
        Args:
            entry_price: Original entry price
            current_price: Current market price
            signal_type: BUY or SELL
            atr: Current ATR value
            profit_locked: Multiple of ATR to trail by (default 0.5)
        
        Returns:
            New stop loss price or None if not in profit
        """
        if signal_type == "BUY":
            # Check if in profit
            if current_price <= entry_price:
                return None
            
            # Trail by 0.5x ATR
            trailing_sl = current_price - (atr * profit_locked)
            
            # Never trail below entry (move to BE + small buffer first)
            if trailing_sl < entry_price:
                trailing_sl = entry_price + (entry_price * 0.001)  # BE + 0.1%
            
            return round(trailing_sl, 2)
        
        else:  # SELL
            # Check if in profit
            if current_price >= entry_price:
                return None
            
            # Trail by 0.5x ATR
            trailing_sl = current_price + (atr * profit_locked)
            
            # Never trail above entry
            if trailing_sl > entry_price:
                trailing_sl = entry_price - (entry_price * 0.001)
            
            return round(trailing_sl, 2)

    def full_risk_analysis(
        self,
        entry_price: float,
        signal_type: str,
        atr: float,
        support_level: Optional[float] = None,
        resistance_level: Optional[float] = None,
        fib_levels: Optional[Dict] = None
    ) -> Dict:
        """
        Perform complete risk analysis for a trade
        
        Returns:
            Comprehensive risk management data
        """
        # Calculate Stop Loss (try level-based first, fallback to ATR)
        if signal_type == "BUY" and support_level:
            sl_method = StopLossMethod.LEVEL_BASED
        elif signal_type == "SELL" and resistance_level:
            sl_method = StopLossMethod.LEVEL_BASED
        else:
            sl_method = StopLossMethod.ATR_BASED

        stop_loss = self.calculate_stop_loss(
            entry_price=entry_price,
            signal_type=signal_type,
            atr=atr,
            support_level=support_level,
            resistance_level=resistance_level,
            method=sl_method
        )

        # Calculate Take Profits
        take_profits = self.calculate_take_profits(
            entry_price=entry_price,
            stop_loss=stop_loss,
            signal_type=signal_type,
            resistance_level=resistance_level,
            support_level=support_level,
            fib_levels=fib_levels
        )

        # Calculate Risk/Reward
        risk_reward = self.calculate_risk_reward(
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profits=take_profits
        )

        # Calculate Position Size
        position_size = self.calculate_position_size(
            entry_price=entry_price,
            stop_loss=stop_loss
        )

        # Check limits
        daily_check = self.check_daily_loss_limit(risk_reward.risk_amount)
        portfolio_check = self.check_portfolio_risk(risk_reward.risk_amount)

        return {
            "stop_loss": {
                "price": stop_loss.price,
                "distance_pips": stop_loss.distance_pips,
                "distance_percent": stop_loss.distance_percent,
                "method": stop_loss.method,
                "invalidation_logic": stop_loss.invalidation_logic
            },
            "take_profit": {
                "tp1": {
                    "price": take_profits["tp1"].price,
                    "distance_pips": take_profits["tp1"].distance_pips,
                    "ratio": take_profits["tp1"].ratio,
                    "position_percent": take_profits["tp1"].position_percentage
                },
                "tp2": {
                    "price": take_profits["tp2"].price,
                    "distance_pips": take_profits["tp2"].distance_pips,
                    "ratio": take_profits["tp2"].ratio,
                    "position_percent": take_profits["tp2"].position_percentage
                },
                "tp3": {
                    "price": take_profits["tp3"].price,
                    "distance_pips": take_profits["tp3"].distance_pips,
                    "ratio": take_profits["tp3"].ratio,
                    "position_percent": take_profits["tp3"].position_percentage
                }
            },
            "risk_reward": {
                "ratio": risk_reward.ratio,
                "risk_amount": risk_reward.risk_amount,
                "profit_target": risk_reward.profit_target,
                "status": risk_reward.status
            },
            "position_sizing": {
                "units": position_size.units,
                "lot_size": position_size.lot_size,
                "position_value": position_size.position_value,
                "leverage_required": position_size.leverage_required
            },
            "risk_checks": {
                "daily_limit": daily_check,
                "portfolio_limit": portfolio_check,
                "all_passed": daily_check["allowed"] and portfolio_check["all_checks_passed"]
            }
        }
