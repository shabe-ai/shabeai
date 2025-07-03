# Contributing to ShabeAI CRM

Thank you for your interest in contributing to ShabeAI CRM! This document provides guidelines and information for contributors.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/shabeai.git
   cd shabeai
   ```

2. **Start development environment**
   ```bash
   # Windows
   .\dev.ps1 dev
   
   # Linux/macOS
   make dev
   ```

3. **Access the application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## 📋 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes
- Follow the coding standards (see below)
- Write tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Backend tests
cd backend && poetry run pytest

# Frontend tests
cd frontend && pnpm test

# Linting
cd backend && poetry run ruff check .
cd frontend && pnpm lint
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 🏗️ Project Structure

```
shabeai/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── routers/        # API routes
│   │   ├── services/       # Business logic
│   │   ├── models.py       # Database models
│   │   └── schemas/        # Pydantic schemas
│   ├── tests/              # Backend tests
│   └── alembic/            # Database migrations
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities and API clients
│   └── tests/             # Frontend tests
├── docker-compose.yml      # Production Docker setup
├── docker-compose.dev.yml  # Development Docker setup
└── .github/               # CI/CD workflows
```

## 📝 Coding Standards

### Python (Backend)
- **Formatter**: Ruff (black-compatible)
- **Linter**: Ruff
- **Type Checker**: MyPy
- **Line Length**: 88 characters
- **Import Sorting**: Ruff (isort-compatible)

```bash
# Format code
cd backend && poetry run ruff format .

# Lint code
cd backend && poetry run ruff check .

# Type check
cd backend && poetry run mypy app/
```

### TypeScript/JavaScript (Frontend)
- **Formatter**: Prettier
- **Linter**: ESLint
- **Type Checker**: TypeScript

```bash
# Format and lint
cd frontend && pnpm lint

# Type check
cd frontend && pnpm type-check
```

### Git Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

Examples:
feat(auth): add JWT authentication
fix(api): resolve user creation bug
docs(readme): update installation instructions
refactor(services): simplify lead service logic
test(api): add integration tests for leads endpoint
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_api.py

# Run integration tests
poetry run pytest tests/integration/
```

### Frontend Testing
```bash
cd frontend

# Run unit tests
pnpm test

# Run E2E tests
pnpm test:e2e

# Run tests in watch mode
pnpm test:watch
```

## 🐳 Docker Development

### Development Commands
```bash
# Start all services
.\dev.ps1 dev  # Windows
make dev       # Linux/macOS

# View logs
.\dev.ps1 logs-backend
.\dev.ps1 logs-frontend

# Run tests in containers
.\dev.ps1 test
.\dev.ps1 test-frontend

# Access container shells
.\dev.ps1 shell-backend
.\dev.ps1 shell-frontend
```

### Database Operations
```bash
# Run migrations
.\dev.ps1 db-migrate

# Reset database (WARNING: deletes all data)
.\dev.ps1 db-reset
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in the respective directories:

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql://shabeai:shabeai_password@localhost:5432/shabeai
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Production Deployment
1. Create a new release tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. The CI/CD pipeline will automatically:
   - Run all tests
   - Build Docker images
   - Deploy to production

### Manual Deployment
```bash
# Build production images
docker-compose build

# Deploy
docker-compose up -d
```

## 🐛 Bug Reports

When reporting bugs, please include:
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, browser, versions, etc.
- **Screenshots**: If applicable

## 💡 Feature Requests

When requesting features, please include:
- **Description**: Clear description of the feature
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How you think it should work
- **Alternatives**: Any alternative solutions you've considered

## 📞 Getting Help

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check the README and API docs

## 🤝 Code Review Process

1. **Pull Request**: Create a PR with a clear description
2. **CI Checks**: Ensure all CI checks pass
3. **Review**: Address reviewer feedback
4. **Merge**: Once approved, merge to main branch

## 📄 License

By contributing to ShabeAI CRM, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to ShabeAI CRM! 🎉 