@echo off
REM Quick Start Script for AI Trading Agent (Windows)

echo ====================================
echo AI TRADING AGENT - QUICK START
echo ====================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/5] Checking Docker installation... OK
echo.

REM Check if .env exists
if not exist .env (
    echo [2/5] Creating .env file from template...
    copy .env.example .env
    echo [INFO] Please edit .env file with your configuration
    echo.
) else (
    echo [2/5] .env file already exists... OK
    echo.
)

REM Build and start containers
echo [3/5] Building Docker containers...
docker-compose build

if %errorlevel% neq 0 (
    echo [ERROR] Docker build failed
    pause
    exit /b 1
)

echo.
echo [4/5] Starting services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo [ERROR] Failed to start services
    pause
    exit /b 1
)

echo.
echo [5/5] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ====================================
echo SERVICES STARTED SUCCESSFULLY!
echo ====================================
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check:      http://localhost:8000/health
echo WebSocket:         ws://localhost:8000/ws/signals
echo.
echo To view logs:      docker-compose logs -f
echo To stop services:  docker-compose down
echo.
echo To run example:
echo   python examples\example_usage.py
echo.
echo To test API:
echo   python examples\test_api.py
echo.
pause
