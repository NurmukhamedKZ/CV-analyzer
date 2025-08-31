from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import os
import tempfile
import shutil
from pathlib import Path
import logging
from datetime import datetime

# Import services
from services.cv_processor import CVProcessor
from services.ai_analyzer import AIAnalyzer
from services.file_validator import FileValidator

# Import models
from models.cv_analysis import CVAnalysisRequest, CVAnalysisResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
cv_processor = CVProcessor()
ai_analyzer = AIAnalyzer()
file_validator = FileValidator()

@router.post("/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...),
    user_id: Optional[str] = Form(None)
):
    """
    Analyze a CV against a job description using AI
    """
    try:
        logger.info(f"Starting CV analysis for file: {cv_file.filename}")
        
        # Validate file
        if not file_validator.is_valid_file(cv_file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only PDF, DOCX, and DOC files are allowed."
            )
        
        if not file_validator.is_valid_size(cv_file):
            raise HTTPException(
                status_code=400, 
                detail="File size too large. Maximum size is 10MB."
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(cv_file.filename).suffix) as temp_file:
            # Copy uploaded file to temp file
            shutil.copyfileobj(cv_file.file, temp_file)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from CV
            logger.info("Extracting text from CV file")
            cv_text = await cv_processor.extract_text(temp_file_path, cv_file.content_type)
            
            if not cv_text or not cv_text.strip():
                raise HTTPException(
                    status_code=400, 
                    detail="Could not extract text from the document. Please ensure it's a valid file."
                )
            
            # Analyze CV with AI
            logger.info("Starting AI analysis")
            analysis_result = await ai_analyzer.analyze_cv(cv_text, job_description)
            
            # Add metadata
            analysis_result["metadata"] = {
                "filename": cv_file.filename,
                "file_size": cv_file.size,
                "file_type": cv_file.content_type,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id
            }
            
            logger.info("CV analysis completed successfully")
            return analysis_result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during CV analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error during CV analysis: {str(e)}"
        )

@router.get("/analysis-history/{user_id}")
async def get_analysis_history(user_id: str, limit: int = 10):
    """
    Get analysis history for a user
    """
    try:
        # This would typically query a database
        # For now, return mock data
        return {
            "user_id": user_id,
            "analyses": [
                {
                    "id": "1",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "filename": "resume.pdf",
                    "overall_score": 75
                }
            ],
            "total": 1
        }
    except Exception as e:
        logger.error(f"Error getting analysis history: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error retrieving analysis history"
        )

@router.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str, user_id: str):
    """
    Delete a specific analysis
    """
    try:
        # This would typically delete from a database
        return {"message": f"Analysis {analysis_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Error deleting analysis"
        )
