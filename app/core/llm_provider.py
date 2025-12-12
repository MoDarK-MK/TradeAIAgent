import g4f
from typing import Optional
from app.config import settings
from app.utils.logger import logger


class LLMProvider:
    def __init__(self, use_g4f: bool = True):
        self.use_g4f = use_g4f or settings.use_g4f
        self.model = settings.gpt_model
        
        if self.use_g4f:
            logger.info(f"Initialized LLM with g4f - Model: {self.model}")
        else:
            logger.warning("Using LLM without API key - g4f not enabled")

    async def generate_analysis(
        self,
        prompt: str,
        max_tokens: int = 1500,
        temperature: float = 0.7
    ) -> str:
        try:
            if self.use_g4f:
                response = await g4f.ChatCompletion.create_async(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response
            else:
                logger.error("g4f not enabled")
                return "Analysis unavailable"
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return f"Error generating analysis: {str(e)}"

    def generate_analysis_sync(
        self,
        prompt: str,
        max_tokens: int = 1500,
        temperature: float = 0.7
    ) -> str:
        try:
            if self.use_g4f:
                response = g4f.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response
            else:
                logger.error("g4f not enabled")
                return "Analysis unavailable"
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return f"Error generating analysis: {str(e)}"

    def generate_trading_recommendation(
        self,
        market_analysis: dict,
        technical_indicators: dict,
        chart_patterns: dict
    ) -> str:
        prompt = f"""
Based on the following market analysis, provide a trading recommendation:

Market Analysis:
{market_analysis}

Technical Indicators:
{technical_indicators}

Chart Patterns:
{chart_patterns}

Please provide:
1. Trading Signal (BUY/SELL/HOLD)
2. Confidence Level (0-100%)
3. Entry Points
4. Stop Loss
5. Take Profit Targets
6. Risk/Reward Ratio
7. Key Reasons for the Recommendation
"""
        return self.generate_analysis_sync(prompt)

    def analyze_chart_image(
        self,
        chart_description: str,
        technical_data: dict
    ) -> str:
        prompt = f"""
Analyze the following chart and technical data to identify trading opportunities:

Chart Description:
{chart_description}

Technical Data:
{technical_data}

Provide:
1. Identified Patterns
2. Support/Resistance Levels
3. Trend Analysis
4. Entry Opportunities
5. Risk Assessment
"""
        return self.generate_analysis_sync(prompt)

    def generate_market_summary(self, market_data: dict) -> str:
        prompt = f"""
Generate a concise market summary based on:

Market Data:
{market_data}

Include:
1. Market Sentiment
2. Key Movements
3. Volatility Assessment
4. Trading Opportunities
5. Risk Factors
"""
        return self.generate_analysis_sync(prompt)


llm_provider = LLMProvider(use_g4f=settings.use_g4f)
