from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging
import requests
import os
from datetime import datetime
from database.model import User, get_session
from services.clerk_service import ClerkService
from sqlmodel import select

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
clerk_service = ClerkService()

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "")
CLERK_API_BASE = "https://api.clerk.com/v1"

def verify_clerk_token(authorization: str = Header(None)) -> str:
    """Verify Clerk JWT token and return user ID"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Verify token with Clerk
        headers = {
            "Authorization": f"Bearer {CLERK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{CLERK_API_BASE}/tokens/verify",
            headers=headers,
            json={"token": token}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        token_data = response.json()
        return token_data.get("sub")  # Clerk user ID
        
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )

@router.get("/me")
async def get_current_user(clerk_user_id: str = Depends(verify_clerk_token)):
    """Get current user information"""
    try:
        user = clerk_service.get_user_by_clerk_id(clerk_user_id)
        
        if not user:
            # User doesn't exist in our database, sync from Clerk
            headers = {
                "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{CLERK_API_BASE}/users/{clerk_user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                clerk_user_data = response.json()
                user = clerk_service.sync_user_from_clerk(clerk_user_data)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        
        return {
            "id": user.id,
            "clerk_user_id": user.clerk_user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_image_url": user.profile_image_url,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )

@router.put("/me")
async def update_current_user(
    update_data: dict,
    clerk_user_id: str = Depends(verify_clerk_token)
):
    """Update current user information"""
    try:
        user = clerk_service.get_user_by_clerk_id(clerk_user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        with get_session() as session:
            # Update allowed fields
            allowed_fields = ["first_name", "last_name"]
            updated = False
            
            for field in allowed_fields:
                if field in update_data:
                    setattr(user, field, update_data[field])
                    updated = True
            
            if updated:
                user.updated_at = datetime.utcnow()
                session.add(user)
                session.commit()
                session.refresh(user)
        
        return {
            "id": user.id,
            "clerk_user_id": user.clerk_user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_image_url": user.profile_image_url,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user information"
        )

@router.get("/stats")
async def get_user_stats(clerk_user_id: str = Depends(verify_clerk_token)):
    """Get user statistics (CV uploads, analyses, etc.)"""
    try:
        user = clerk_service.get_user_by_clerk_id(clerk_user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        with get_session() as session:
            # Count user's CV uploads
            from database.model import CVFile, AnalysisResult
            
            cv_count = len(session.exec(
                select(CVFile).where(CVFile.user_id == user.id)
            ).all())
            
            analysis_count = len(session.exec(
                select(AnalysisResult).where(AnalysisResult.user_id == user.id)
            ).all())
        
        return {
            "user_id": user.id,
            "cv_uploads": cv_count,
            "analyses_completed": analysis_count,
            "member_since": user.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )

@router.delete("/me")
async def delete_current_user(clerk_user_id: str = Depends(verify_clerk_token)):
    """Deactivate current user account"""
    try:
        user = clerk_service.get_user_by_clerk_id(clerk_user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        with get_session() as session:
            user.is_active = False
            user.updated_at = datetime.utcnow()
            session.add(user)
            session.commit()
        
        return {"message": "User account deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating user account"
        )
