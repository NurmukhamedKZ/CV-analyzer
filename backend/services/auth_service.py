import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication and user management"""
    
    def __init__(self):
        # JWT configuration
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        
        # Password hashing
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # In-memory user storage (replace with database in production)
        self.users = {}
        self.blacklisted_tokens = set()
        
        # Initialize with a test user
        self._create_test_user()
    
    def _create_test_user(self):
        """Create a test user for development"""
        test_user = {
            "id": str(uuid.uuid4()),
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": self.pwd_context.hash("password123"),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        self.users[test_user["email"]] = test_user
        logger.info("Test user created: test@example.com / password123")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        try:
            return self.pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT access token"""
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            to_encode.update({"exp": expire})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Access token created for user: {data.get('sub', 'unknown')}")
            
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            # Check if token is blacklisted
            if token in self.blacklisted_tokens:
                logger.warning("Token is blacklisted")
                return None
            
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            
            if email is None:
                logger.warning("Token missing subject")
                return None
            
            return payload
            
        except JWTError as e:
            logger.error(f"JWT error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None
    
    def user_exists(self, email: str) -> bool:
        """Check if a user exists"""
        return email in self.users
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            # Check if passwords match
            if user_data.get("password") != user_data.get("confirm_password"):
                raise ValueError("Passwords do not match")
            
            # Create user object
            user = {
                "id": str(uuid.uuid4()),
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "hashed_password": self.get_password_hash(user_data["password"]),
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Store user
            self.users[user["email"]] = user
            
            # Return user without password
            user_response = {k: v for k, v in user.items() if k != "hashed_password"}
            logger.info(f"User created successfully: {user['email']}")
            
            return user_response
            
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with email and password"""
        try:
            user = self.users.get(email)
            if not user:
                logger.warning(f"Authentication failed: user not found - {email}")
                return None
            
            if not self.verify_password(password, user["hashed_password"]):
                logger.warning(f"Authentication failed: invalid password - {email}")
                return None
            
            if not user["is_active"]:
                logger.warning(f"Authentication failed: user inactive - {email}")
                return None
            
            # Return user without password
            user_response = {k: v for k, v in user.items() if k != "hashed_password"}
            logger.info(f"User authenticated successfully: {email}")
            
            return user_response
            
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return None
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from token"""
        try:
            payload = self.verify_token(token)
            if payload is None:
                return None
            
            email = payload.get("sub")
            if email is None:
                return None
            
            user = self.users.get(email)
            if user is None:
                return None
            
            # Return user without password
            user_response = {k: v for k, v in user.items() if k != "hashed_password"}
            return user_response
            
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            return None
    
    def invalidate_token(self, token: str) -> bool:
        """Add token to blacklist"""
        try:
            self.blacklisted_tokens.add(token)
            logger.info("Token blacklisted successfully")
            return True
        except Exception as e:
            logger.error(f"Error blacklisting token: {str(e)}")
            return False
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an access token"""
        try:
            payload = self.verify_token(token)
            if payload is None:
                return None
            
            # Create new token with same data
            new_token = self.create_access_token({"sub": payload.get("sub")})
            logger.info(f"Token refreshed for user: {payload.get('sub')}")
            
            return new_token
            
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return None
    
    def update_user(self, email: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user information"""
        try:
            user = self.users.get(email)
            if not user:
                return None
            
            # Update allowed fields
            allowed_fields = ["first_name", "last_name"]
            for field in allowed_fields:
                if field in update_data:
                    user[field] = update_data[field]
            
            user["updated_at"] = datetime.utcnow()
            
            # Return updated user without password
            user_response = {k: v for k, v in user.items() if k != "hashed_password"}
            logger.info(f"User updated successfully: {email}")
            
            return user_response
            
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return None
    
    def change_password(self, email: str, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            user = self.users.get(email)
            if not user:
                return False
            
            # Verify current password
            if not self.verify_password(current_password, user["hashed_password"]):
                logger.warning(f"Password change failed: invalid current password - {email}")
                return False
            
            # Update password
            user["hashed_password"] = self.get_password_hash(new_password)
            user["updated_at"] = datetime.utcnow()
            
            logger.info(f"Password changed successfully for user: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            return False
    
    def deactivate_user(self, email: str) -> bool:
        """Deactivate a user account"""
        try:
            user = self.users.get(email)
            if not user:
                return False
            
            user["is_active"] = False
            user["updated_at"] = datetime.utcnow()
            
            logger.info(f"User deactivated: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error deactivating user: {str(e)}")
            return False
