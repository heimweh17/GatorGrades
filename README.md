# Grade Track

A web app that visualizes student grade trends, distributions, and performance metrics across assignments and exams.  
Built with Flask, React (Vite), SQLite / PostgreSQL, and Docker Compose.

---

## Features

- Interactive dashboards for grade distributions and trends  
- Calculates average, median, standard deviation, and pass rate automatically  
- Upload your own CSV grade data and view instant analytics  
- Fully RESTful Flask API backend  
- React + Recharts frontend for smooth visualizations  
- Docker Compose support — easy to deploy anywhere  

---

## Tech Stack

| Layer | Technology |
| :---- | :---------- |
| Frontend | React + Vite + Axios + Recharts |
| Backend | Flask + SQLAlchemy + Flask-CORS |
| Database | SQLite (local) or PostgreSQL (Docker) |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
Grade-Track/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   │   └── api.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── DistributionChart.jsx
│   │   │   └── TrendsChart.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Setup & Run

### Option 1 — Run with Docker (Recommended)

1. Make sure Docker is installed
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Verify installation:
     ```bash
     docker --version
     docker compose version
     ```

2. Build and run:
   ```bash
   docker compose build
   docker compose up
   ```

   Then open:
   - Frontend → http://localhost:5173  
   - Backend API → http://localhost:8000/api  

   To stop:
   ```bash
   docker compose down
   ```

---

### Option 2 — Run locally (no Docker)

#### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
# or
source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
$env:DATABASE_URL = "sqlite:///gatorgrades.db"  # PowerShell
python app.py
```

Backend runs at: http://127.0.0.1:8000

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

---

## Sample CSV Format

You can upload CSVs like this:

```csv
course_code,course_title,term,assignment_title,max_score,student_external_id,student_name,score
COP3530,Data Structures & Algorithms,Fall 2025,HW1 - Linked Lists,100,1001,Emma Chen,95
COP3530,Data Structures & Algorithms,Fall 2025,Quiz 1 - Recursion,50,1002,Lucas Rivera,22
COP3530,Data Structures & Algorithms,Fall 2025,Final Exam,250,1005,Ethan Zhao,244
```

A full sample file (`grades-sample.csv`) is included.

---

## Example Output

Once you upload a CSV, the dashboard shows:
- Student count, Assignments, Average %, Median %, Std Dev %, Pass Rate %
- A grade distribution histogram
- A trend line chart of assignment averages

---

## Troubleshooting

| Problem | Possible Fix |
| :------- | :------------ |
| 500 Internal Server Error on `/api/courses` | Check backend logs: `docker compose logs -f backend` |
| Charts not showing | Ensure `/api/*` endpoints return data in browser |
| Port conflict | Stop other local servers on `5173` or `8000` |
| Flask errors about Postgres | Set `DATABASE_URL=sqlite:///gatorgrades.db` for local testing |

---

## Credits

Developed by Alex Liu (University of Florida, CS Class of 2028)  
Built as a personal full-stack data visualization project.

---

## Screenshot

Below is the current working dashboard view:

![dashboard](https://github.com/heimweh17/GatorGrades/blob/main/Screenshot%202025-10-27%20015509.png "")

