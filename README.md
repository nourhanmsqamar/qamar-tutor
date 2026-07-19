# Qamar Tutor - Backend API

An AI-powered study assistant that helps students learn from their own lecture notes and study materials using FastAPI, Gemini API, and RAG.

---

## 🚀 Environment Setup & Initialization Guide

This guide describes how to initialize the backend environment and run the web server from scratch.

### 1. Prerequisites
Make sure you have [Anaconda / Miniconda](https://www.anaconda.com/) installed on your machine.

### 2. Virtual Environment Management (Conda)
To keep dependencies isolated and avoid conflicts with the base environment, we use a dedicated Conda environment:

```bash
# Create a new isolated environment with Python 3.11
conda create --name qamar-env python=3.11 -y

# Activate the project environment
conda activate qamar-env

3. Dependency Management & Server Installation
# Step 4: Install FastAPI framework and Uvicorn server inside the active environment
pip install fastapi uvicorn

# Step 5: Freeze dependencies into requirements.txt to track exact versions
pip freeze > backend/requirements.txt

4. Running the Backend Server
# Step 6: Start the local live-reloading server from the root directory
uvicorn backend.app.main:app --reload


### 🌐 API Gateways & Verification Links
Once the server status displays Application startup complete, open your browser and verify the following endpoints:

API Root Gateway (Health Check): http://127.0.0.1:8000/

Expected Output: {"status": "healthy", "project": "Qamar Tutor", "message": "Welcome to Qamar Tutor AI Backend!"}

Interactive API Documentation (Swagger UI): http://127.0.0.1:8000/docs

Description: An interactive UI allowing frontend developers and engineers to test endpoints live.

----
### 🏗️ Clean Modular Architecture
The project follows strict separation of concerns to maintain code scalability:

qamar-tutor/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers and HTTP endpoints (The Waiter)
│   │   ├── core/         # Security configs, API keys, and environment settings
│   │   ├── models/       # Database schemas and tables (PostgreSQL models)
│   │   ├── services/     # Core business logic and AI/RAG modules (The Kitchen/Chef)
│   │   ├── main.py       # Main application entrypoint that initializes FastAPI
│   ├── requirements.txt  # Project dependency manifest
└── .gitignore            # Git filter to ignore untracked files like __pycache__ and secrets

#Note: All folders contain an __init__.py file to explicitly define them as Python packages.

