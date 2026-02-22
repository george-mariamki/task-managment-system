# Task Management System (FastAPI + Vue 3) — Containerized CRUD App

This repository contains a small, containerized full‑stack application built for the Loopback practical assignment: a Python API (FastAPI) with CRUD, OpenAPI docs, token-based authentication, SQLite persistence, and validated file uploads, plus a Vue.js 3 frontend implementing CRUD operations.

## Features

- Backend: FastAPI REST API with CRUD operations, OpenAPI specification, JWT-based auth, and SQLite datastore.
- File upload: validation (allowed extensions + max size), stored in the project folder and served via static files.
- Frontend: Vue.js 3 UI with Create/Read/Update/Delete for tasks and attachment handling.
- Containerization: Dockerfiles for backend/frontend + `docker-compose.yml` for running the stack.

## Tech stack

- Backend: FastAPI, SQLAlchemy, SQLite, JWT (`/login/access-token`).
- Frontend: Vue 3 (Vite), Pinia, Vue Router, Axios (adds `Authorization: Bearer <token>` via interceptor).
- Containers: Docker, Docker Compose.

## Project structure

- `backend/`: FastAPI app (`app/main.py`), routers under `app/api/api_v1/`, DB models/schemas/crud, upload utilities.
- `frontend/`: Vue 3 app (Vite) with login/register/dashboard and task components.
- `docker-compose.yml`: runs both services and persists SQLite + uploads via named volumes.

## Quick start (Docker)

### Prerequisites
- Docker + Docker Compose installed.

### Run

```bash
docker compose up --build
Open
Frontend: http://localhost:5173

Backend health: http://localhost:8000/health

API base (default): http://localhost:8000/api/v1

OpenAPI (Swagger JSON): http://localhost:8000/api/v1/openapi.json

Local development (without Docker)
Backend
bash
cd backend
python -m venv .venv
# activate venv (Windows/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Frontend
bash
cd frontend
npm install
npm run dev
Configuration (.env)
Backend env
A sample file exists at: backend/.env.example.

Common variables:

APP_ENV

API_V1_STR (default: /api/v1)

SQLALCHEMY_DATABASE_URI (default: sqlite:///./sql_app.db)

Upload:

UPLOAD_DIR (default: uploads)

UPLOAD_PUBLIC_PREFIX (default: /uploads)

UPLOAD_ALLOWED_EXTENSIONS (example: .jpg,.jpeg,.png,.gif,.pdf,.doc,.docx,.txt)

UPLOAD_MAX_SIZE_BYTES (backend limit is configured for ~5MB)

Frontend env
A sample file exists at: frontend/.env.example.

Common variables:

VITE_API_BASE_URL (example: http://localhost:8000/api/v1) — used by Axios as the API base URL.

VITE_BACKEND_ORIGIN (example: http://localhost:8000) — used to build clickable URLs to uploaded files.

Upload UX:

VITE_UPLOAD_ALLOWED_EXTS (example: .jpg,.jpeg,.png,.gif,.pdf,.doc,.docx,.txt)

VITE_UPLOAD_MAX_SIZE_MB (keep it aligned with backend limit)

Note: docker-compose.yml sets VITE_API_URL for the frontend container; make sure your frontend code and env keys are aligned (the Axios client reads VITE_API_BASE_URL).

Authentication
Bearer token (JWT).

Token URL: ${API_V1_STR}/login/access-token (default: /api/v1/login/access-token).

API overview
Base path is API_V1_STR (default /api/v1).

Routers are mounted for:

login

users

tasks

upload

attachments

Typical endpoints used by the UI:

Tasks:

GET /api/v1/tasks

POST /api/v1/tasks

PUT /api/v1/tasks/{id}

DELETE /api/v1/tasks/{id}

Upload:

POST /api/v1/upload (multipart form field name: file)

Attachments:

DELETE /api/v1/attachments/{id}

File upload rules
Max size: enforced on the backend via UPLOAD_MAX_SIZE_BYTES and on the frontend via VITE_UPLOAD_MAX_SIZE_MB.

Allowed extensions: backend UPLOAD_ALLOWED_EXTENSIONS, frontend VITE_UPLOAD_ALLOWED_EXTS.

Serving: uploaded files are exposed under UPLOAD_PUBLIC_PREFIX (default /uploads).

Persistence
SQLite is used as datastore (configurable via SQLALCHEMY_DATABASE_URI).

With Docker Compose, uploads and the SQLite database are persisted via named volumes.

Notes for production
A /debug-settings endpoint exists for debugging and should be disabled/removed in production.
