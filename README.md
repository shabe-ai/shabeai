# ShabeAI CRM

A modern CRM built with FastAPI backend and Next.js frontend.

### Production deployment (Vercel + Convex Cloud)

1. **Create a Vercel project** and select the `frontend` folder as root.  
2. Add the env vars shown below.  
3. Every push to **main** auto-deploys.

Required env vars:

| Key | Where to get it |
| --- | --------------- |
| `NEXT_PUBLIC_CONVEX_URL` | Convex dashboard → Deployments |
| `NEXT_PUBLIC_BASE_URL`   | Your Vercel domain (`https://app.shabe.ai`) |
| `NEXT_PUBLIC_STRIPE_PRICE_ID` | Stripe dashboard → Products |
| `STRIPE_SECRET_KEY` | Stripe dashboard → Developers → API keys |
| `STRIPE_WEBHOOK_SECRET` | `stripe listen --print-secret` |

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

**Windows (PowerShell):**
```powershell
# Start development environment with hot reloading
.\dev.ps1 dev

# Show all available commands
.\dev.ps1 help
```

**Linux/macOS:**
```sh
# Start development environment with hot reloading
make dev

# Or use docker-compose directly
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

This will start:
- **Backend API** at http://localhost:8000
- **Frontend** at http://localhost:3000  
- **PostgreSQL Database** at localhost:5432

## Development Commands

**Windows (PowerShell):**
```powershell
# Show all available commands
.\dev.ps1 help

# Start development environment
.\dev.ps1 dev

# Run tests
.\dev.ps1 test
.\dev.ps1 test-frontend

# Lint code
.\dev.ps1 lint

# Database operations
.\dev.ps1 db-migrate
.\dev.ps1 db-reset  # WARNING: Deletes all data

# View logs
.\dev.ps1 logs
.\dev.ps1 logs-backend
.\dev.ps1 logs-frontend
```

**Linux/macOS:**
```sh
# Show all available commands
make help

# Start development environment
make dev

# Run tests
make test
make test-frontend

# Lint code
make lint
make lint-frontend

# Database operations
make db-migrate
make db-reset  # WARNING: Deletes all data

# View logs
make logs
make logs-backend
make logs-frontend
```

## Manual Setup (without Docker)

### Backend Setup

```sh
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```sh
cd frontend
pnpm install
pnpm dev
```

### Database Setup

```sh
# Start PostgreSQL (or use Docker)
docker run -d --name postgres -e POSTGRES_DB=shabeai -e POSTGRES_USER=shabeai -e POSTGRES_PASSWORD=shabeai_password -p 5432:5432 postgres:15-alpine

# Run migrations
cd backend
alembic upgrade head
```

## Project Structure

- `backend/app/` - FastAPI app, routers, models, services
- `backend/tests/` - Backend API and service tests
- `frontend/` - Next.js frontend application
- `docker-compose.yml` - Production Docker setup
- `docker-compose.dev.yml` - Development Docker setup

## API Documentation

Once the backend is running, see the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 