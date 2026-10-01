# MentorMatch AI

MentorMatch AI connects students with verified mentors using transparent, explainable matching. A student signs up, builds a profile, gets ranked mentor recommendations with clear reasons and skill gaps, and sends a mentorship request. The mentor accepts or declines, and the student is notified in the app.

```
Email sign-up → Onboarding → Matching → Request → Mentor accepts/declines → Status notification
```

> **Status:** MVP in progress. The backend is being rebuilt from a single-file prototype into a persisted, role-aware API. The frontend has not been started yet.

---

## Features (MVP)

- Email/password authentication via Supabase
- Role-based access: `student`, `mentor`, `admin`
- Student onboarding (profile, skills, goals)
- Admin-managed mentor directory with verification status
- Deterministic matching: weighted score, reasons, and skill gaps (no opaque "AI" score)
- Mentorship requests with duplicate-pending protection
- Mentor inbox with accept/decline decisions
- In-app notifications for status changes

**Deferred (not in MVP):** scheduling, messaging, file uploads, embeddings, calendar integration.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python) |
| Database | Supabase Postgres |
| ORM / migrations | SQLAlchemy + Alembic |
| Auth | Supabase Auth (JWT validated by FastAPI) |
| Frontend | To be built |

---

## Project Structure (target)

```
backend/
├── app/
│   ├── main.py            # App entry point, router registration
│   ├── core/
│   │   ├── config.py      # Settings loaded from environment
│   │   └── security.py    # JWT validation, get_current_user, require_role()
│   ├── db/
│   │   ├── session.py     # SQLAlchemy engine and session
│   │   └── models.py      # ORM models
│   ├── schemas/           # Pydantic request/response models
│   ├── routers/           # auth, students, mentors, matching, requests, notifications
│   └── services/
│       └── matching.py    # Pure, unit-testable matching logic
├── alembic/               # Migrations
├── tests/
├── .env.example
└── requirements.txt
frontend/                  # Not started
```

---

## Data Model

- `users`: id (Supabase auth user ID), email, role
- `student_profiles`
- `mentor_profiles`: skills, industry, experience, availability note, mentorship areas, verification status
- `skills`: normalized (lowercase, trimmed)
- profile-skill link tables
- `mentorship_requests`: student, mentor, status (`pending` / `accepted` / `declined`)
- `notifications`

Key database rules:

- A **partial unique index** on `(student_id, mentor_id) WHERE status = 'pending'` prevents duplicate pending requests.
- Decisions update with `WHERE status = 'pending'`, so a request can't be decided twice.
- The decision and its notification are created in the **same transaction**.

---

## API Overview

| Method | Endpoint | Role | Purpose |
|---|---|---|---|
| GET | `/api/auth/me` | any | Current user (creates the `users` row on first login) |
| GET/PUT | `/api/students/me` | student | View and update own profile |
| GET | `/api/mentors` | any | List verified mentors |
| GET | `/api/mentors/{id}` | any | Mentor detail |
| GET | `/api/matching/recommendations` | student | Ranked mentors with reasons and skill gaps |
| POST | `/api/mentorship-requests` | student | Create a request |
| GET | `/api/mentorship-requests` | student / mentor | Students see their own; mentors see requests addressed to them |
| POST | `/api/mentorship-requests/{id}/decision` | mentor | Accept or decline |
| GET | `/api/notifications` | any | List own notifications |

Admins create and verify mentors through the mentor endpoints (use Swagger UI at `/docs` for now).

Interactive API docs are available at `http://localhost:8000/docs` when the server is running.

---

## Matching

Matching is deterministic and explainable. Weights live in a single config dict (for example skills overlap, industry, availability), and each response returns:

- the total score
- each component's weighted contribution (the "reasons")
- the student's skill gaps relative to the mentor

Because the logic is a pure function, it can be unit tested without a database.

---

## Getting Started

### Prerequisites

- Python 3.11+
- A Supabase project (Postgres + Auth)

### Setup

```bash
git clone <your-repo-url>
cd <your-repo>/backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in the values
```

### Environment variables

Create `backend/.env` (see `.env.example`):

```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<pooler-host>:5432/postgres
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_JWT_SECRET=<only if your project uses HS256>
SUPABASE_JWKS_URL=<only if your project uses asymmetric keys>
CORS_ORIGINS=http://localhost:5173
```

Notes:

- Use the Supabase **session pooler** connection string. The direct connection is IPv6-only on some plans and fails on many networks.
- Check whether your Supabase project signs JWTs with HS256 (shared secret) or asymmetric keys (JWKS) and configure the matching variable.
- Never commit `.env`.

### Run migrations

```bash
alembic upgrade head
```

### Seed an admin

```bash
python -m scripts.seed_admin --email you@example.com
```

### Start the API

```bash
uvicorn app.main:app --reload
```

---

## Mentor Onboarding Flow

1. An admin creates a mentor profile with the mentor's **email**.
2. When someone signs up with that email, the backend links the profile to their account and assigns the `mentor` role.
3. The mentor logs in, sees their request inbox, and accepts or declines.

---

## Testing

```bash
pytest
```

Test plan highlights:

- Register, log in, log out; access only permitted routes per role
- Admin creates and verifies a mentor, who then appears in discovery
- Profile data produces ranked, explained recommendations
- One pending request per student/mentor pair; duplicates are rejected
- Mentors see only their own requests and can accept or decline once
- Students see the updated status and notification
- Validation errors, invalid mentor IDs, expired tokens, wrong-role access, and database failures

---

## Roadmap

- [ ] Repo cleanup (`.gitignore`, `.env.example`, remove tracked `venv`/`node_modules`)
- [ ] Project structure, config, DB session, models
- [ ] Alembic initial migration
- [ ] Auth dependency and role guards
- [ ] Profiles, mentor directory, admin mentor management
- [ ] Matching service and endpoint
- [ ] Requests and decisions
- [ ] Notifications
- [ ] Frontend (auth, onboarding, mentor directory, request status, mentor inbox)
- [ ] End-to-end smoke test

---

## Contributing

1. Create a feature branch from `main`.
2. Keep changes focused and add tests with new logic.
3. Open a pull request describing the change.

---

## License

TBD
