AI-Driven Project Automation & Submission Controller

An automated backend system that generates, manages, deploys, and submits coding projects using Generative AI and GitHub automation.
Designed to support multi-round, iterative development workflows with minimal manual intervention.

** Overview **

This project is a FastAPI-based service that accepts development tasks, uses AI to generate project code, publishes it to GitHub, deploys it via GitHub Pages, and submits results to an external evaluation system.

It is optimized for round-based project execution, where each round builds upon the previous one using stored context and repository state.

Architecture

The system is organized into two primary components:

Application Entry Point (app.py)
Initializes the FastAPI application
Registers task routes
Exposes health check endpoints

Task Controller (task_controller.py)
Core orchestration and business logic
Manages:
Multi-round task execution
AI prompt construction and responses
GitHub repository creation and updates
Deployment and submission workflows

Setup & Installation
Prerequisites
Python 3.8+
Git
GitHub Personal Access Token (PAT)

Environment Variables
Create a .env file in the project root:
```.env
GITHUB_TOKEN=your_github_personal_access_token_here
```

Required permissions:
Create repositories
Push commits
Enable and manage GitHub Pages

Dependencies
```bash
pip install fastapi uvicorn python-dotenv PyGithub httpx
```

Running the Application

Start the FastAPI server:
```bash
uvicorn app:app --reload
```
