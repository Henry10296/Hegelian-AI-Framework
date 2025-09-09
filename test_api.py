#!/usr/bin/env python3
"""
Simple test script to verify Hegelian AI Framework API endpoints
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8001"
    
    print("Testing Hegelian AI Framework API...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Health endpoint: {response.status_code}")
        health_data = response.json()
        print(f"  Status: {health_data.get('status')}")
        print(f"  Components: {json.dumps(health_data.get('components'), indent=2)}")
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")
    
    # Test system info endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/info")
        print(f"✓ System info endpoint: {response.status_code}")
        info_data = response.json()
        print(f"  System: {info_data.get('name')} v{info_data.get('version')}")
    except Exception as e:
        print(f"✗ System info endpoint failed: {e}")
    
    print("\nAPI test completed!")

if __name__ == "__main__":
    test_api()