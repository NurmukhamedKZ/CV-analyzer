# 🐍 AI CV Checker - FastAPI Backend

A robust, scalable FastAPI backend for AI-powered CV analysis and optimization.

## ✨ Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **File Processing**: Support for PDF, DOCX, and DOC files
- **AI Integration**: OpenAI GPT-4 integration for intelligent CV analysis
- **Authentication**: JWT-based user authentication and authorization
- **File Validation**: Comprehensive file type and size validation
- **Async Processing**: Non-blocking file processing and AI analysis
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Error Handling**: Robust error handling with meaningful error messages

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── routes/                 # API route definitions
│   ├── cv_analysis.py     # CV analysis endpoints
│   └── auth.py            # Authentication endpoints
├── services/               # Business logic services
│   ├── cv_processor.py    # File processing service
│   ├── ai_analyzer.py     # AI analysis service
│   ├── file_validator.py  # File validation service
│   └── auth_service.py    # Authentication service
├── models/                 # Pydantic data models
│   ├── cv_analysis.py     # CV analysis models
│   └── auth.py            # Authentication models
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── start.sh               # Startup script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd backend
   ```

2. **Make the startup script executable**:
   ```bash
   chmod +x start.sh
   ```

3. **Run the startup script**:
   ```bash
   ./start.sh
   ```

   This script will:
   - Check Python version
   - Create virtual environment
   - Install dependencies
   - Create `.env` file from template
   - Start the FastAPI server

### Manual Setup

If you prefer manual setup:

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

4. **Start the server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Required Configuration

- **OPENAI_API_KEY**: Your OpenAI API key for AI-powered analysis
- **JWT_SECRET_KEY**: Secret key for JWT token signing (change in production)

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)
- **API Base URL**: http://localhost:8000

## 🔌 API Endpoints

### CV Analysis

- `POST /api/analyze-cv` - Analyze CV against job description
- `GET /api/analysis-history/{user_id}` - Get analysis history
- `DELETE /api/analysis/{analysis_id}` - Delete analysis

### Authentication

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/me` - Get current user
- `POST /api/refresh-token` - Refresh JWT token
- `POST /api/forgot-password` - Password reset request
- `POST /api/reset-password` - Reset password

## 🧪 Testing

### Test User

A test user is automatically created for development:

- **Email**: test@example.com
- **Password**: password123

### Testing with curl

```bash
# Test the API health
curl http://localhost:8000/health

# Test CV analysis (with mock data)
curl -X POST http://localhost:8000/api/analyze-cv \
  -F "cv=@test.pdf" \
  -F "job_description=Software Engineer position"

# Test authentication
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt password hashing
- **File Validation**: Comprehensive file type and size validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Sanitization**: File name sanitization and validation
- **Token Blacklisting**: Support for token invalidation

## 📁 File Processing

### Supported Formats

- **PDF**: Full text extraction using PyPDF2
- **DOCX**: Text extraction from paragraphs and tables
- **DOC**: Basic text extraction (limited support)

### File Validation

- **Size Limit**: 10MB maximum
- **Type Validation**: MIME type and extension validation
- **Content Validation**: Basic content structure validation

## 🤖 AI Integration

### OpenAI GPT-4

The backend integrates with OpenAI's GPT-4 model for intelligent CV analysis:

- **Grammar Suggestions**: Professional writing improvements
- **Keyword Matching**: Skills and requirements analysis
- **ATS Compatibility**: Applicant Tracking System optimization
- **Bullet Point Improvements**: Actionable enhancement suggestions
- **Overall Scoring**: Comprehensive CV assessment

### Fallback Mode

When OpenAI API is not available, the system provides intelligent mock analysis based on:
- Keyword matching between CV and job description
- Basic content validation
- Professional improvement suggestions

## 🚀 Production Deployment

### Environment Setup

1. **Set production environment variables**:
   ```bash
   DEBUG=False
   JWT_SECRET_KEY=your-production-secret-key
   OPENAI_API_KEY=your-production-openai-key
   ```

2. **Use production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in .env or use different port
   uvicorn main:app --port 8001
   ```

2. **OpenAI API errors**:
   - Check your API key in `.env`
   - Verify API key has sufficient credits
   - Check OpenAI service status

3. **File upload issues**:
   - Verify file type is supported
   - Check file size limits
   - Ensure proper MIME type detection

### Logs

Check the console output for detailed logging information. The backend provides comprehensive logging for:
- File processing operations
- AI analysis requests
- Authentication events
- Error conditions

## 🔮 Future Enhancements

- **Database Integration**: PostgreSQL/MongoDB for persistent storage
- **File Storage**: Cloud storage integration (AWS S3, Google Cloud)
- **Rate Limiting**: API rate limiting and usage tracking
- **Caching**: Redis caching for improved performance
- **Monitoring**: Prometheus metrics and health checks
- **Testing**: Comprehensive unit and integration tests
- **CI/CD**: Automated testing and deployment pipelines

## 📄 License

This project is part of the AI CV Checker application.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the logs for error details
- Ensure all environment variables are properly configured
