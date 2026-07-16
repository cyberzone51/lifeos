# LifeOS — AI Personal Operating System

Universal AI assistant for managing everyday life.

## Features

- AI Assistant (natural language)
- Personal Finance (expenses, income, budget)
- Tasks & Planner
- Habits Tracking
- Health Tracking (weight, sleep, mood)
- Journal & Notes
- Knowledge Base
- AI Memory
- Voice Input
- Telegram Mini App
- Multi-language (15+)
- Multi-currency

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy + Alembic
- Google Gemini AI

### Frontend
- Flutter 3.x
- Material 3
- Riverpod
- GoRouter

## Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd LifeOS
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Start Frontend

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

### 4. Docker (Recommended)

```bash
docker-compose up -d
```

## API Documentation

Once running, visit: http://localhost:8000/docs

## Project Structure

```
LifeOS/
├── backend/           # Python FastAPI
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Config, security
│   │   ├── models/    # SQLAlchemy models
│   │   ├── services/  # Business logic
│   │   └── ai/        # AI module
│   └── tests/
├── frontend/          # Flutter app
│   └── lib/
│       ├── app/       # App config, router, theme
│       ├── features/  # Feature modules
│       └── core/      # Shared utilities
├── docker/            # Docker config
└── docs/              # Documentation
```

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
pytest
```

### Frontend

```bash
cd frontend
flutter pub get
flutter analyze
flutter test
```

## License

MIT
