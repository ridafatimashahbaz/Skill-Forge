import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.common.db import get_db, init_db
from services.common.models import User, Profile, Skill, Project, Certification, Role
from services.common.deps import get_current_claims, require_role

app = FastAPI(title="SkillForge Core Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
init_db()


def get_own_profile(user_id: str, db: Session) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# ---------- Schemas ----------

class ProfileUpdate(BaseModel):
    education: Optional[str] = None
    experience_level: Optional[str] = None
    career_goal: Optional[str] = None


class SkillIn(BaseModel):
    name: str
    proficiency: int = 1


class ProjectIn(BaseModel):
    title: str
    description: str = ""
    tech_stack: str = ""
    url: Optional[str] = None


class CertificationIn(BaseModel):
    name: str
    issuer: str = ""
    year: Optional[int] = None


# ---------- Health ----------

@app.get("/health")
def health():
    return {"status": "ok", "service": "core"}


# ---------- Profile ----------

@app.get("/profile/me")
def get_my_profile(claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    return serialize_profile(profile)


@app.put("/profile/me")
def update_my_profile(payload: ProfileUpdate, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    return serialize_profile(profile)


def serialize_profile(profile: Profile):
    return {
        "id": profile.id,
        "education": profile.education,
        "experience_level": profile.experience_level,
        "career_goal": profile.career_goal,
        "skills": [{"id": s.id, "name": s.name, "proficiency": s.proficiency} for s in profile.skills],
        "projects": [{"id": p.id, "title": p.title, "description": p.description,
                       "tech_stack": p.tech_stack, "url": p.url} for p in profile.projects],
        "certifications": [{"id": c.id, "name": c.name, "issuer": c.issuer, "year": c.year}
                            for c in profile.certifications],
    }


# ---------- Skills ----------

@app.post("/skills")
def add_skill(payload: SkillIn, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    skill = Skill(profile_id=profile.id, name=payload.name, proficiency=payload.proficiency)
    db.add(skill)
    db.commit()
    return {"id": skill.id, "name": skill.name, "proficiency": skill.proficiency}


@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: str, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.profile_id == profile.id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"deleted": skill_id}


# ---------- Projects ----------

@app.post("/projects")
def add_project(payload: ProjectIn, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    project = Project(profile_id=profile.id, **payload.dict())
    db.add(project)
    db.commit()
    return {"id": project.id, **payload.dict()}


@app.delete("/projects/{project_id}")
def delete_project(project_id: str, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    project = db.query(Project).filter(Project.id == project_id, Project.profile_id == profile.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"deleted": project_id}


# ---------- Certifications ----------

@app.post("/certifications")
def add_certification(payload: CertificationIn, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = get_own_profile(claims["sub"], db)
    cert = Certification(profile_id=profile.id, **payload.dict())
    db.add(cert)
    db.commit()
    return {"id": cert.id, **payload.dict()}


# ---------- Mentor / Admin views ----------

@app.get("/students")
def list_students(claims: dict = Depends(require_role("mentor", "admin")), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == Role.student).all()
    result = []
    for u in students:
        p = u.profile
        result.append({
            "user_id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "career_goal": p.career_goal if p else "",
            "experience_level": p.experience_level if p else "",
            "skill_count": len(p.skills) if p else 0,
        })
    return result


@app.get("/students/{user_id}")
def get_student(user_id: str, claims: dict = Depends(require_role("mentor", "admin")), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
    return serialize_profile(profile)


# Internal endpoint used by the AI/Analyzer services (server-to-server, still JWT-protected)
@app.get("/internal/profile/{user_id}")
def internal_get_profile(user_id: str, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return serialize_profile(profile)
