# AI CV Checker

A full-stack web application that provides AI-powered CV analysis and optimization feedback. Users can upload their CV (PDF/DOCX) and paste a job description to receive comprehensive feedback on grammar, skills match, ATS compatibility, and improvement suggestions.

## Features

- **CV Upload**: Support for PDF, DOCX, and DOC files
- **AI Analysis**: Powered by OpenAI GPT-4 for comprehensive feedback
- **Multiple Analysis Areas**:
  - Grammar and clarity suggestions
  - Keyword matching with job descriptions
  - ATS (Applicant Tracking System) compatibility scoring
  - Improved bullet point suggestions
  - Overall CV score
- **Professional UI**: Clean, modern interface built with TailwindCSS
- **Responsive Design**: Works on desktop and mobile devices
- **Security**: CVs are processed temporarily and not stored permanently

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript and App Router
- **Styling**: TailwindCSS with custom design system
- **Backend**: Next.js API routes
- **AI**: OpenAI GPT-4 API
- **File Processing**: pdf-parse for PDFs, docx for Word documents
- **UI Components**: Custom components with Lucide React icons
- **File Upload**: React Dropzone for drag-and-drop functionality

## Prerequisites

- Node.js 18+ 
- npm or yarn
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-cv-checker
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   ```
   
   Edit `.env.local` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

1. **Upload CV**: Drag and drop or click to upload your CV file (PDF, DOCX, or DOC)
2. **Add Job Description**: Paste the job description you're applying for
3. **Analyze**: Click "Analyze CV with AI" to start the analysis
4. **Review Results**: View comprehensive feedback in organized sections:
   - Grammar and clarity improvements
   - Keyword matching analysis
   - ATS compatibility score and suggestions
   - Improved bullet point examples
   - Overall CV score

## API Endpoints

### POST `/api/analyze-cv`
Analyzes a CV against a job description using AI.

**Request Body (FormData):**
- `cv`: CV file (PDF, DOCX, or DOC)
- `jobDescription`: Text of the job description

**Response:**
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

## Project Structure

```
ai-cv-checker/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   │   └── analyze-cv/    # CV analysis endpoint
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── results/           # Results page
├── components/             # React components
│   ├── CVUploadForm.tsx   # Main upload form
│   ├── Header.tsx         # Navigation header
│   └── Footer.tsx         # Footer component
├── public/                 # Static assets
├── .env.local             # Environment variables
├── package.json           # Dependencies
├── tailwind.config.js     # TailwindCSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT-4 access | Yes |
| `NEXTAUTH_URL` | NextAuth.js base URL | No (for future auth) |
| `NEXTAUTH_SECRET` | NextAuth.js secret key | No (for future auth) |

## Security Features

- **File Validation**: Only allows PDF, DOCX, and DOC files
- **Size Limits**: Maximum file size of 10MB
- **Temporary Processing**: CVs are processed in memory and not stored
- **Input Sanitization**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Future Enhancements

- [ ] User authentication with NextAuth.js
- [ ] User dashboard for CV history
- [ ] Premium features and subscription plans
- [ ] CV templates and examples
- [ ] Export analysis reports
- [ ] Integration with job boards
- [ ] Multi-language support

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ai-cv-checker/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Next.js team for the excellent framework
- TailwindCSS for the utility-first CSS framework
- The open-source community for various packages and tools

---

**Note**: This application requires an active OpenAI API key to function. Make sure to keep your API key secure and never commit it to version control.
