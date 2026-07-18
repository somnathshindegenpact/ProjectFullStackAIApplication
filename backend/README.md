# Backend (Flask)


Quick-start for the provided Flask backend skeleton.

Requirements
- Python 3.10+

Project brief
- Developing a smart task management application that helps users organize and prioritize work with deadlines, categories, and progress tracking. AI will provide recommendations for task prioritization and time management to improve productivity.

Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and adjust the values. By default the app will use `sqlite:///dev.db`.

3. Create the database and seed demo data:

```bash
python create_db.py
```

4. Run the app for development:

```bash
python app.py
```

Database migrations (Flask-Migrate)

This project includes a small helper `manage.py` to run migration commands.

Examples:

```bash
# initialize migrations directory (only once)
python manage.py db-init

# autogenerate a migration from model changes
python manage.py db-migrate -m "add tasks table"

# apply migrations
python manage.py db-upgrade

# stamp current head without applying (useful for existing DB)
python manage.py db-stamp
```

API Endpoints

- `GET /api/health` — health check
- `POST /api/auth/register` — register (json: `email`, `password`)
- `POST /api/auth/login` — login (json: `email`, `password`)
- `POST /api/auth/refresh` — refresh (use refresh JWT)
- `GET /api/auth/me` — current user (requires access token)
- `POST /api/ai/ingest` — ingest a document (json: `title`, `content`, `source_url`)
- `POST /api/ai/search` — vector search (json: `query`, `top_k`)
- `POST /api/ai/ask` — AI/RAG ask (requires access token; json: `query`)

Notes
- This is a minimal scaffold for a capstone project. Replace the embedding storage and retrieval with Postgres+pgvector or an external vector DB for production RAG features. Do NOT commit secrets; use environment variables for keys.

Deployment notes
- Docker: A `Dockerfile` for backend and frontend plus `docker-compose.yml` are included for local integration testing. Run `docker-compose up --build` to start both services.
- Heroku: Use the `Procfile` in the root for deploying the backend. Set `DATABASE_URL` (Heroku Postgres) and `JWT_SECRET_KEY`, `FLASK_SECRET_KEY`, and `OPENAI_API_KEY` in Heroku config vars.
- Frontend: Consider deploying the frontend to Vercel or Netlify (build output in `frontend/build`). Point `REACT_APP_API_URL` to the deployed backend URL.

Security
- Never commit `.env` or secrets. Use the `.env.example` files to document required environment variables.


