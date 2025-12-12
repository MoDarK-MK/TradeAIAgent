#!/usr/bin/env python3
"""
Integration Test Suite - Frontend & Backend
Tests all major features of the integrated system
"""

import asyncio
import aiohttp
import json
import time

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

async def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/health") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Health Check: {data['status']}")
                print(f"   Version: {data['version']}")
                return True
            else:
                print(f"❌ Health Check Failed: {resp.status}")
                return False

async def test_market_symbols():
    """Test market symbols endpoint"""
    print("\n📊 Testing Market Symbols...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/market/symbols") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Available Symbols: {len(data['symbols'])} symbols found")
                for symbol in data['symbols'][:3]:
                    print(f"   - {symbol['symbol']}: {symbol['name']}")
                return True
            else:
                print(f"❌ Market Symbols Failed: {resp.status}")
                return False

async def test_recent_signals():
    """Test recent signals endpoint"""
    print("\n📈 Testing Recent Signals...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/signals/recent?limit=5") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Recent Signals Loaded: {len(data)} signals")
                if data:
                    print(f"   Latest: {data[0]['signal']} ({data[0]['confidence']}%)")
                return True
            else:
                print(f"❌ Recent Signals Failed: {resp.status}")
                return False

async def test_signal_statistics():
    """Test signal statistics endpoint"""
    print("\n📊 Testing Signal Statistics...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/signals/statistics") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Signal Statistics Loaded")
                print(f"   Total Signals: {data['total_signals']}")
                print(f"   Buy Signals: {data['buy_signals']}")
                print(f"   Avg Confidence: {data['avg_confidence']}%")
                print(f"   Win Rate: {data['win_rate']}%")
                return True
            else:
                print(f"❌ Signal Statistics Failed: {resp.status}")
                return False

async def test_indicators_list():
    """Test indicators list endpoint"""
    print("\n🔧 Testing Indicators List...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/indicators/list") as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"✅ Indicators Loaded: {data['total_indicators']} indicators")
                indicators = list(data['indicators'].keys())[:5]
                for ind in indicators:
                    print(f"   - {ind}")
                return True
            else:
                print(f"❌ Indicators List Failed: {resp.status}")
                return False

async def test_websocket_connection():
    """Test WebSocket connection"""
    print("\n🔌 Testing WebSocket Connection...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"{WS_URL}/ws/signals") as ws:
                print("✅ WebSocket Connected")
                
                msg = await ws.receive_json(timeout=5)
                print(f"   Received: {msg['type']}")
                print(f"   Message: {msg['message']}")
                
                await ws.close()
                print("✅ WebSocket Disconnected Gracefully")
                return True
    except Exception as e:
        print(f"❌ WebSocket Failed: {str(e)}")
        return False

async def test_api_docs():
    """Test API documentation endpoint"""
    print("\n📚 Testing API Documentation...")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/docs") as resp:
            if resp.status == 200:
                print(f"✅ API Documentation Available at /docs")
                return True
            else:
                print(f"❌ API Documentation Failed: {resp.status}")
                return False

async def run_all_tests():
    """Run all integration tests"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║         MOD Trading Agent - Integration Test Suite            ║
    ║                                                               ║
    ║  Testing Frontend-Backend Integration & All APIs              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"🎯 Testing Server: {BASE_URL}")
    print(f"⏱️  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    results.append(("Health Check", await test_health_check()))
    results.append(("API Documentation", await test_api_docs()))
    results.append(("Market Symbols", await test_market_symbols()))
    results.append(("Recent Signals", await test_recent_signals()))
    results.append(("Signal Statistics", await test_signal_statistics()))
    results.append(("Indicators List", await test_indicators_list()))
    results.append(("WebSocket Connection", await test_websocket_connection()))
    
    print("\n" + "="*60)
    print("📋 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} | {test_name}")
    
    print("="*60)
    print(f"Overall: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - INTEGRATION SUCCESSFUL!")
        print("\n✨ Features Verified:")
        print("   ✅ REST API endpoints functional")
        print("   ✅ WebSocket real-time streaming")
        print("   ✅ Market data endpoints")
        print("   ✅ Signal analysis endpoints")
        print("   ✅ API documentation")
        print("\n🚀 System ready for production!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⛔ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test execution failed: {str(e)}")
