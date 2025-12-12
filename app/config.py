"""
Configuration Management
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    app_name: str = Field(default="AI Trading Agent", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    
    # Database
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="trading_db", alias="POSTGRES_DB")
    postgres_user: str = Field(default="trading_user", alias="POSTGRES_USER")
    postgres_password: str = Field(default="password", alias="POSTGRES_PASSWORD")
    
    # Redis
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, alias="REDIS_PASSWORD")
    
    # Trading Configuration
    default_capital: float = Field(default=10000, alias="DEFAULT_CAPITAL")
    max_risk_percent: float = Field(default=2.0, alias="MAX_RISK_PERCENT")
    max_daily_loss_percent: float = Field(default=5.0, alias="MAX_DAILY_LOSS_PERCENT")
    max_drawdown_percent: float = Field(default=15.0, alias="MAX_DRAWDOWN_PERCENT")
    max_open_positions: int = Field(default=5, alias="MAX_OPEN_POSITIONS")
    max_correlation: float = Field(default=0.70, alias="MAX_CORRELATION")
    
    # API Keys
    binance_api_key: Optional[str] = Field(default=None, alias="BINANCE_API_KEY")
    binance_api_secret: Optional[str] = Field(default=None, alias="BINANCE_API_SECRET")
    news_api_key: Optional[str] = Field(default=None, alias="NEWS_API_KEY")
    
    # Security
    secret_key: str = Field(default="your-secret-key-min-32-characters-long", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/trading_agent.log", alias="LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Construct database URL"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


# Global settings instance
settings = Settings()
