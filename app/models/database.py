"""
Database Models for TimescaleDB/PostgreSQL
"""

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.config import settings


Base = declarative_base()


class TradeSignal(Base):
    """Store trading signals"""
    __tablename__ = "trade_signals"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    symbol = Column(String(50), index=True)
    timeframe = Column(String(10))
    signal_type = Column(String(10))  # BUY, SELL, HOLD
    confidence = Column(Float)
    quality_score = Column(Float)
    confluence_count = Column(Integer)
    
    entry_price = Column(Float)
    stop_loss_price = Column(Float)
    take_profit_1 = Column(Float)
    take_profit_2 = Column(Float)
    take_profit_3 = Column(Float)
    
    risk_reward_ratio = Column(Float)
    position_size = Column(Float)
    
    technical_data = Column(JSON)  # Store full technical analysis
    executed = Column(Boolean, default=False)


class Trade(Base):
    """Store executed trades"""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, index=True)
    
    symbol = Column(String(50), index=True)
    side = Column(String(10))  # BUY or SELL
    
    entry_time = Column(DateTime, default=datetime.utcnow)
    entry_price = Column(Float)
    position_size = Column(Float)
    
    stop_loss = Column(Float)
    take_profit_1 = Column(Float)
    take_profit_2 = Column(Float)
    take_profit_3 = Column(Float)
    
    exit_time = Column(DateTime, nullable=True)
    exit_price = Column(Float, nullable=True)
    
    profit_loss = Column(Float, nullable=True)
    profit_loss_percent = Column(Float, nullable=True)
    
    status = Column(String(20))  # OPEN, CLOSED, STOPPED_OUT
    notes = Column(String(500), nullable=True)


class OHLCVData(Base):
    """Store historical OHLCV data (TimescaleDB hypertable)"""
    __tablename__ = "ohlcv_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    symbol = Column(String(50), index=True)
    timeframe = Column(String(10), index=True)
    
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class PerformanceMetrics(Base):
    """Store trading performance metrics"""
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    
    win_rate = Column(Float, default=0.0)
    profit_factor = Column(Float, default=0.0)
    
    total_profit = Column(Float, default=0.0)
    total_loss = Column(Float, default=0.0)
    net_profit = Column(Float, default=0.0)
    
    max_drawdown = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, nullable=True)
    
    average_win = Column(Float, default=0.0)
    average_loss = Column(Float, default=0.0)


# Database connection
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
