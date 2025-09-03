import logging
import os
from typing import Optional, Dict, Any
from datetime import datetime
from database.model import User, get_session
from sqlmodel import select
import json
import hmac
import hashlib

logger = logging.getLogger(__name__)

class ClerkService:
    """Service for handling Clerk webhooks and user synchronization"""
    
    def __init__(self):
        self.webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET", "")
        
    def verify_webhook(self, payload: bytes, signature: str) -> bool:
        """Verify Clerk webhook signature"""
        if not self.webhook_secret:
            logger.warning("CLERK_WEBHOOK_SECRET not set, skipping verification")
            return True
            
        try:
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            # Clerk sends signature as "v1,{hash}"
            signature_hash = signature.split(',')[1] if ',' in signature else signature
            
            return hmac.compare_digest(expected_signature, signature_hash)
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False
    
    def handle_user_created(self, event_data: Dict[str, Any]) -> Optional[User]:
        """Handle user.created webhook event"""
        try:
            user_data = event_data.get('data', {})
            
            # Extract user information from Clerk event
            clerk_user_id = user_data.get('id')
            email_addresses = user_data.get('email_addresses', [])
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            profile_image_url = user_data.get('profile_image_url')
            
            if not clerk_user_id or not email_addresses:
                logger.error("Missing required user data in webhook")
                return None
            
            # Get primary email
            primary_email = None
            for email in email_addresses:
                if email.get('id') == user_data.get('primary_email_address_id'):
                    primary_email = email.get('email_address')
                    break
            
            if not primary_email and email_addresses:
                primary_email = email_addresses[0].get('email_address')
            
            if not primary_email:
                logger.error("No email address found in user data")
                return None
            
            # Create user in database
            with get_session() as session:
                # Check if user already exists
                existing_user = session.exec(
                    select(User).where(User.clerk_user_id == clerk_user_id)
                ).first()
                
                if existing_user:
                    logger.info(f"User already exists: {clerk_user_id}")
                    return existing_user
                
                # Create new user
                new_user = User(
                    clerk_user_id=clerk_user_id,
                    email=primary_email,
                    first_name=first_name,
                    last_name=last_name,
                    profile_image_url=profile_image_url,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                
                logger.info(f"Created new user: {clerk_user_id} ({primary_email})")
                return new_user
                
        except Exception as e:
            logger.error(f"Error handling user.created event: {str(e)}")
            return None
    
    def handle_user_updated(self, event_data: Dict[str, Any]) -> Optional[User]:
        """Handle user.updated webhook event"""
        try:
            user_data = event_data.get('data', {})
            clerk_user_id = user_data.get('id')
            
            if not clerk_user_id:
                logger.error("Missing user ID in webhook")
                return None
            
            with get_session() as session:
                # Find existing user
                user = session.exec(
                    select(User).where(User.clerk_user_id == clerk_user_id)
                ).first()
                
                if not user:
                    logger.warning(f"User not found for update: {clerk_user_id}")
                    return None
                
                # Update user information
                email_addresses = user_data.get('email_addresses', [])
                if email_addresses:
                    # Get primary email
                    primary_email = None
                    for email in email_addresses:
                        if email.get('id') == user_data.get('primary_email_address_id'):
                            primary_email = email.get('email_address')
                            break
                    
                    if primary_email:
                        user.email = primary_email
                
                user.first_name = user_data.get('first_name')
                user.last_name = user_data.get('last_name')
                user.profile_image_url = user_data.get('profile_image_url')
                user.updated_at = datetime.utcnow()
                
                session.add(user)
                session.commit()
                session.refresh(user)
                
                logger.info(f"Updated user: {clerk_user_id}")
                return user
                
        except Exception as e:
            logger.error(f"Error handling user.updated event: {str(e)}")
            return None
    
    def handle_user_deleted(self, event_data: Dict[str, Any]) -> bool:
        """Handle user.deleted webhook event"""
        try:
            user_data = event_data.get('data', {})
            clerk_user_id = user_data.get('id')
            
            if not clerk_user_id:
                logger.error("Missing user ID in webhook")
                return False
            
            with get_session() as session:
                # Find and deactivate user (soft delete)
                user = session.exec(
                    select(User).where(User.clerk_user_id == clerk_user_id)
                ).first()
                
                if not user:
                    logger.warning(f"User not found for deletion: {clerk_user_id}")
                    return False
                
                user.is_active = False
                user.updated_at = datetime.utcnow()
                
                session.add(user)
                session.commit()
                
                logger.info(f"Deactivated user: {clerk_user_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error handling user.deleted event: {str(e)}")
            return False
    
    def get_user_by_clerk_id(self, clerk_user_id: str) -> Optional[User]:
        """Get user by Clerk user ID"""
        try:
            with get_session() as session:
                user = session.exec(
                    select(User).where(User.clerk_user_id == clerk_user_id)
                ).first()
                return user
        except Exception as e:
            logger.error(f"Error getting user by Clerk ID: {str(e)}")
            return None
    
    def sync_user_from_clerk(self, clerk_user_data: Dict[str, Any]) -> Optional[User]:
        """Sync user data from Clerk API"""
        try:
            clerk_user_id = clerk_user_data.get('id')
            if not clerk_user_id:
                return None
            
            with get_session() as session:
                # Check if user exists
                user = session.exec(
                    select(User).where(User.clerk_user_id == clerk_user_id)
                ).first()
                
                email_addresses = clerk_user_data.get('email_addresses', [])
                primary_email = None
                
                if email_addresses:
                    for email in email_addresses:
                        if email.get('id') == clerk_user_data.get('primary_email_address_id'):
                            primary_email = email.get('email_address')
                            break
                    
                    if not primary_email:
                        primary_email = email_addresses[0].get('email_address')
                
                if user:
                    # Update existing user
                    if primary_email:
                        user.email = primary_email
                    user.first_name = clerk_user_data.get('first_name')
                    user.last_name = clerk_user_data.get('last_name')
                    user.profile_image_url = clerk_user_data.get('profile_image_url')
                    user.updated_at = datetime.utcnow()
                else:
                    # Create new user
                    if not primary_email:
                        logger.error("No email address found for user sync")
                        return None
                    
                    user = User(
                        clerk_user_id=clerk_user_id,
                        email=primary_email,
                        first_name=clerk_user_data.get('first_name'),
                        last_name=clerk_user_data.get('last_name'),
                        profile_image_url=clerk_user_data.get('profile_image_url'),
                        is_active=True,
                        created_at=datetime.utcnow()
                    )
                
                session.add(user)
                session.commit()
                session.refresh(user)
                
                return user
                
        except Exception as e:
            logger.error(f"Error syncing user from Clerk: {str(e)}")
            return None
