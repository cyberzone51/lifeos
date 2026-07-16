#!/bin/bash
# LifeOS Setup Script

set -e

echo "🚀 Setting up LifeOS..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker"
    exit 1
fi

# Copy env file
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
fi

# Start PostgreSQL and Redis
echo "🐘 Starting PostgreSQL and Redis..."
docker-compose up -d postgres redis

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
sleep 5

# Setup Backend
echo "🐍 Setting up Backend..."
cd backend
pip install -r requirements.txt

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To start the frontend:"
echo "  cd frontend"
echo "  flutter pub get"
echo "  flutter run -d chrome"
