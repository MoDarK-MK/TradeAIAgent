#!/usr/bin/env python3
"""
Integrated MOD Trading Agent - Frontend + Backend
Starts the FastAPI server with integrated frontend dashboard
"""

import sys
import os
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║          MOD Trading Agent - Integrated Dashboard            ║
    ║                                                               ║
    ║  Starting AI-Powered Trading Intelligence Engine              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("📦 Backend: FastAPI Server")
    print("🎨 Frontend: AI Trading Dashboard")
    print("🤖 Engine: LLM-Powered Signal Generation")
    print("💾 Database: In-Memory Analysis History")
    print("🔌 Real-time: WebSocket Signal Streaming")
    print()
    
    print("🚀 Starting server...")
    print("📍 Web Dashboard: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔗 WebSocket: ws://localhost:8000/ws/signals")
    print()
    print("Press CTRL+C to stop the server")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
