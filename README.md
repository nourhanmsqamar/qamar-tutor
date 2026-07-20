# 🌙 Qamar Tutor - Backend API

An AI-powered study assistant designed to help students learn efficiently from their own lecture notes and study materials using FastAPI, Groq API, and RAG (Retrieval-Augmented Generation).

---

## 🏗️ Architectural Overview & Clean Design

The project strictly follows a **Layered Architecture (Separation of Concerns)** to ensure high scalability and easy maintenance.

### Project Structure
```text
qamar-tutor/
├── alembic/              # Database migration environment & version tracks (Phase 3)
│   ├── versions/         # Automatic migration scripts (e.g., create_users_table)
│   └── env.py            # Alembic configuration and DB connection engine
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers and HTTP endpoints (The Waiter)
│   │   ├── core/         # Security configs, JWT, API keys, and environment settings
│   │   ├── models/       # Database schemas and tables (SQLAlchemy models)
│   │   ├── schemas/      # Pydantic data validation and serialization models (Phase 4)
│   │   ├── services/     # Core business logic and AI/RAG modules (The Kitchen/Chef)
│   │   └── main.py       # Main application entrypoint that initializes FastAPI
│   └── requirements.txt  # Project dependency manifest
├── alembic.ini           # Configuration file for Alembic migrations
├── qamar_tutor.db        # Local SQLite database instance (Phase 3)
├── .env                  # Secret environment variables (Excluded from Git)
└── .gitignore            # Git filter to ignore untracked files (__pycache__, envs, secrets)

```

*Note: Every directory inside `app/` contains an `__init__.py` file to explicitly define it as a structural Python package.*

---

## 🚀 Core Features Implemented

### 🤖 1. Advanced AI Assistant Integration (Session 4)

* **Groq API Infrastructure:** Seamlessly integrated the backend with Groq API to leverage ultra-fast, cutting-edge open-source Large Language Models.
* **Engineized Intelligence:** Configured **Meta's `llama-3.1-8b-instant**` as the core model to execute instantaneous and cost-effective responses.
* **Provider Abstraction:** Isolated all AI intelligence inside a dedicated service layer (`GeminiService`), making future model or provider swaps completely transparent to the API endpoints.
* **Dynamic Diagnostics:** Exposed a testing endpoint `POST /api/v1/ai/test` inside `ai_routes.py` to run continuous system health checks on text generation via Swagger UI.

### 📚 2. Context-Aware RAG Implementation (Session 5)

* **Data-Driven Context:** Developed the `ask_with_context` service method capable of ingesting raw extracted text from PDFs alongside user questions.
* **Strict Guardrails:** Programmed a highly optimized system prompt enforcing the model to rely *only* on the provided context, successfully eliminating AI hallucinations.
* **Dedicated RAG Gateway:** Created the `POST /api/v1/ai/ask-pdf` endpoint, forcing the assistant to act as a strict tutor that refuses to answer if information is missing from the academic material.

### 🔗 3. End-to-End RAG Pipeline Integration (Session 6)

* **Dynamic File Processing:** Engineered the `POST /api/v1/ai/ask-file` endpoint to accept simultaneous file uploads and text queries via `multipart/form-data`.
* **On-the-Fly Extraction:** Integrated the `PDFService` (using PyMuPDF) directly into the router logic to parse documents entirely in-memory without saving them to disk.
* **Full-Circle QA System:** Successfully connected the document parser with the Groq RAG engine, allowing users to upload a custom PDF and receive instant, context-grounded AI answers in a single API call.

### 🗄️ 4. Robust Database & Migration Management (Phase 3)

* **SQLAlchemy ORM:** Configured a resilient object-relational mapping layer utilizing scoped DB sessions and automated resource cleanup using Python's `yield` dependency injection.
* **SQLite Single-File Storage:** Provisioned a light-weight, highly-stable local database configuration to fast-track development and environment isolation.
* **Alembic Version Control:** Synchronized database state control allowing seamless metadata comparisons, generation of versioned blueprints, and smooth execution of DB state changes via CLI.

### 🔒 5. Enterprise-Grade Authentication & Security (Phase 4)

* **Cryptographic Hashing:** Employed `passlib` bundled with an isolated, secure version of `bcrypt` (`==4.0.1`) to strictly enforce industrial one-way hashing for secure password storage.
* **Stateless JWT Infrastructure:** Engineered a dynamic JSON Web Token minting system utilizing a cryptographically strong `SECRET_KEY` and `HS256` hashing to sign tamper-proof `Access Tokens` (30-minute lifespan).
* **Strict Pydantic Validation:** Enforced type-safe email schemas through `Pydantic[email]` ensuring all user payloads match defensive input criteria prior to hit any controller endpoint.

---

## 🛠️ Installation & Environment Setup

Follow these sequential steps to initialize the development environment and boot up the live server from scratch.

### 1. Prerequisites

Ensure you have [Anaconda / Miniconda](https://www.anaconda.com/) installed on your local machine.

### 2. Virtual Environment Management (Conda)

To isolate project dependencies, create and activate a dedicated Conda workspace:

```bash
# Create an isolated Python 3.11 environment
conda create --name qamar-env python=3.11 -y

# Activate the project environment
conda activate qamar-env

```

### 3. Dependency & Server Installation

Install the primary web framework, database components, security tools, and live server package inside the active environment:

```bash
# Install framework, AI tools, database utilities, and security libraries
pip install fastapi uvicorn groq python-dotenv sqlalchemy alembic passlib PyJWT "pydantic[email]" "bcrypt==4.0.1"

# Freeze dependencies into the manifest file
pip freeze > backend/requirements.txt

```

### 4. Configuration & Secrets Management

Create a `.env` file in the root directory of the project to securely house environment keys without hardcoding them into production source code:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
DATABASE_URL=sqlite:///./qamar_tutor.db
SECRET_KEY=9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

### 5. Running Database Migrations

Apply the migration schemas locally to create the required tables (`users`, etc.) inside the SQLite database instance:

```bash
# Apply migrations to the latest state (Head)
alembic upgrade head

```

### 6. Running the Live Server

Execute the asynchronous server using Uvicorn with automated code hot-reloading enabled:

```bash
uvicorn backend.app.main:app --reload

```

---

## 🌐 API Gateways & Verification Links

Once the terminal logs `Application startup complete`, open your browser to verify project status and run interactive end-to-end tests:

* **API Root Gateway (Health Check):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Interactive API Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Core Router Catalog (Endpoints View)

| Scope | Method | Endpoint | Description | Expected Payload |
| --- | --- | --- | --- | --- |
| **AI Engine** | `POST` | `/api/v1/ai/test` | Standard text generation diagnostic endpoint | `{"text": "string"}` |
| **AI Engine** | `POST` | `/api/v1/ai/ask-pdf` | Context-grounded RAG query processor (Raw text) | `{"question": "str", "context": "str"}` |
| **AI Engine** | `POST` | `/api/v1/ai/ask-file` | Live PDF upload parser + context grounded prompt | `multipart/form-data (File + Question)` |
| **Auth Gateway** | `POST` | `/auth/register` | Registers a unique user and hashes the password | `{"email": "str", "password": "str"}` |
| **Auth Gateway** | `POST` | `/auth/login` | Validates records and issues secure bearer JWTs | `{"email": "str", "password": "str"}` |

```
