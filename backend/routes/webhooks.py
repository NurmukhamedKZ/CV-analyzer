from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging
import json
from services.clerk_service import ClerkService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
clerk_service = ClerkService()

@router.post("/clerk")
async def handle_clerk_webhook(request: Request):
    """
    Handle Clerk webhook events
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        
        # Parse JSON
        try:
            event_data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook payload")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON payload"
            )
        
        event_type = event_data.get('type')
        
        if not event_type:
            logger.error("Missing event type in webhook")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing event type"
            )
        
        logger.info(f"Processing Clerk webhook: {event_type}")
        
        # Handle different event types
        if event_type == 'user.created':
            user = clerk_service.handle_user_created(event_data)
            if user:
                logger.info(f"User created successfully: {user.clerk_user_id}")
                return {"message": "User created successfully", "user_id": user.id}
            else:
                logger.error("Failed to create user from webhook")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )
        
        elif event_type == 'user.updated':
            user = clerk_service.handle_user_updated(event_data)
            if user:
                logger.info(f"User updated successfully: {user.clerk_user_id}")
                return {"message": "User updated successfully", "user_id": user.id}
            else:
                logger.error("Failed to update user from webhook")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user"
                )
        
        elif event_type == 'user.deleted':
            success = clerk_service.handle_user_deleted(event_data)
            if success:
                logger.info("User deleted successfully")
                return {"message": "User deleted successfully"}
            else:
                logger.error("Failed to delete user from webhook")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete user"
                )
        
        else:
            logger.info(f"Unhandled webhook event type: {event_type}")
            return {"message": f"Event type {event_type} received but not processed"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Clerk webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing webhook"
        )

@router.get("/health")
async def webhook_health():
    """
    Health check endpoint for webhooks
    """
    return {"status": "healthy", "service": "webhooks"}
