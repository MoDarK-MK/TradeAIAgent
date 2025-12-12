#!/bin/bash
# Quick Start Script for AI Trading Agent (Linux/Mac)

echo "===================================="
echo "AI TRADING AGENT - QUICK START"
echo "===================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

echo "[1/5] Checking Docker installation... OK"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[2/5] Creating .env file from template..."
    cp .env.example .env
    echo "[INFO] Please edit .env file with your configuration"
    echo ""
else
    echo "[2/5] .env file already exists... OK"
    echo ""
fi

# Build and start containers
echo "[3/5] Building Docker containers..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "[ERROR] Docker build failed"
    exit 1
fi

echo ""
echo "[4/5] Starting services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to start services"
    exit 1
fi

echo ""
echo "[5/5] Waiting for services to be ready..."
sleep 10

echo ""
echo "===================================="
echo "SERVICES STARTED SUCCESSFULLY!"
echo "===================================="
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check:      http://localhost:8000/health"
echo "WebSocket:         ws://localhost:8000/ws/signals"
echo ""
echo "To view logs:      docker-compose logs -f"
echo "To stop services:  docker-compose down"
echo ""
echo "To run example:"
echo "  python examples/example_usage.py"
echo ""
echo "To test API:"
echo "  python examples/test_api.py"
echo ""
