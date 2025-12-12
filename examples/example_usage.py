"""
Example usage of the Trading Agent
Demonstrates how to use the system for trading analysis
"""

import numpy as np
from app.core.trading_agent import TradingAgent


def generate_sample_data(length=100):
    """Generate sample OHLCV data for testing"""
    # Create synthetic price data with trend
    base_price = 42000
    trend = np.linspace(0, 2000, length)
    noise = np.random.randn(length) * 200
    
    close = base_price + trend + noise
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


def main():
    """Run example analysis"""
    print("=" * 60)
    print("AI TRADING AGENT - EXAMPLE USAGE")
    print("=" * 60)
    print()
    
    # Initialize Trading Agent
    agent = TradingAgent(
        capital=10000,  # $10,000 capital
        max_risk_percent=2.0,  # Risk 2% per trade
        max_daily_loss_percent=5.0  # Stop trading if lose 5% in a day
    )
    
    # Generate sample data
    print("📊 Generating sample BTC/USD data...")
    data = generate_sample_data(length=100)
    
    # Perform analysis
    print("🔍 Analyzing market conditions...")
    print()
    
    analysis = agent.analyze(
        symbol="BTC/USD",
        timeframe="1H",
        open_prices=data["open"],
        high=data["high"],
        low=data["low"],
        close=data["close"],
        volume=data["volume"],
        image_base64=None  # No chart image in this example
    )
    
    # Display results
    print("=" * 60)
    print("📈 ANALYSIS RESULTS")
    print("=" * 60)
    print()
    
    # Metadata
    print(f"Symbol: {analysis['metadata']['symbol']}")
    print(f"Timeframe: {analysis['metadata']['timeframe']}")
    print(f"Current Price: ${analysis['metadata']['current_price']:,.2f}")
    print(f"Analysis Time: {analysis['metadata']['timestamp']}")
    print()
    
    # Signal
    signal = analysis['signal']
    print("🎯 SIGNAL INFORMATION:")
    print(f"  Type: {signal['type']}")
    print(f"  Confidence: {signal['confidence']:.1f}%")
    print(f"  Strength: {signal['strength']}")
    print(f"  Quality Score: {signal['quality_score']:.1f}/100")
    print(f"  Confluences: {signal['confluence_count']}")
    print()
    
    # Entry
    entry = analysis['entry']
    print("📍 ENTRY INFORMATION:")
    print(f"  Price: ${entry['price']:,.2f}")
    print(f"  Trigger: {entry['trigger']}")
    print(f"  Description: {entry['description']}")
    print()
    
    # Risk Management
    if analysis['stop_loss']:
        sl = analysis['stop_loss']
        tp = analysis['take_profit']
        rr = analysis['risk_reward']
        
        print("🛡️ RISK MANAGEMENT:")
        print(f"  Stop Loss: ${sl['price']:,.2f} (-{sl['distance_percent']:.2f}%)")
        print(f"  Method: {sl['method']}")
        print(f"  Invalidation: {sl['invalidation_logic']}")
        print()
        
        print("💰 TAKE PROFIT TARGETS:")
        print(f"  TP1: ${tp['tp1']['price']:,.2f} (1:{tp['tp1']['ratio']:.1f}) - Close {tp['tp1']['position_percent']}%")
        print(f"  TP2: ${tp['tp2']['price']:,.2f} (1:{tp['tp2']['ratio']:.1f}) - Close {tp['tp2']['position_percent']}%")
        print(f"  TP3: ${tp['tp3']['price']:,.2f} (1:{tp['tp3']['ratio']:.1f}) - Close {tp['tp3']['position_percent']}%")
        print()
        
        print("📊 RISK/REWARD:")
        print(f"  Ratio: 1:{rr['ratio']:.2f}")
        print(f"  Risk Amount: ${rr['risk_amount']:,.2f}")
        print(f"  Profit Target: ${rr['profit_target']:,.2f}")
        print(f"  Status: {rr['status']}")
        print()
    
    # Technical Details
    indicators = analysis['technical_details']['indicators']
    print("📉 TECHNICAL INDICATORS:")
    print(f"  RSI: {indicators['RSI']['value']:.1f} - {indicators['RSI']['interpretation']}")
    print(f"  MACD: {indicators['MACD']['interpretation']}")
    print(f"  Trend: {indicators['MA_crossover']['trend']}")
    print(f"  ADX: {indicators['ADX']['value']:.1f} - {indicators['ADX']['strength']} {indicators['ADX']['direction']}")
    print(f"  Volatility: {indicators['ATR']['volatility']}")
    if indicators['Support']:
        print(f"  Support: ${indicators['Support']:,.2f}")
    if indicators['Resistance']:
        print(f"  Resistance: ${indicators['Resistance']:,.2f}")
    print()
    
    # Patterns
    patterns = analysis['technical_details']['patterns']
    if patterns:
        print("🎨 CHART PATTERNS DETECTED:")
        for pattern in patterns[:3]:
            print(f"  - {pattern['name']} ({pattern['type']}) - {pattern['signal']}")
        print()
    
    # Execution Checklist
    checklist = analysis['execution_checklist']
    print("✅ EXECUTION CHECKLIST:")
    print(f"  {'✓' if checklist['price_action_confirmed'] else '✗'} Price action confirmed")
    print(f"  {'✓' if checklist['momentum_aligned'] else '✗'} Momentum aligned")
    print(f"  {'✓' if checklist['volatility_acceptable'] else '✗'} Volatility acceptable")
    print(f"  {'✓' if checklist['risk_reward_positive'] else '✗'} Risk/Reward positive")
    print(f"  {'✓' if checklist.get('risk_limits_ok', False) else '✗'} Risk limits OK")
    print(f"  {'✓' if checklist['all_ready'] else '✗'} All systems ready")
    print()
    
    # Recommendations
    print("💡 RECOMMENDATIONS:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    print()
    
    # Warnings
    if analysis['warnings']:
        print("⚠️  WARNINGS:")
        for warning in analysis['warnings']:
            print(f"  - {warning}")
        print()
    
    # Final verdict
    print("=" * 60)
    quality = analysis['quality_validation']
    if quality['passed']:
        print("✅ VERDICT: TRADE SIGNAL APPROVED")
        print(f"   Quality Score: {quality['quality_score']:.1f}/100")
        print(f"   Confluences: {quality['confluence_count']}")
    else:
        print("❌ VERDICT: TRADE SIGNAL REJECTED")
        if quality['issues']:
            print("   Issues:")
            for issue in quality['issues']:
                print(f"   - {issue}")
    print("=" * 60)
    print()
    
    # Educational disclaimer
    print("⚠️  DISCLAIMER:")
    print("This analysis is for educational and professional use only.")
    print("Trading involves substantial risk of loss. Past performance is")
    print("not indicative of future results. Always do your own research")
    print("and consider consulting a financial advisor.")
    print()


if __name__ == "__main__":
    main()
