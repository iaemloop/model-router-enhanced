#!/bin/bash

# Enhanced Model Router Setup and Test Script

echo "🚀 Enhanced Model Router Setup and Test"
echo "========================================"

# Check if we have OpenRouter API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  OPENROUTER_API_KEY not set. Creating test mode..."
    echo "export OPENROUTER_API_KEY=test-key" >> ~/.bashrc
    source ~/.bashrc
    echo "📝 Set OPENROUTER_API_KEY=test-key for testing"
else
    echo "✅ OPENROUTER_API_KEY is set"
fi

# Test the router
echo ""
echo "🧪 Testing Enhanced Model Router"
echo "================================"

echo "1. Testing simple task (should prefer free model):"
python3 router.py --models models.json --task "Hello, how are you?" --dry

echo ""
echo "2. Testing complex task (may request paid model):"
python3 router.py --models models.json --task "Debug this Python function that's causing memory leaks" --dry

echo ""
echo "3. Checking available models:"
python3 router.py --check-models

echo ""
echo "4. Testing model status:"
python3 model_tester.py --status

echo ""
echo "📊 Enhanced Model Router Setup Complete!"
echo "========================================"
echo "🎯 Features implemented:"
echo "   ✅ Free model prioritization"
echo "   ✅ Paid model approval system" 
echo "   ✅ Daily model health testing"
echo "   ✅ Cost optimization tracking"
echo "   ✅ Status monitoring"
echo ""
echo "🚀 To start daily monitoring:"
echo "   python3 daemon.py --start"
echo ""
echo "📋 To view reports:"
echo "   python3 model_tester.py --report"
echo "   python3 router.py --cost-report"