from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from datetime import datetime, timedelta
import os

# Import services and models
from services.auth_service import AuthService
from models.auth import UserLogin, UserRegister, UserResponse, TokenResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

# Initialize auth service
auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """
    Register a new user
    """
    try:
        logger.info(f"User registration attempt for email: {user_data.email}")
        
        # Check if user already exists
        if auth_service.user_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Create new user
        user = auth_service.create_user(user_data)
        logger.info(f"User registered successfully: {user.email}")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.post("/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin):
    """
    Authenticate user and return JWT token
    """
    try:
        logger.info(f"Login attempt for email: {user_credentials.email}")
        
        # Authenticate user
        user = auth_service.authenticate_user(user_credentials.email, user_credentials.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Generate JWT token
        token = auth_service.create_access_token(data={"sub": user.email})
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.post("/logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout user (invalidate token)
    """
    try:
        token = credentials.credentials
        auth_service.invalidate_token(token)
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during logout"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user information
    """
    try:
        token = credentials.credentials
        user = auth_service.get_current_user(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refresh JWT token
    """
    try:
        token = credentials.credentials
        new_token = auth_service.refresh_token(token)
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Send password reset email
    """
    try:
        # This would typically send a password reset email
        # For now, just return success message
        return {"message": f"Password reset instructions sent to {email}"}
        
    except Exception as e:
        logger.error(f"Error in forgot password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password reset request"
        )

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    """
    Reset password using reset token
    """
    try:
        # This would typically validate the reset token and update password
        # For now, just return success message
        return {"message": "Password reset successfully"}
        
    except Exception as e:
        logger.error(f"Error in password reset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error resetting password"
        )
