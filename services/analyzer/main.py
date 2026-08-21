import sys, os, json, random
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Dict, List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.common.db import get_db, init_db
from services.common.models import Profile, Assessment, AssessmentQuestion, Roadmap, ASSESSMENT_AREAS
from services.common.deps import get_current_claims
from .analyzer import SkillAnalyzer, SkillGapCalculator, RoadmapGenerator, suggest_projects_for_gaps

app = FastAPI(title="SkillForge Analyzer Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
init_db()

analyzer = SkillAnalyzer()
gap_calculator = SkillGapCalculator()
roadmap_generator = RoadmapGenerator()


@app.get("/health")
def health():
    return {"status": "ok", "service": "analyzer"}


def get_own_profile(user_id: str, db: Session) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# ---------- Assessment ----------

@app.get("/assessment/questions")
def get_questions(area: Optional[str] = None, count: int = 5, db: Session = Depends(get_db)):
    q = db.query(AssessmentQuestion)
    if area:
        q = q.filter(AssessmentQuestion.area == area)
    questions = q.all()
    random.shuffle(questions)
    questions = questions[:count]
    return [
        {
            "id": item.id, "area": item.area, "question": item.question,
            "options": {"a": item.option_a, "b": item.option_b, "c": item.option_c, "d": item.option_d},
        }
        for item in questions
    ]


class AnswerIn(BaseModel):
    question_id: str
    selected_option: str


class AssessmentSubmit(BaseModel):
    area: str
    answers: List[AnswerIn]


@app.post("/assessment/submit")
def submit_assessment(payload: AssessmentSubmit, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)

    correct = 0
    for ans in payload.answers:
        q = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == ans.question_id).first()
        if q and q.correct_option == ans.selected_option:
            correct += 1

    score = analyzer.calculate_score(correct, len(payload.answers))

    assessment = Assessment(profile_id=profile.id, area=payload.area, score=score)
    db.add(assessment)
    db.commit()

    return {"area": payload.area, "score": score, "correct": correct, "total": len(payload.answers)}


@app.get("/assessment/scores")
def get_scores(claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    latest: Dict[str, float] = {}
    for a in sorted(profile.assessments, key=lambda x: x.taken_at):
        latest[a.area] = a.score
    return latest


# ---------- Gap analysis + roadmap ----------

class RoadmapRequest(BaseModel):
    target_role: str


def level_from_scores(scores: Dict[str, float]) -> str:
    if not scores:
        return "beginner"
    avg = sum(scores.values()) / len(scores)
    if avg >= 75:
        return "advanced"
    if avg >= 45:
        return "intermediate"
    return "beginner"


@app.post("/roadmap/generate")
def generate_roadmap(payload: RoadmapRequest, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)

    scores = {a: 0.0 for a in ASSESSMENT_AREAS}
    for a in profile.assessments:
        scores[a.area] = a.score

    gaps = gap_calculator.identify_gaps(scores, payload.target_role)
    current_level = level_from_scores(scores)
    projects = suggest_projects_for_gaps(gaps)

    # resources come from the AI service's knowledge base in production;
    # here we return topic names so the frontend/AI service can enrich them.
    resources = [{"topic": g["topic"], "lookup": True} for g in gaps]

    roadmap = roadmap_generator.generate(current_level, scores, gaps, payload.target_role, projects, resources)

    record = Roadmap(profile_id=profile.id, target_role=payload.target_role, content_json=json.dumps(roadmap))
    db.add(record)
    db.commit()

    return roadmap


@app.get("/roadmap/latest")
def latest_roadmap(claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    record = (
        db.query(Roadmap)
        .filter(Roadmap.profile_id == profile.id)
        .order_by(Roadmap.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="No roadmap generated yet")
    return json.loads(record.content_json)


# Internal endpoint for the AI agent to call directly (server-to-server)
@app.get("/internal/gap-analysis/{user_id}")
def internal_gap_analysis(user_id: str, target_role: str, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    scores = {a: 0.0 for a in ASSESSMENT_AREAS}
    for a in profile.assessments:
        scores[a.area] = a.score
    gaps = gap_calculator.identify_gaps(scores, target_role)
    return {"scores": scores, "gaps": gaps, "current_level": level_from_scores(scores)}
