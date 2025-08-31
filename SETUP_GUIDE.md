# 🚀 AI CV Checker - Complete Setup Guide

This guide will help you set up and run both the **Next.js Frontend** and **FastAPI Backend** for the AI CV Checker application.

## 📋 Prerequisites

- **Node.js 18+** and **npm**
- **Python 3.8+** and **pip**
- **Git** (for cloning the repository)

## 🏗️ Project Structure

```
CVaiStartup/
├── app/                    # Next.js frontend (App Router)
├── components/             # React components
├── backend/                # FastAPI backend
│   ├── main.py            # FastAPI app entry point
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── models/             # Pydantic models
│   └── requirements.txt    # Python dependencies
├── package.json            # Frontend dependencies
└── README.md               # Project documentation
```

## 🚀 Quick Start (Both Services)

### Option 1: Automated Setup (Recommended)

1. **Make the backend startup script executable**:
   ```bash
   cd backend
   chmod +x start.sh
   ```

2. **Start the backend** (in one terminal):
   ```bash
   cd backend
   ./start.sh
   ```

3. **Start the frontend** (in another terminal):
   ```bash
   npm run dev
   ```

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env file with your OpenAI API key
   ```

5. **Start FastAPI server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend Setup

1. **Navigate to project root**:
   ```bash
   cd ..  # If you're in backend directory
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env.local
   # Edit .env.local file
   ```

4. **Start Next.js development server**:
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Backend Environment (.env)

Create `backend/.env` file:

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

### Frontend Environment (.env.local)

Create `.env.local` file in project root:

```bash
# Backend Configuration
BACKEND_URL=http://localhost:8000

# OpenAI Configuration (optional, backend handles this)
OPENAI_API_KEY=your_openai_api_key_here

# NextAuth Configuration (for future features)
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_here
```

## 🌐 Access URLs

### Frontend
- **Application**: http://localhost:3000
- **Home Page**: http://localhost:3000
- **Results Page**: http://localhost:3000/results
- **About Page**: http://localhost:3000/about
- **Pricing Page**: http://localhost:3000/pricing

### Backend
- **API Base**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Testing the Setup

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "message": "API is running"}
```

### 2. Test Frontend

Open http://localhost:3000 in your browser. You should see:
- ✅ Landing page with CV upload form
- ✅ Navigation menu
- ✅ Professional UI design

### 3. Test CV Analysis

1. **Upload a PDF CV** (drag & drop works!)
2. **Paste a job description** (e.g., "Software Engineer position")
3. **Click "Analyze CV with AI"**
4. **View results** - you'll get comprehensive feedback

## 🔑 OpenAI API Setup

### Get API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key

### Configure API Key

1. **Backend**: Add to `backend/.env`
   ```bash
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

2. **Frontend**: Add to `.env.local` (optional, backend handles this)
   ```bash
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## 🐛 Troubleshooting

### Backend Issues

#### Port Already in Use
```bash
# Change port in .env or use different port
uvicorn main:app --port 8001
```

#### Python Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Virtual Environment
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

#### Port Already in Use
```bash
# Use different port
npm run dev -- -p 3001
```

#### Dependencies
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Environment Variables
```bash
# Ensure .env.local exists and has correct values
cp env.example .env.local
# Edit .env.local with your configuration
```

### Common Issues

1. **CORS Errors**: Ensure backend CORS is configured for frontend URL
2. **File Upload Fails**: Check file type and size limits
3. **AI Analysis Fails**: Verify OpenAI API key and credits
4. **Connection Refused**: Ensure both services are running

## 📊 Monitoring & Logs

### Backend Logs
- Check terminal where backend is running
- Look for detailed logging information
- API requests and responses are logged

### Frontend Logs
- Check browser developer console
- Network tab shows API requests
- Check terminal where frontend is running

## 🚀 Production Deployment

### Backend Production

1. **Set production environment**:
   ```bash
   DEBUG=False
   JWT_SECRET_KEY=your-production-secret-key
   ```

2. **Use production server**:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Production

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm start
   ```

## 🔒 Security Notes

- **Change default JWT secret** in production
- **Use HTTPS** in production
- **Set proper CORS origins** for production domains
- **Secure OpenAI API key** - never commit to version control

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **OpenAI API Documentation**: https://platform.openai.com/docs
- **TailwindCSS Documentation**: https://tailwindcss.com/docs

## 🤝 Support

If you encounter issues:

1. **Check the logs** for both frontend and backend
2. **Verify environment variables** are set correctly
3. **Ensure both services** are running
4. **Check file permissions** for startup scripts
5. **Verify Python and Node.js versions** meet requirements

## 🎯 Next Steps

After successful setup:

1. **Test with real CVs** and job descriptions
2. **Customize the UI** to match your brand
3. **Add authentication** using the built-in auth system
4. **Deploy to production** when ready
5. **Add database integration** for persistent storage
6. **Implement rate limiting** and monitoring

---

**Happy coding! 🎉**

Your AI CV Checker is now ready to help users optimize their resumes and land their dream jobs!
