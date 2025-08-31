from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=50, description="User first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="User last name")

class UserRegister(UserBase):
    """Model for user registration"""
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")
    confirm_password: str = Field(..., description="Password confirmation")

class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserResponse(UserBase):
    """Model for user response"""
    id: str = Field(..., description="User ID")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="When the user account was created")
    updated_at: Optional[datetime] = Field(None, description="When the user account was last updated")
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Model for token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: Optional[UserResponse] = Field(None, description="User information")

class PasswordReset(BaseModel):
    """Model for password reset"""
    email: EmailStr = Field(..., description="User email address")

class PasswordChange(BaseModel):
    """Model for password change"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
    confirm_new_password: str = Field(..., description="New password confirmation")

class UserUpdate(BaseModel):
    """Model for updating user information"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User last name")
    email: Optional[EmailStr] = Field(None, description="User email address")
