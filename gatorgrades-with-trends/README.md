# GatorGrades

Full-stack student performance dashboard (Flask + PostgreSQL + React).

## Quick Start (Docker Compose)
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend:  http://localhost:8000/api/health
- Postgres: localhost:5432 (pg/pg passwords in compose)

A small demo dataset is auto-seeded on first request.

## CSV Upload (MVP)
Endpoint: `POST /api/upload` (multipart/form-data, field: `file`)

**CSV columns (min):**
```
course_code,term,assignment_title,student_external_id,student_name,score,max_score
COP3530,Fall 2025,HW1,12345678,Alex,92,100
```
Additional optional: `course_title, graded_at, assignment_due`

## API (MVP)
- `GET /api/health` – health check
- `GET /api/courses` – list courses
- `GET /api/courses/:id/summary` – aggregates (avg/median/stddev/pass rate)
- `GET /api/courses/:id/distribution?assignmentId=` – histogram buckets (0–100%)

## Dev Notes
- Flask + SQLAlchemy; tables created on app start.
- Seed data lives in `models.seed_demo()`.
- React + Vite; proxy `/api` to backend in dev.
- Add tests, auth (JWT), and CI as easy extensions.

## Project Structure
```
gatorgrades/
  backend/
    app.py
    db.py
    models.py
    routes/
      api.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      App.jsx
      main.jsx
      components/
        DistributionChart.jsx
    package.json
    vite.config.js
    Dockerfile
  docker-compose.yml
  README.md
```


## Sample Data
Two copies included for convenience:
- `sample-data/grades-sample.csv`
- `grades-sample.csv`

## Tests
In a local (non-Docker) shell, you can run backend tests quickly with SQLite:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pytest -q
```


### Trends Endpoint
- `GET /api/courses/:id/trends` – average percentage per assignment ordered by due date (for line chart)

Front-end renders this as a line chart: one point per assignment (x = due date or title, y = avg %).
