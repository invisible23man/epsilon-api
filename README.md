# Epsilon API - FastAPI Backend

## Overview
Epsilon API is a **FastAPI-based backend** that provides **mental health trend analysis and AI-powered insights**.

## Installation
### 1️⃣ Clone Repository
```bash
git clone https://github.com/invisible23man/epsilon-api.git
cd epsilon-api
```

### 2️⃣ Install Dependencies using Poetry
```bash
poetry install
```

### 3️⃣ Run the FastAPI Server
```bash
poetry run uvicorn app.main:app --reload
```

## API Endpoints
- `GET /api/trends` → Fetch latest mental health trends
- `GET /api/insights` → Provide AI-based insights
- `POST /api/users/data` → Store user analytics

## Deployment with Docker
```bash
docker build -t epsilon-api .
docker run -p 8000:8000 --env-file .env epsilon-api
```

## Security Features
✅ **JWT-based authentication**
✅ **Rate limiting**
✅ **CORS protection**

## 4️⃣ Project Structure
```
/epsilon-api
├── app/
│   ├── main.py  # Entry point
│   ├── config.py  # Environment & settings
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── trends.py  # Trends data endpoint
│   │   │   │   ├── insights.py  # AI insights endpoint
│   │   │   │   ├── auth.py  # Authentication
│   ├── models/  # Database ORM models
│   ├── schemas/  # Pydantic models for request validation
│   ├── services/  # Business logic functions
│   ├── database.py  # Database connection
├── tests/  # Unit and integration tests
├── pyproject.toml  # Poetry dependency management
├── README.md  # Project documentation
├── .gitignore  # Ignored files for version control
├── Dockerfile  # Containerization
├── .env  # Environment variables
```