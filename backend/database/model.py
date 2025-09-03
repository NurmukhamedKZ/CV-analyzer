from typing import Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import Column, JSON as SA_JSON
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cv_checker.db")
engine = create_engine(DATABASE_URL, echo=False)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(unique=True, index=True)  # Clerk's unique user ID
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    hashed_password: Optional[str] = None  # Keep for backward compatibility
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class CVFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    filename: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    file_content: Optional[str]
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class AnalysisResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    cv_id: Optional[int] = Field(default=None, foreign_key="cvfile.id")
    job_description: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(SA_JSON))
    overall_score: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


def init_db():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
