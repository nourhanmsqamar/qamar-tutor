# 🌙 Qamar Tutor - Backend API

An AI-powered study assistant designed to help students learn efficiently from their own lecture notes and study materials using FastAPI, Groq API, and RAG (Retrieval-Augmented Generation).

---

## 🏗️ Architectural Overview & Clean Design

The project strictly follows a **Layered Architecture (Separation of Concerns)** to ensure high scalability and easy maintenance.

### Project Structure
```text
qamar-tutor/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers and HTTP endpoints (The Waiter)
│   │   ├── core/         # Security configs, API keys, and environment settings
│   │   ├── models/       # Database schemas and tables (PostgreSQL models)
│   │   ├── services/     # Core business logic and AI/RAG modules (The Kitchen/Chef)
│   │   └── main.py       # Main application entrypoint that initializes FastAPI
│   └── requirements.txt  # Project dependency manifest
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

Install the primary web framework and live server package inside the active environment:

```bash
# Install framework dependencies
pip install fastapi uvicorn groq python-dotenv

# Freeze dependencies into the manifest file
pip freeze > backend/requirements.txt

```

### 4. Configuration & Secrets Management

Create a `.env` file in the root directory of the project to securely house environment keys without hardcoding them into production source code:

```env
GROQ_API_KEY=your_actual_groq_api_key_here

```

### 5. Running the Live Server

Execute the asynchronous server using Uvicorn with automated code hot-reloading enabled:

```bash
uvicorn backend.app.main:app --reload

```

---

## 🌐 API Gateways & Verification Links

Once the terminal logs `Application startup complete`, open your browser to verify project status and run interactive end-to-end tests:

* **API Root Gateway (Health Check):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* *Expected Response:* `{"status": "healthy", "project": "Qamar Tutor", "message": "Welcome to Qamar Tutor AI Backend!"}`


* **Interactive API Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* *Usage:* Access this UI to visually review request models, inject sample context/questions payloads, and dynamically test live API responses.



