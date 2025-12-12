@echo off
REM Start MOD Trading Agent Integrated System
REM Frontend + Backend + Real-time WebSocket

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║          MOD Trading Agent - Integrated System                ║
echo ║                                                               ║
echo ║  Starting AI-Powered Trading Intelligence Engine              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo 📦 Backend: FastAPI Server
echo 🎨 Frontend: AI Trading Dashboard
echo 🤖 Engine: LLM-Powered Signal Generation ^(g4f^)
echo 💾 Database: In-Memory Analysis History
echo 🔌 Real-time: WebSocket Signal Streaming
echo.

echo 🚀 Starting server...
echo 📍 Web Dashboard: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🔗 WebSocket: ws://localhost:8000/ws/signals
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
