# AI CV Checker - Demo Guide

## 🚀 Quick Start Demo

### 1. Prerequisites
- Node.js 18+ installed
- OpenAI API key (for AI analysis functionality)

### 2. Setup
```bash
# Clone and navigate to project
cd ai-cv-checker

# Install dependencies
npm install

# Copy environment file
cp env.example .env.local

# Edit .env.local and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🧪 Testing the Application

### Test 1: Basic UI Navigation
- ✅ Homepage loads with hero section
- ✅ Navigation menu works (Home, About, Pricing)
- ✅ CV upload form is displayed
- ✅ Responsive design on mobile/desktop

### Test 2: File Upload
- ✅ Drag and drop CV files
- ✅ File type validation (PDF, DOCX, DOC)
- ✅ File size validation (max 10MB)
- ✅ File removal functionality

### Test 3: Form Validation
- ✅ Submit button disabled without CV
- ✅ Submit button disabled without job description
- ✅ Submit button enabled with both inputs

### Test 4: AI Analysis (Requires OpenAI API Key)
1. Upload a CV file (PDF/DOCX)
2. Paste a job description
3. Click "Analyze CV with AI"
4. View results page with:
   - Overall score
   - Grammar suggestions
   - Keyword matching
   - ATS compatibility
   - Improved bullet points

## 📁 Sample Test Data

### Sample CV Content
```
John Doe
Software Engineer
john.doe@email.com
(555) 123-4567

EXPERIENCE
Software Engineer at Tech Corp (2020-2023)
- Developed web applications using React and Node.js
- Collaborated with cross-functional teams
- Implemented CI/CD pipelines

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2020

SKILLS
JavaScript, React, Node.js, Python, Git, Docker
```

### Sample Job Description
```
We are looking for a Software Engineer with experience in:
- React and Node.js development
- Web application development
- Team collaboration
- CI/CD implementation
- JavaScript and Python programming
- Version control with Git
```

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run `npm install` to install dependencies

2. **OpenAI API errors**
   - Check your API key in `.env.local`
   - Ensure you have sufficient API credits

3. **File upload issues**
   - Check file format (PDF, DOCX, DOC only)
   - Ensure file size < 10MB

4. **Build errors**
   - Clear `.next` folder: `rm -rf .next`
   - Restart dev server: `npm run dev`

### Development Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 🌟 Features to Test

### Core Functionality
- [ ] CV file upload (PDF/DOCX/DOC)
- [ ] Job description input
- [ ] AI-powered analysis
- [ ] Results display
- [ ] Navigation between pages

### UI/UX Elements
- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Form validation
- [ ] File drag & drop

### Security Features
- [ ] File type validation
- [ ] File size limits
- [ ] Temporary file processing
- [ ] No permanent storage

## 📱 Mobile Testing

Test the application on various screen sizes:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🔍 API Testing

### Test the CV Analysis Endpoint
```bash
# Using curl (replace with actual file path)
curl -X POST http://localhost:3000/api/analyze-cv \
  -F "cv=@/path/to/your/cv.pdf" \
  -F "jobDescription=Software Engineer position requiring React and Node.js"
```

### Expected Response Format
```json
{
  "grammarSuggestions": ["suggestion1", "suggestion2"],
  "keywordMatch": {
    "matched": ["keyword1", "keyword2"],
    "missing": ["keyword3", "keyword4"],
    "score": 75
  },
  "atsCompatibility": {
    "score": 80,
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"]
  },
  "improvedBulletPoints": ["improved bullet 1", "improved bullet 2"],
  "overallScore": 78,
  "summary": "Brief summary of the analysis"
}
```

## 🎯 Demo Scenarios

### Scenario 1: Perfect Match
- Upload CV with all required skills
- Job description matches CV perfectly
- Expected: High scores across all categories

### Scenario 2: Skills Gap
- Upload CV missing some required skills
- Job description has additional requirements
- Expected: Lower keyword match score, specific improvement suggestions

### Scenario 3: Format Issues
- Upload CV with poor formatting
- Job description is well-structured
- Expected: Lower ATS compatibility score, formatting suggestions

## 🚀 Next Steps

After testing the basic functionality:

1. **Add Authentication**
   - Implement NextAuth.js
   - Add user management
   - Track usage limits

2. **Enhance AI Analysis**
   - Industry-specific feedback
   - Role-based optimization
   - Custom analysis prompts

3. **Add Premium Features**
   - Multiple CV templates
   - Export functionality
   - Advanced analytics

4. **Performance Optimization**
   - File processing optimization
   - Caching strategies
   - CDN integration

## 📞 Support

If you encounter issues:
1. Check the console for error messages
2. Verify environment variables
3. Check file permissions
4. Review the README.md for detailed setup instructions

---

**Happy Testing! 🎉**
