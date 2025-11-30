# Dog Management App

A comprehensive, self-hosted web application for managing multiple dogs, including health records, training logs, walks (with GPX), care routines, and equipment.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (Async), PostgreSQL.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, TanStack Query.
- **Infrastructure**: Docker & Docker Compose.

## Features

- **Multi-user Support**: Isolated data per user.
- **Dog Profiles**: Detailed info, avatars, diet/health notes.
- **Health Tracking**: Vet visits, vaccinations, invoice uploads.
- **Training**: Goals, behavior issues, session logs (markdown + video links).
- **Walks**: GPS tracking (GPX upload & visualization), notes, mood.
- **Care Routine**: Recurring task tracking (daily/weekly/monthly) with reminders.
- **Equipment**: Gear inventory.
- **Activity Feed**: Unified timeline of all events.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd dog-app
   ```

2. **Environment Setup**
   The `docker-compose.yml` comes with default development credentials.
   - DB User: `dogapp`
   - DB Password: `dogapp_password`
   - Secret Key: `supersecretkeychangedinproduction`

   For production, modify `docker-compose.yml` or use an `.env` file.

3. **Start the Application**
   ```bash
   docker compose up -d --build
   ```
   This starts:
   - Postgres DB (port 5432)
   - Backend API (port 8000)
   - Frontend App (port 3000)

4. **Access the App**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Initial Setup**
   - Register a new user at `http://localhost:3000/register`.
   - Log in and start adding dogs!

### Database Migrations

The backend attempts to run migrations automatically on startup (via `uvicorn` startup script if configured, or manually).
If tables are missing, run:

```bash
docker compose exec backend alembic upgrade head
```

(Note: The initial migration script `001_initial_schema.py` is included).

## Development

- **Backend**: Located in `/backend`.
  - Install deps: `pip install -r requirements.txt`
  - Run locally: `uvicorn app.main:app --reload`
- **Frontend**: Located in `/frontend`.
  - Install deps: `npm install`
  - Run locally: `npm run dev`

