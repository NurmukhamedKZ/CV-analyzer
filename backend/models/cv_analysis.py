from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CVAnalysisRequest(BaseModel):
    """Request model for CV analysis"""
    job_description: str = Field(..., description="Job description to analyze against")
    user_id: Optional[str] = Field(None, description="User ID for tracking")

class KeywordMatch(BaseModel):
    """Model for keyword matching results"""
    matched: List[str] = Field(..., description="Keywords that match between CV and job description")
    missing: List[str] = Field(..., description="Keywords from job description missing in CV")
    score: int = Field(..., ge=0, le=100, description="Keyword match percentage")

class ATSCompatibility(BaseModel):
    """Model for ATS compatibility results"""
    score: int = Field(..., ge=0, le=100, description="ATS compatibility score")
    issues: List[str] = Field(..., description="ATS compatibility issues found")
    suggestions: List[str] = Field(..., description="Suggestions to improve ATS compatibility")

class CVAnalysisResponse(BaseModel):
    """Response model for CV analysis"""
    grammar_suggestions: List[str] = Field(..., description="Grammar and clarity improvement suggestions")
    keyword_match: KeywordMatch = Field(..., description="Keyword matching analysis")
    ats_compatibility: ATSCompatibility = Field(..., description="ATS compatibility analysis")
    improved_bullet_points: List[str] = Field(..., description="Improved bullet point examples")
    overall_score: int = Field(..., ge=0, le=100, description="Overall CV score")
    summary: str = Field(..., description="Summary of the analysis")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the analysis")

class AnalysisHistoryItem(BaseModel):
    """Model for analysis history items"""
    id: str = Field(..., description="Analysis ID")
    timestamp: datetime = Field(..., description="When the analysis was performed")
    filename: str = Field(..., description="Original CV filename")
    overall_score: int = Field(..., description="Overall score from the analysis")
    job_description: Optional[str] = Field(None, description="Job description used for analysis")

class AnalysisHistoryResponse(BaseModel):
    """Response model for analysis history"""
    user_id: str = Field(..., description="User ID")
    analyses: List[AnalysisHistoryItem] = Field(..., description="List of analyses")
    total: int = Field(..., description="Total number of analyses")

class DeleteAnalysisResponse(BaseModel):
    """Response model for deleting analysis"""
    message: str = Field(..., description="Success message")
    analysis_id: str = Field(..., description="ID of deleted analysis")
