# Task Manager AI App

This project is a secure full-stack task manager application with authentication, protected user data, and an AI-powered assistant. Users can register, log in, create and manage tasks, organize work into categories, and ask the AI assistant for recommendations based on their stored content.

## Problem
Many people struggle to stay organized because they manage tasks across multiple areas of life without a simple system for planning, prioritizing, and reflecting on progress. This app helps users bring those tasks into one place and get guidance when they need it.

## Target User
Students, professionals, and anyone who wants a simple way to manage daily work and stay organized.

## Core Experience
- Sign up and sign in securely
- Create, edit, and delete tasks
- Organize tasks by category and priority
- Ask the AI assistant for help with planning and prioritization
- Keep a structured record of task-related information

## Current Implementation Notes
This repository includes the core full-stack foundation for that experience:
- React frontend with authentication and protected routes
- Flask backend with JWT-based authentication
- SQLAlchemy models and SQLite-backed storage
- AI/RAG-style endpoints for ingesting content and answering questions with retrieved context
- Login rate limiting and password reset support

## Project Links
- GitHub repository: https://github.com/somnathshindelab6/ProjectAuthenticatedFullStackAIApplication
- Deployed app: https://somnathshindelab6.github.io/ProjectAuthenticatedFullStackAIApplication/

## Local Setup
### Backend
1. Open the backend folder
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy .env.example to .env and update the values
5. Create the database and seed demo data:
   ```bash
   python create_db.py
   ```
6. Start the app:
   ```bash
   python app.py
   ```

### Frontend
1. Open the frontend folder
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the app:
   ```bash
   npm start
   ```

## Database
The app uses SQLite locally by default through DATABASE_URL. The seed script creates a demo user and sample categories, tasks, and documents.

## AI/RAG Workflow
The backend includes endpoints for ingesting content and asking questions using stored context. The workflow is designed to be source-backed and can be extended with richer task planning knowledge later.

## Deployment Notes
- Frontend is configured for GitHub Pages
- Backend can be deployed separately to Render, Railway, or Heroku
- Set production environment variables for secrets and API access

## Submission Summary
This repository includes:
- React frontend code
- Flask backend code
- SQL database setup and seed instructions
- AI/RAG workflow code
- .env example file
- Dependency files
- README documentation

