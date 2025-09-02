import logging
import os
from typing import Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
import json
import re

# Load environment variables
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)
else:
    load_dotenv()

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Service for AI-powered CV analysis using OpenAI"""
    
    def __init__(self):
        self.openai_client = None
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if self.api_key:
            try:
                masked = self.api_key[:6] + "..." + self.api_key[-4:]
                logger.info(f"Found OpenAI API key: {masked}")
                # ✅ New client initialization
                self.openai_client = AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.openai_client = None
        else:
            logger.warning("No OpenAI API key found. Will use mock analysis.")
    
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        try:
            if self.openai_client:
                logger.info("Using OpenAI for CV analysis")
                return await self._analyze_with_openai(cv_text, job_description)
            else:
                logger.info("Using mock analysis (no OpenAI API key)")
                return self._analyze_with_mock(cv_text, job_description)
        except Exception as e:
            logger.error(f"Error in CV analysis: {str(e)}")
            return self._analyze_with_mock(cv_text, job_description)
    
    async def _analyze_with_openai(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze CV using OpenAI GPT"""
        try:
            prompt = self._create_analysis_prompt(cv_text, job_description)
            
            # ✅ Use new API
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",   # consider gpt-4o / gpt-4o-mini for cost/perf
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert CV/resume analyst and career coach. 
                        analyse headhunter, linkedin, and another sites to find patterns in job requirements and keywords, 
                        Provide detailed, actionable feedback in the exact JSON format requested."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            
            response_text = response.choices[0].message.content
            
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                raise ValueError("No valid JSON found in response")
            
            analysis_result = json.loads(json_match.group())
            return self._normalize_analysis_result(analysis_result)
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            raise ValueError("Invalid response format from AI")
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    
    def _analyze_with_mock(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Provide mock analysis when OpenAI is not available"""
        logger.info("Providing mock analysis")
        
        # Simple keyword matching
        cv_lower = cv_text.lower()
        job_lower = job_description.lower()
        
        # Extract potential keywords from job description
        job_words = set(word.lower() for word in job_lower.split() if len(word) > 3)
        
        # Find matches and missing keywords
        matched_keywords = [word for word in job_words if word in cv_lower]
        missing_keywords = list(job_words - set(matched_keywords))[:10]  # Limit to 10
        
        # Calculate scores
        keyword_score = min(100, int((len(matched_keywords) / max(len(job_words), 1)) * 100))
        ats_score = max(50, keyword_score - 10)  # ATS score slightly lower
        overall_score = (keyword_score + ats_score) // 2
        
        return {
            "grammar_suggestions": [
                "Consider using more action verbs at the beginning of bullet points",
                "Ensure consistent formatting throughout the document",
                "Use present tense for current roles and past tense for previous positions",
                "Avoid generic phrases like 'responsible for' - be more specific"
            ],
            "keyword_match": {
                "matched": matched_keywords[:10],
                "missing": missing_keywords,
                "score": keyword_score
            },
            "ats_compatibility": {
                "score": ats_score,
                "issues": [
                    "Some bullet points could be more specific with metrics",
                    "Consider adding more industry-specific keywords",
                    "Format could be more ATS-friendly",
                    "Some sections might not be easily parseable by ATS systems"
                ],
                "suggestions": [
                    "Add quantifiable achievements (e.g., 'Increased performance by 25%')",
                    "Include more technical skills relevant to the job",
                    "Use standard section headers (Experience, Education, Skills)",
                    "Avoid complex formatting and graphics"
                ]
            },
            "improved_bullet_points": [
                "Developed and maintained 5+ web applications using React and Node.js, improving user engagement by 30%",
                "Collaborated with 8 cross-functional team members to deliver projects 20% ahead of schedule",
                "Implemented CI/CD pipelines reducing deployment time from 2 hours to 15 minutes",
                "Led technical architecture decisions for 3 major projects, resulting in 40% faster development cycles",
                "Mentored 4 junior developers, improving team productivity by 25%"
            ],
            "overall_score": overall_score,
            "summary": f"Good technical foundation with room for improvement in specificity and keyword optimization. Your CV matches {len(matched_keywords)} out of {len(job_words)} key terms from the job description. Focus on adding quantifiable achievements and industry-specific keywords to improve your ATS compatibility score."
        }
    
    def _create_analysis_prompt(self, cv_text: str, job_description: str) -> str:
        """Create the prompt for OpenAI analysis"""
        return f"""
Analyze this CV against the job description and provide comprehensive feedback in the following JSON format,


CV Text:
{cv_text[:3000]}...

Job Description:
{job_description[:1000]}...

Please provide analysis in this exact JSON format:
{{
  "grammar_suggestions": ["suggestion1", "suggestion2"],
  "keyword_match": {{
    "matched": ["keyword1", "keyword2"],
    "missing": ["keyword3", "keyword4"],
    "score": 75
  }},
  "ats_compatibility": {{
    "score": 80,
    "issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"]
  }},
  "should_learn_technologys": ["technology 1", "technology 2"],
  "overall_score": 78,
  "summary": "Brief summary of the analysis"
}}

Focus on:
- Grammar and clarity improvements
- Keyword matching between CV and job description
- ATS (Applicant Tracking System) compatibility issues
- Actionable improvement suggestions
- Write technologys that user should learn based on CV text to get a job
- Overall score based on all factors

Be specific and actionable in your feedback. Ensure the response is valid JSON."""
    
    def _normalize_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and validate the analysis result"""
        # Ensure all required fields are present
        required_fields = [
            "grammar_suggestions", "keyword_match", "ats_compatibility",
            "should_learn_technologys", "overall_score", "summary"
        ]
        
        for field in required_fields:
            if field not in result:
                logger.warning(f"Missing field in AI response: {field}")
                if field == "grammar_suggestions":
                    result[field] = ["No grammar suggestions available"]
                elif field == "keyword_match":
                    result[field] = {"matched": [], "missing": [], "score": 0}
                elif field == "ats_compatibility":
                    result[field] = {"score": 0, "issues": [], "suggestions": []}
                elif field == "should_learn_technologys":
                    result[field] = ["No should_learn_technologys available"]
                elif field == "overall_score":
                    result[field] = 0
                elif field == "summary":
                    result[field] = "Analysis summary not available"
        
        # Ensure scores are within valid range
        if "overall_score" in result:
            result["overall_score"] = max(0, min(100, int(result["overall_score"])))
        
        if "keyword_match" in result and "score" in result["keyword_match"]:
            result["keyword_match"]["score"] = max(0, min(100, int(result["keyword_match"]["score"])))
        
        if "ats_compatibility" in result and "score" in result["ats_compatibility"]:
            result["ats_compatibility"]["score"] = max(0, min(100, int(result["ats_compatibility"]["score"])))
        
        return result
