import uuid
import datetime
from sqlalchemy import (
    Column, String, Integer, Float, ForeignKey, DateTime, Text, Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from .db import Base


def gen_uuid():
    return str(uuid.uuid4())


class Role(str, enum.Enum):
    student = "student"
    mentor = "mentor"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.student)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False, foreign_keys="Profile.user_id")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), unique=True, nullable=False)
    education = Column(String, default="")
    experience_level = Column(String, default="beginner")  # beginner/intermediate/advanced
    career_goal = Column(String, default="")
    cv_filename = Column(String, nullable=True)
    mentor_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="profile", foreign_keys=[user_id])

    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="profile", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    profile_id = Column(UUID(as_uuid=False), ForeignKey("profiles.id"), nullable=False)
    name = Column(String, nullable=False)
    proficiency = Column(Integer, default=1)  # 1-5 self-rated

    profile = relationship("Profile", back_populates="skills")


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    profile_id = Column(UUID(as_uuid=False), ForeignKey("profiles.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    tech_stack = Column(String, default="")
    url = Column(String, nullable=True)

    profile = relationship("Profile", back_populates="projects")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    profile_id = Column(UUID(as_uuid=False), ForeignKey("profiles.id"), nullable=False)
    name = Column(String, nullable=False)
    issuer = Column(String, default="")
    year = Column(Integer, nullable=True)

    profile = relationship("Profile", back_populates="certifications")


ASSESSMENT_AREAS = ["python", "web_development", "git", "devops", "ai", "database"]


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    profile_id = Column(UUID(as_uuid=False), ForeignKey("profiles.id"), nullable=False)
    area = Column(String, nullable=False)
    score = Column(Float, nullable=False)  # 0-100
    taken_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="assessments")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    area = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)  # "a" | "b" | "c" | "d"
    difficulty = Column(Integer, default=1)  # 1-3


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    profile_id = Column(UUID(as_uuid=False), ForeignKey("profiles.id"), nullable=False)
    target_role = Column(String, nullable=False)
    content_json = Column(Text, nullable=False)  # serialized roadmap structure
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    url = Column(String, nullable=True)
    topic = Column(String, nullable=False)
    resource_type = Column(String, default="article")  # article/course/video/doc
    description = Column(Text, default="")
    created_by = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
