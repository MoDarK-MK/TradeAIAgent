"""
API Test Script
Test the Trading Agent API endpoints
"""

import requests
import json
import numpy as np
from datetime import datetime


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_indicators_list():
    """Test indicators list endpoint"""
    print_section("Testing Indicators List")
    
    response = requests.get(f"{BASE_URL}/indicators/list")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Indicators: {data['total_indicators']}")
        print("\nAvailable Indicators:")
        for name, info in list(data['indicators'].items())[:3]:
            print(f"  - {name}: {info['description']}")
        print("  ...")
    
    return response.status_code == 200


def generate_sample_data(length=100, trend="up"):
    """Generate sample OHLCV data"""
    base_price = 42000
    
    if trend == "up":
        trend_component = np.linspace(0, 2000, length)
    elif trend == "down":
        trend_component = np.linspace(2000, 0, length)
    else:
        trend_component = np.zeros(length)
    
    noise = np.random.randn(length) * 200
    close = base_price + trend_component + noise
    
    open_prices = close + np.random.randn(length) * 50
    high = np.maximum(open_prices, close) + np.abs(np.random.randn(length) * 100)
    low = np.minimum(open_prices, close) - np.abs(np.random.randn(length) * 100)
    volume = np.random.randint(1000000, 5000000, length)
    
    return {
        "open": close.tolist(),
        "high": high.tolist(),
        "low": low.tolist(),
        "close": close.tolist(),
        "volume": volume.tolist()
    }


def test_analyze_bullish():
    """Test analysis with bullish data"""
    print_section("Testing Analysis - Bullish Trend")
    
    data = {
        "symbol": "BTC/USD",
        "timeframe": "1H",
        "ohlcv": generate_sample_data(100, trend="up"),
        "capital": 10000,
        "risk_percent": 2.0
    }
    
    print("Sending request...")
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        analysis = response.json()
        
        print("\n📊 Analysis Results:")
        print(f"  Symbol: {analysis['metadata']['symbol']}")
        print(f"  Current Price: ${analysis['metadata']['current_price']:,.2f}")
        print(f"\n🎯 Signal:")
        print(f"  Type: {analysis['signal']['type']}")
        print(f"  Confidence: {analysis['signal']['confidence']:.1f}%")
        print(f"  Strength: {analysis['signal']['strength']}")
        print(f"  Quality Score: {analysis['signal']['quality_score']:.1f}/100")
        print(f"  Confluences: {analysis['signal']['confluence_count']}")
        
        if analysis['stop_loss']:
            print(f"\n🛡️ Risk Management:")
            print(f"  Entry: ${analysis['entry']['price']:,.2f}")
            print(f"  Stop Loss: ${analysis['stop_loss']['price']:,.2f}")
            print(f"  TP1: ${analysis['take_profit']['tp1']['price']:,.2f} (1:{analysis['take_profit']['tp1']['ratio']:.1f})")
            print(f"  TP2: ${analysis['take_profit']['tp2']['price']:,.2f} (1:{analysis['take_profit']['tp2']['ratio']:.1f})")
            print(f"  TP3: ${analysis['take_profit']['tp3']['price']:,.2f} (1:{analysis['take_profit']['tp3']['ratio']:.1f})")
            print(f"  R:R Ratio: 1:{analysis['risk_reward']['ratio']:.2f} ({analysis['risk_reward']['status']})")
        
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(analysis['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
        
        if analysis['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in analysis['warnings'][:2]:
                print(f"  - {warning}")
        
        print(f"\n✅ Quality Check: {'PASSED' if analysis['quality_validation']['passed'] else 'FAILED'}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def test_analyze_bearish():
    """Test analysis with bearish data"""
    print_section("Testing Analysis - Bearish Trend")
    
    data = {
        "symbol": "EUR/USD",
        "timeframe": "4H",
        "ohlcv": generate_sample_data(100, trend="down"),
        "capital": 10000,
        "risk_percent": 2.0
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        analysis = response.json()
        print(f"\n🎯 Signal: {analysis['signal']['type']}")
        print(f"  Confidence: {analysis['signal']['confidence']:.1f}%")
        print(f"  Quality Score: {analysis['signal']['quality_score']:.1f}/100")
    
    return response.status_code == 200


def test_analyze_insufficient_data():
    """Test analysis with insufficient data"""
    print_section("Testing Error Handling - Insufficient Data")
    
    data = {
        "symbol": "BTC/USD",
        "timeframe": "1H",
        "ohlcv": generate_sample_data(20, trend="up"),  # Only 20 candles
        "capital": 10000
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Expected Error: {response.status_code == 400}")
    
    if response.status_code == 400:
        print(f"Error Message: {response.json()}")
    
    return response.status_code == 400


def test_summary():
    """Test summary endpoint"""
    print_section("Testing Summary Endpoint")
    
    response = requests.get(f"{BASE_URL}/summary")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        summary = response.json()
        print(f"\nSummary:")
        print(json.dumps(summary, indent=2))
    
    return response.status_code == 200


def run_all_tests():
    """Run all API tests"""
    print("\n" + "🚀" * 30)
    print("  AI TRADING AGENT - API TEST SUITE")
    print("🚀" * 30)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Indicators List", test_indicators_list),
        ("Bullish Analysis", test_analyze_bullish),
        ("Bearish Analysis", test_analyze_bearish),
        ("Error Handling", test_analyze_insufficient_data),
        ("Summary", test_summary)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("  TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:12} - {name}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        
        if success:
            print("\n✅ All tests passed successfully!")
        else:
            print("\n⚠️  Some tests failed. Check the output above.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server.")
        print(f"   Make sure the server is running at {BASE_URL}")
        print("   Start it with: python -m uvicorn app.main:app --reload")
