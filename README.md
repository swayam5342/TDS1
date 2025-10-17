🤖 AI-Driven Project Automation & Submission Controller

This repository contains the core logic for an automated system designed to generate, manage, and submit coding projects, primarily targeting multi-round development tasks. It uses Generative AI to create project files and leverages the GitHub API for version control, hosting, and continuous submission.

🚀 Overview

The system operates as a FastAPI service that accepts development tasks. It is structured into two main components:

The Application Entry Point (app.py): Configures the FastAPI application, includes the task router, and provides basic health checks.

The Task Controller (task_controller.py): Contains the core business logic for executing multi-round tasks, communicating with Generative AI models, and managing GitHub interactions.

⚙️ Setup and Installation

Prerequisites

Python 3.8+

Git

A GitHub Personal Access Token (PAT)

1. Environment Variables

Create a .env file in the root directory and configure your GitHub Personal Access Token. This token must have permissions to create repositories, push commits, and manage GitHub Pages.

GITHUB_TOKEN="your_github_personal_access_token_here"


2. Dependencies

Install the required Python packages (assuming the dependencies used in the controller, such as fastapi, python-dotenv, PyGithub, and httpx):

pip install fastapi uvicorn python-dotenv PyGithub httpx
# You may also need utility packages for AI and attachment processing (not listed here)


3. Running the Application

Start the FastAPI server using Uvicorn:

uvicorn app:app --reload


The application will be accessible at http://127.0.0.1:8000. You can check its status at the health endpoint: http://127.0.0.1:8000/health.

🧠 Core Logic: Task Controller

The task_controller manages the lifecycle of a development task across multiple rounds. It relies heavily on utility functions for interacting with AI and GitHub.

Round 1: Project Creation (task_1_controller)

This round handles the initial development based on a brief and specific checks.

Prompt Generation: The system constructs a detailed prompt using the task brief, checks, and any attached files.

AI Generation: The Generative AI model creates the initial project files (e.g., index.html, main.py, etc.).

GitHub Setup:

A new public repository is created (named after the task).

The generated files are uploaded in the initial commit.

GitHub Pages is enabled to host the project online.

Submission: The repository details (repo URL, commit SHA, Pages URL) are sent to the external evaluation endpoint.

Resilience: An exponential backoff retry mechanism is used for the AI generation, GitHub operations, and the final submission to ensure robustness against transient errors.

Round 2: Project Modification (task_2_controller)

This round handles iterative changes based on new requirements or feedback.

Context Retrieval:

The existing repository is retrieved.

The list of files currently in the repo is fetched.

The content of the internal tracking file (round_1.txt, which stores the initial prompt context) is retrieved.

Modification Prompt: A prompt is crafted that includes the new brief/checks, the list of existing files, and the context from Round 1.

AI Modification: The AI model generates updated files or new files based on the modification prompt.

GitHub Update: The updated/new files are committed to the existing repository.

Submission: The new commit SHA and Pages URL are sent to the evaluation endpoint.
