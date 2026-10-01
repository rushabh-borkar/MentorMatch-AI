# MentorMatch AI — Windows Run Instructions

## Prerequisites
- Python 3.11+ recommended
- Node.js 20+ and npm

## 1. Start backend

Open CMD:

```cmd
cd ai_mentor_platform\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend: http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs

## 2. Start frontend

Open a second CMD:

```cmd
cd ai_mentor_platform\frontend
npm install
npm run dev
```

Open the URL Vite prints, normally:
http://localhost:5173

## 3. Demo flow
1. Open Home.
2. Click "Find my mentors".
3. Review explainable compatibility scores.
4. Click "Request mentorship" on a mentor.
5. Open "Career Roadmap".
6. Show the 8-week roadmap.
7. Explain the architecture: profile -> matching -> explainability -> request -> roadmap -> feedback.

## Notes
This is a self-contained MVP and does not require an API key.
The matching engine is deterministic and explainable so the demo works offline.
For a production version, replace/add embeddings or an LLM, authentication, a real database, verified alumni accounts, calendar/video integrations, and real analytics.
