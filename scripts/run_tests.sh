#!/bin/bash
# LifeOS Test Runner

set -e

echo "🧪 Running LifeOS Tests..."

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    exit 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/../backend"

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -q pytest pytest-asyncio httpx

# Run tests
echo ""
echo "▶️  Running unit tests..."
pytest tests/test_ai_router.py tests/test_finance_agent.py tests/test_gamification.py tests/test_goals.py tests/test_mental.py -v

echo ""
echo "▶️  Running API integration tests..."
pytest tests/test_api.py -v

echo ""
echo "✅ All tests completed!"
