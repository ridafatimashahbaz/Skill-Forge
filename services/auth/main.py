import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from services.common.db import get_db, init_db
from services.common.models import User, Profile, Role
from services.common.security import hash_password, verify_password, create_access_token
from services.common.deps import get_current_claims

app = FastAPI(title="SkillForge Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Role = Role.student


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/signup", response_model=TokenResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.flush()

    profile = Profile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, user.role.value, user.email)
    return TokenResponse(access_token=token, role=user.role.value, user_id=user.id)


@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.role.value, user.email)
    return TokenResponse(access_token=token, role=user.role.value, user_id=user.id)


@app.get("/me")
def me(claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == claims["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value,
    }
