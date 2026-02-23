# 📋 Task Management System

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**A modern, containerized task management application with a RESTful API backend and intuitive Vue.js frontend**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Development](#-development)

</div>

---

## 📖 Overview

Task Management System is a full-stack web application designed for managing tasks efficiently. The system features a robust FastAPI backend with JWT authentication, comprehensive CRUD operations, and file upload capabilities, paired with a modern Vue.js 3 frontend that provides an intuitive user experience.

### Key Highlights

- ✅ **Production-Ready Architecture**: Clean separation of concerns with modular design
- ✅ **Containerized Deployment**: Fully dockerized for easy setup and deployment
- ✅ **Secure Authentication**: JWT-based token authentication with secure password hashing
- ✅ **File Management**: Secure file upload with type validation and organized storage
- ✅ **RESTful API**: Well-documented OpenAPI/Swagger specification
- ✅ **Modern Frontend**: Responsive UI built with Vue.js 3, Pinia, and Tailwind CSS

---

## ✨ Features

### Backend Features
- 🔐 **JWT Authentication**: Secure token-based authentication system
- 📝 **Complete CRUD Operations**: Create, Read, Update, Delete for tasks
- 👥 **User Management**: User registration and authentication
- 📎 **File Upload**: Secure file upload with MIME type validation
- 📊 **OpenAPI Documentation**: Interactive API documentation via Swagger UI
- 🗄️ **SQLite Database**: Lightweight, file-based database with SQLAlchemy ORM
- 🔒 **Security**: Password hashing with bcrypt, CORS configuration

### Frontend Features
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 🔄 **State Management**: Centralized state with Pinia
- 🧭 **Routing**: Client-side routing with Vue Router
- 📱 **Responsive Design**: Mobile-friendly interface
- 🔐 **Protected Routes**: Authentication-based route protection
- ⚡ **Fast Development**: Hot module replacement with Vite

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Vue.js 3      │ ◄─────► │   FastAPI       │
│   Frontend      │  HTTP   │   Backend       │
│   (Port 5173)   │         │   (Port 8000)   │
└─────────────────┘         └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │   SQLite DB     │
                            │   + Uploads     │
                            └─────────────────┘
```

### Project Structure

```
task-management-system/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   │   └── api_v1/
│   │   │       └── endpoints/ # Individual endpoint modules
│   │   │           ├── tasks.py      # Task CRUD operations
│   │   │           ├── users.py      # User management
│   │   │           ├── login.py     # Authentication
│   │   │           ├── upload.py    # File upload
│   │   │           └── attachments.py # File attachments
│   │   ├── core/              # Core configuration and security
│   │   │   ├── config.py      # Application settings
│   │   │   └── security.py    # JWT and password hashing
│   │   ├── crud/              # Database CRUD operations
│   │   ├── db/                # Database configuration
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── utils/             # Utility functions
│   ├── Dockerfile             # Backend container definition
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # Vue.js 3 frontend application
│   ├── src/
│   │   ├── api/              # API client configuration
│   │   ├── components/       # Vue components
│   │   ├── router/           # Vue Router configuration
│   │   ├── stores/           # Pinia stores
│   │   └── views/            # Page views
│   ├── Dockerfile            # Frontend container definition
│   └── package.json          # Node.js dependencies
│
├── docker-compose.yml        # Multi-container orchestration
└── README.md                 # This file
```

### Architecture Decisions

1. **FastAPI over Flask**: Chosen for its modern async support, automatic OpenAPI documentation, and excellent performance
2. **SQLite**: Selected for simplicity and portability, suitable for small to medium-scale applications
3. **Vue.js 3**: Modern reactive framework with excellent developer experience
4. **Docker Compose**: Enables consistent development and deployment environments
5. **JWT Authentication**: Stateless authentication suitable for RESTful APIs
6. **Pinia**: Modern state management solution for Vue.js 3
7. **Tailwind CSS**: Utility-first CSS framework for rapid UI development

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.109.0 | Modern Python web framework |
| **SQLAlchemy** | 2.0.25 | ORM for database operations |
| **SQLite** | - | Lightweight database |
| **Python-JOSE** | 3.3.0 | JWT token handling |
| **Passlib** | 1.7.4 | Password hashing (bcrypt) |
| **Pydantic** | 2.5.3 | Data validation and settings |
| **Uvicorn** | 0.27.0 | ASGI server |
| **Python-Multipart** | 0.0.6 | File upload handling |
| **Aiofiles** | 23.2.1 | Async file operations |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Vue.js** | 3.5.25 | Progressive JavaScript framework |
| **Vite** | 7.3.1 | Fast build tool and dev server |
| **Pinia** | 3.0.4 | State management |
| **Vue Router** | 5.0.2 | Client-side routing |
| **Axios** | 1.13.5 | HTTP client |
| **Tailwind CSS** | 4.1.18 | Utility-first CSS framework |

### DevOps
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)

*Optional for local development:*
- **Python** 3.11 or higher
- **Node.js** 20 or higher
- **npm** or **yarn**

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/george-mariamki/task-managment-system
cd task-management-system

# Start all services
# Note: By default, Docker Compose automatically loads the default environment variables 
# from the example files:
# - Backend: `.backend/.env.example`
# - Frontend: `.frontend/.env.example`

docker-compose up --build

# The application will be available at:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env.development file)

# OPTIONAL:
# If you want to experiment with custom environment variable values,
# first modify them inside `.env.example`,
# then run the following command to copy them into the development config:

cp .env.example .env.development

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables (create .env.development file)

# OPTIONAL:
# If you want to experiment with custom environment variable values,
# first modify them inside `.env.example`,
# then run the following command to copy them into the development config:

cp .env.example .env.development

# Run development server
npm run dev
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)

Create a `.env.development` file in the `backend/` directory:

```env
# Application
APP_ENV=development

PROJECT_NAME="Task Management System"
API_V1_STR="/api/v1"

SECRET_KEY="CHANGETHISINPRODUCTIONSUPERSECRETKEY"
ACCESS_TOKEN_EXPIRE_MINUTES=11520

SQLALCHEMY_DATABASE_URI="sqlite:///./sql_app.db"

CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]

UPLOAD_DIR="uploads"
UPLOAD_PUBLIC_PREFIX="/uploads"
UPLOAD_ALLOWED_EXTENSIONS=[".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".txt"]
UPLOAD_MAX_SIZE_MB=5
```

#### Frontend (.env)

Create a `.env.develoopment` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_BACKEND_ORIGIN=http://localhost:8000
VITE_UPLOAD_MAX_SIZE_MB=5
VITE_UPLOAD_ALLOWED_EXTS=[".jpg",".jpeg",".png",".gif",".pdf",".doc",".docx",".txt"]

```

---

## 📚 API Documentation

### Interactive Documentation

Once the backend is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs

### API Endpoints

#### Authentication
- `POST /api/v1/login/access-token` - User login (returns JWT token)
- `POST /api/v1/users` - Register new user
- `GET /api/v1/users/me` - returns current user

#### Tasks (Protected - Requires JWT)
- `GET /api/v1/tasks` - List all tasks for authenticated user
- `POST /api/v1/tasks` - Create a new task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

#### File Upload (Protected - Requires JWT)
- `POST /api/v1/upload` - Upload a file
- `GET /api/v1/attachments` - List all attachments for authenticated user
- `DELETE /api/v1/attachments/{id}` - Delete attachment

### Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## 💻 Development

### Running in Development Mode

With Docker Compose, the services automatically reload on code changes:

```bash
docker-compose build
docker-compose up
```

### Database Migrations

The database is automatically initialized on first startup. SQLite database files are stored in:
- Docker: `/app/sql_app.db_folder/sql_app.db` (persisted in volume)
- Local: `backend/sql_app.db_folder/sql_app.db`

### File Uploads

Uploaded files are stored in:
- Docker: `/app/uploads` (persisted in volume)
- Local: `backend/uploads/`


### Code Structure

- **Backend**: Follows FastAPI best practices with separation of concerns
  - Models: SQLAlchemy database models
  - Schemas: Pydantic models for request/response validation
  - CRUD: Database operation layer
  - API: Route handlers and business logic

- **Frontend**: Vue.js 3 Composition API with organized structure
  - Components: Reusable UI components
  - Views: Page-level components
  - Stores: Pinia state management
  - API: Centralized HTTP client configuration

---

## 🧪 Testing

### Manual Testing

1. **Register a new user** via the frontend or API
2. **Login** to receive a JWT token
3. **Create tasks** using the authenticated endpoints
4. **Upload files** with validation
5. **Test CRUD operations** for tasks

### API Testing

Use the Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

---

## 📝 License

This project is created as a demonstration project.

---

## 👤 Author

**George Mariamki**

- Project: [Task Management System](https://github.com/george-mariamki/task-managment-system)

---

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- Vue.js team for the progressive framework
- All open-source contributors whose packages made this project possible

---

<div align="center">

**Built with ❤️ using FastAPI and Vue.js 3**

⭐ Star this repo if you find it helpful!

</div>
