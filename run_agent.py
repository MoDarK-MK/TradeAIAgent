import numpy as np
from app.core.trading_agent import TradingAgent
from app.utils.logger import logger
import asyncio


async def main():
    logger.info("Starting MOD Trading Agent with g4f...")
    
    agent = TradingAgent(
        capital=10000,
        max_risk_percent=2.0,
        max_daily_loss_percent=5.0
    )
    
    np.random.seed(42)
    close_prices = np.array([100 + i + np.random.randn() for i in range(100)])
    high_prices = close_prices + np.abs(np.random.randn(100))
    low_prices = close_prices - np.abs(np.random.randn(100))
    open_prices = close_prices + np.random.randn(100)
    volume = np.random.randint(1000000, 10000000, 100)
    
    logger.info("Running analysis...")
    analysis = agent.analyze(
        symbol="BTC/USD",
        timeframe="1H",
        open_prices=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
        volume=volume
    )
    
    logger.info("=== MOD Trading Agent Analysis ===")
    logger.info(f"Signal: {analysis.get('signal', {}).get('signal_type')}")
    logger.info(f"Confidence: {analysis.get('signal', {}).get('confidence')}%")
    logger.info(f"Strength: {analysis.get('signal', {}).get('strength')}")
    logger.info(f"Quality Score: {analysis.get('signal', {}).get('quality_score')}")
    
    if analysis.get('llm_analysis'):
        logger.info("=== LLM Analysis (via g4f) ===")
        logger.info(analysis['llm_analysis'])
    
    print("\n✓ MOD Trading Agent executed successfully!")
    print("✓ Using g4f for LLM - No API key required!")


if __name__ == "__main__":
    asyncio.run(main())
