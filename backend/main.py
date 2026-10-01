
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import math, re

app = FastAPI(title="MentorMatch AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

ALUMNI = [
    {
        "id": 1, "name": "Ananya Rao", "role": "AI/ML Engineer",
        "company": "NovaAI", "experience": 4,
        "skills": ["python","machine learning","deep learning","llm","generative ai","pytorch"],
        "industries": ["ai","software"], "interests": ["generative ai","llm","computer vision"],
        "bio": "Builds production AI systems and mentors students entering applied AI."
    },
    {
        "id": 2, "name": "Arjun Mehta", "role": "Software Engineer",
        "company": "CloudWorks", "experience": 5,
        "skills": ["java","python","backend","sql","system design","apis"],
        "industries": ["software","cloud"], "interests": ["backend","distributed systems","career growth"],
        "bio": "Software engineer focused on backend systems, interviews and career transitions."
    },
    {
        "id": 3, "name": "Priya Sharma", "role": "Data Scientist",
        "company": "FinData", "experience": 6,
        "skills": ["python","machine learning","statistics","pandas","sql","data science"],
        "industries": ["data","fintech"], "interests": ["analytics","machine learning","statistics"],
        "bio": "Data scientist who mentors students on ML fundamentals, portfolios and analytics."
    },
    {
        "id": 4, "name": "Rahul Verma", "role": "Product Engineer",
        "company": "BuildHub", "experience": 3,
        "skills": ["javascript","react","node","python","product development","apis"],
        "industries": ["software","startup"], "interests": ["full stack","startups","product"],
        "bio": "Product engineer helping students turn projects into deployable products."
    },
    {
        "id": 5, "name": "Sneha Iyer", "role": "ML Platform Engineer",
        "company": "DataForge", "experience": 7,
        "skills": ["python","mlops","docker","kubernetes","machine learning","cloud"],
        "industries": ["ai","cloud","software"], "interests": ["mlops","cloud","production ai"],
        "bio": "ML platform specialist focused on deploying and operating AI systems at scale."
    }
]

class Student(BaseModel):
    name: str
    branch: str = ""
    year: str = ""
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    career_goal: str = ""
    industry: str = ""
    experience: str = ""
    needs: List[str] = Field(default_factory=list)

class MentorRequest(BaseModel):
    student_name: str
    mentor_id: int
    message: str

def norm(s):
    return re.sub(r"[^a-z0-9+# ]", "", str(s).lower()).strip()

def tokens(items):
    out=set()
    for x in items:
        for part in re.split(r"[,/|]", norm(x)):
            if part.strip(): out.add(part.strip())
    return out

def match(student, mentor):
    ss = tokens(student.skills)
    si = tokens(student.interests)
    ms = tokens(mentor["skills"])
    mi = tokens(mentor["interests"])
    skill_overlap = len(ss & ms) / max(1, len(ss))
    interest_overlap = len(si & mi) / max(1, len(si))
    goal = norm(student.career_goal)
    role = norm(mentor["role"] + " " + " ".join(mentor["skills"]) + " " + " ".join(mentor["industries"]))
    goal_terms = set(goal.split())
    goal_overlap = len(goal_terms & set(role.split())) / max(1, len(goal_terms))
    industry = norm(student.industry)
    industry_score = 1 if industry and industry in [norm(x) for x in mentor["industries"]] else 0
    experience_score = min(1, mentor["experience"]/7)
    score = round(100*(0.35*skill_overlap + 0.25*interest_overlap + 0.20*goal_overlap + 0.15*industry_score + 0.05*experience_score))
    score = max(35, min(98, score))
    reasons=[]
    if skill_overlap >= .25: reasons.append("Strong skill overlap")
    if interest_overlap > 0: reasons.append("Aligned interests")
    if goal_overlap > 0: reasons.append("Relevant to your career goal")
    if industry_score: reasons.append("Same target industry")
    if not reasons: reasons.append("Relevant professional experience")
    gaps = sorted((ms-ss), key=len)[:4]
    return score, reasons, gaps

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.get("/api/alumni")
def alumni(): return ALUMNI

@app.post("/api/match")
def get_matches(student: Student):
    results=[]
    for mentor in ALUMNI:
        score,reasons,gaps=match(student, mentor)
        results.append({**mentor, "score":score, "reasons":reasons, "mentor_gaps":gaps})
    return sorted(results, key=lambda x:x["score"], reverse=True)

@app.post("/api/request")
def request_mentor(req: MentorRequest):
    mentor = next((x for x in ALUMNI if x["id"]==req.mentor_id), None)
    if not mentor: raise HTTPException(404, "Mentor not found")
    return {"status":"pending", "mentor":mentor["name"], "student":req.student_name}

@app.post("/api/roadmap")
def roadmap(student: Student):
    goal=student.career_goal or "your target career"
    return {
        "goal": goal,
        "weeks": [
            {"title":"Foundation", "duration":"Weeks 1–2", "tasks":["Audit current skills","Choose one focused learning track","Set a measurable weekly goal"]},
            {"title":"Build", "duration":"Weeks 3–5", "tasks":["Build one portfolio project","Use GitHub with clear documentation","Ask mentor for architecture/code feedback"]},
            {"title":"Prove", "duration":"Weeks 6–7", "tasks":["Deploy the project","Prepare a concise project walkthrough","Complete one mock interview"]},
            {"title":"Launch", "duration":"Week 8", "tasks":["Tailor resume to target roles","Improve LinkedIn/GitHub profile","Apply to relevant internships or jobs"]}
        ]
    }
