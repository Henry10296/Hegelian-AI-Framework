#!/usr/bin/env python3
"""
Test script to demonstrate proper import of ai_core.models package
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the models package correctly
    from ai_core.models import EthicalCase, DecisionResult, ThesisResult, AntithesisResult, SynthesisResult
    
    print("✅ Successfully imported all models:")
    print(f"  - EthicalCase: {EthicalCase}")
    print(f"  - DecisionResult: {DecisionResult}")
    print(f"  - ThesisResult: {ThesisResult}")
    print(f"  - AntithesisResult: {AntithesisResult}")
    print(f"  - SynthesisResult: {SynthesisResult}")
    
    # Test creating an instance
    case = EthicalCase(
        title="Test Case",
        description="A test ethical case"
    )
    print(f"\n✅ Successfully created EthicalCase instance: {case.title}")
    
    print("\n🎉 All imports working correctly!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("\n💡 This is likely because:")
    print("1. You're trying to run __init__.py directly (which doesn't work)")
    print("2. Python path doesn't include the project root")
    print("\n📋 Correct usage:")
    print("   python test_models_import.py")
    print("   # NOT: python ai_core/models/__init__.py")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")