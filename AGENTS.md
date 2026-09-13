## RULES — Agent MUST follow:
1. Post IMPLEMENTATION PLAN first → WAIT for approval
2. Run build + test after every change
3. All tests PASS before marking complete
4. Never modify: /legacy, /vendor, /config/secrets
5. Open DRAFT PR — never ready-for-review automatically
6. Follow conventions in .github/copilot-instructions.md
# ZyntroAI Project — AI Agent Rules & Workflow

## 🎯 YOU MUST FOLLOW THESE RULES ON EVERY TASK

### ⚙️ Build & Test Commands
- **Install**: `uv sync --dev`
- **Build**: Not applicable (Python)
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Type Check**: `uv run mypy app/ --strict`
- **Test**: `uv run pytest --cov=app --cov-fail-under=80`
- **Security**: `uv run bandit -r app/ -ll`
- **All Checks**: `uvx pre-commit run --all-files`

### ✅ Workflow Rules
1. **PLAN FIRST**: Always post an **Implementation Plan** and wait for ✅ approval before writing any code
2. **TESTS REQUIRED**: Every new feature/bugfix must include tests that pass
3. **ALL CHECKS GREEN**: Run all quality gates (lint, format, types, tests, security) before opening PR
4. **DRAFT PR ONLY**: Always open **DRAFT** pull requests, never ready-for-review
5. **BRANCH NAMING**: Use format: `feat/short-description`, `fix/short-description`, `docs/short-description`
6. **COMMIT MESSAGES**: Use conventional commits (feat:, fix:, docs:, etc.)

### 🚫 NEVER DO
- ❌ Modify files in: `/legacy`, `/vendor`, `/node_modules`, `.env*`, `*.lock`
- ❌ Commit secrets, API keys, or credentials
- ❌ Bypass pre-commit hooks
- ❌ Push directly to `main` branch
- ❌ Delete existing tests without replacement
- ❌ Use `any` type or `# type: ignore` without justification

### 📁 File Conventions
- **Python**: Use `snake_case` for variables/functions, `PascalCase` for classes
- **FastAPI**: Use `APIRouter` for endpoints, `Pydantic` models for schemas
- **Tests**: Mirror app structure in `tests/` directory
- **Imports**: Group as: stdlib, third-party, local (with blank lines between)

### 🎨 Code Style
- Line length: 88 characters (Ruff default)
- Use f-strings, not .format() or %
- Use `async/await` for all I/O operations
- Type hints required on all public functions
- Docstrings required on all modules/classes/public functions

### 🔒 Security
- Never log sensitive data
- Validate all inputs with Pydantic
- Use environment variables for secrets
- Sanitize outputs to prevent injection

### 📊 Quality Gates
Your PR must pass ALL of these before human review:
- ✅ `ruff check .` (linting)
- ✅ `ruff format --check .` (formatting)
- ✅ `mypy app/ --strict` (type checking)
- ✅ `pytest --cov=app --cov-fail-under=80` (tests with 80%+ coverage)
- ✅ `bandit -r app/ -ll` (security scanning)

### 📝 PR Requirements
Every PR must include:
- Clear description of changes
- Screenshot/GIF if UI changes
- Test results summary
- Breaking changes noted (if any)
- Linked issues with `Closes #123` or `Fixes #456`

### 🎯 Project Standards
- **Framework**: FastAPI
- **Async**: Use `asyncio` and `anyio` where appropriate
- **Database**: SQLAlchemy/Async SQLAlchemy (if applicable)
- **Validation**: Pydantic v2
- **Testing**: pytest with pytest-asyncio
- **HTTP Client**: httpx
- **Package Manager**: uv
- **Formatting**: Ruff
- **Linting**: Ruff
- **Type Checking**: mypy --strict
- **Security**: Bandit

---

## 📄 **2. .github/copilot-instructions.md**

```markdown
# ZyntroAI FastAPI Project — Copilot Instructions

## 🏗️ Project Architecture

This is a **production-ready FastAPI boilerplate** with:
- Versioned API endpoints (`/api/v1/`)
- Pydantic v2 models for request/response validation
- SQLAlchemy ORM (async-capable)
- Dependency injection pattern
- Structured logging
- Comprehensive error handling
- Health check endpoint (`/api/v1/health`)

## 📦 Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | Latest |
| Language | Python | 3.12+ |
| Package Manager | uv | Latest |
| HTTP Client | httpx | Latest |
| Validation | Pydantic | v2 |
| Testing | pytest | Latest |
| Async Testing | pytest-asyncio | Latest |
| Linting | Ruff | Latest |
| Formatting | Ruff | Latest |
| Type Checking | mypy | Latest |
| Security | Bandit | Latest |
| Coverage | pytest-cov | Latest |

## 🚀 Development

### Environment Setup
```bash
# Clone repository
git clone https://github.com/zyntromedia/ZyntroAI-Project.git
cd ZyntroAI-Project

# Copy environment template
cp .env.example .env

# Edit .env with your values (especially SECRET_KEY)
nano .env  # or use your preferred editor

# Install all dependencies (dev + prod)
uv sync --dev

# Enable pre-commit hooks (run once)
uv tool install pre-commit
uvx pre-commit install
