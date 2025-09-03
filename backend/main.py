from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import uvicorn

from dotenv import load_dotenv
from database.model import init_db
import os
import signal

# Import routers
from routes.cv_analysis import router as cv_router
from routes.auth import router as auth_router
from routes.webhooks import router as webhook_router
from routes.users import router as users_router

# Load environment variables
load_dotenv()

# Initialize database (create tables)
init_db()

# Create FastAPI app
app = FastAPI(
    title="AI CV Checker API",
    description="Backend API for AI-powered CV analysis and optimization",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cv_router, prefix="/api", tags=["CV Analysis"])
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(webhook_router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "AI CV Checker API is running!", "status": "healthy"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy and working", "message": "API is running"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )


@app.get("/shutdown")
async def shutdown_server():
    # Get the PID of the current process (which is the Uvicorn server)
    pid = os.getpid()
    # Send a SIGINT signal to gracefully shut down
    os.kill(pid, signal.SIGINT)
    return {"message": "Server is shutting down..."}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
