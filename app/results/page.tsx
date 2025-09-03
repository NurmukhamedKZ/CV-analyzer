'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Download, Share2, Star, TrendingUp, Target, FileText, CheckCircle } from 'lucide-react'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

// Interface for the data returned by FastAPI backend (snake_case)
interface BackendCVAnalysisResult {
  grammar_suggestions: string[]
  keyword_match: {
    matched: string[]
    missing: string[]
    score: number
  }
  ats_compatibility: {
    score: number
    issues: string[]
    suggestions: string[]
  }
  should_learn_technologys: string[]
  overall_score: number
  summary: string
  metadata?: {
    filename: string
    file_size: number
    file_type: string
    analysis_timestamp: string
    user_id: string | null
  }
}

// Interface for the frontend (camelCase)
interface CVAnalysisResult {
  grammarSuggestions: string[]
  keywordMatch: {
    matched: string[]
    missing: string[]
    score: number
  }
  atsCompatibility: {
    score: number
    issues: string[]
    suggestions: string[]
  }
  shouldLearnTechnologys: string[]
  overallScore: number
  summary: string
  metadata?: {
    filename: string
    fileSize: number
    fileType: string
    analysisTimestamp: string
    userId: string | null
  }
}

// Function to transform backend data to frontend format
function transformBackendData(backendData: BackendCVAnalysisResult): CVAnalysisResult {
  return {
    grammarSuggestions: backendData.grammar_suggestions || [],
    keywordMatch: {
      matched: backendData.keyword_match?.matched || [],
      missing: backendData.keyword_match?.missing || [],
      score: backendData.keyword_match?.score || 0
    },
    atsCompatibility: {
      score: backendData.ats_compatibility?.score || 0,
      issues: backendData.ats_compatibility?.issues || [],
      suggestions: backendData.ats_compatibility?.suggestions || []
    },
    shouldLearnTechnologys: backendData.should_learn_technologys || [],
    overallScore: backendData.overall_score || 0,
    summary: backendData.summary || '',
    metadata: backendData.metadata ? {
      filename: backendData.metadata.filename,
      fileSize: backendData.metadata.file_size,
      fileType: backendData.metadata.file_type,
      analysisTimestamp: backendData.metadata.analysis_timestamp,
      userId: backendData.metadata.user_id
    } : undefined
  }
}

export default function ResultsPage() {
  const [result, setResult] = useState<CVAnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const storedResult = localStorage.getItem('cvAnalysisResult')
    if (storedResult) {
      try {
        const parsedResult = JSON.parse(storedResult)
        console.log('Raw stored result:', parsedResult)
        
        // Transform the data to match frontend interface
        const transformedResult = transformBackendData(parsedResult)
        console.log('Transformed result:', transformedResult)
        
        setResult(transformedResult)
      } catch (error) {
        console.error('Error parsing stored result:', error)
        router.push('/')
      }
    } else {
      router.push('/')
    }
    setIsLoading(false)
  }, [router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300">Loading results...</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-300 mb-4">No results found</p>
          <button
            onClick={() => router.push('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Go Back
          </button>
        </div>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 dark:text-green-400'
    if (score >= 60) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 dark:bg-green-900'
    if (score >= 60) return 'bg-yellow-100 dark:bg-yellow-900'
    return 'bg-red-100'
  }

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => router.push('/')}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:text-blue-400 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Analysis</span>
          </button>
          
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:text-blue-400 transition-colors">
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>
            <button className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:text-blue-400 transition-colors">
              <Share2 className="w-4 h-4" />
              <span>Share</span>
            </button>
          </div>
        </div>

        {/* Overall Score */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-8 mb-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">CV Analysis Results</h1>
            <div className="inline-flex items-center space-x-4 bg-gray-50 dark:bg-gray-700 px-8 py-4 rounded-full">
              <div className={`text-6xl font-bold ${getScoreColor(result.overallScore)}`}>
                {result.overallScore}
              </div>
              <div className="text-left">
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">Overall Score</p>
                <p className="text-gray-600 dark:text-gray-300">out of 100</p>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-300 mt-4 max-w-2xl mx-auto">{result.summary}</p>
          </div>
        </div>

        {/* Results Grid */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Grammar & Clarity */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Grammar & Clarity</h2>
            </div>
            <div className="space-y-3">
              {result.grammarSuggestions.map((suggestion, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-gray-700 dark:text-gray-300">{suggestion}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Keyword Match */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-green-600 dark:text-green-400" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Keyword Match</h2>
            </div>
            
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Match Score</span>
                <span className={`text-lg font-bold ${getScoreColor(result.keywordMatch.score)}`}>
                  {result.keywordMatch.score}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getScoreBgColor(result.keywordMatch.score)}`}
                  style={{ width: `${result.keywordMatch.score}%` }}
                ></div>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Matched Keywords:</h4>
                <div className="flex flex-wrap gap-2">
                  {result.keywordMatch.matched.map((keyword, index) => (
                    <span key={index} className="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 text-xs rounded-full">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Missing Keywords:</h4>
                <div className="flex flex-wrap gap-2">
                  {result.keywordMatch.missing.map((keyword, index) => (
                    <span key={index} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* ATS Compatibility */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">ATS Compatibility</h2>
            </div>
            
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">ATS Score</span>
                <span className={`text-lg font-bold ${getScoreColor(result.atsCompatibility.score)}`}>
                  {result.atsCompatibility.score}/100
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getScoreBgColor(result.atsCompatibility.score)}`}
                  style={{ width: `${result.atsCompatibility.score}%` }}
                ></div>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Issues Found:</h4>
                <ul className="space-y-1">
                  {result.atsCompatibility.issues.map((issue, index) => (
                    <li key={index} className="text-sm text-red-600 flex items-start space-x-2">
                      <span className="text-red-500 mt-1">•</span>
                      <span>{issue}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Suggestions:</h4>
                <ul className="space-y-1">
                  {result.atsCompatibility.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-sm text-green-600 dark:text-green-400 flex items-start space-x-2">
                      <span className="text-green-500 mt-1">•</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Improved Bullet Points */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
                <Star className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">You should learn technologys</h2>
            </div>
            
            <div className="space-y-3">
              {result.shouldLearnTechnologys.map((tech, index) => (
                <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                  <p className="text-sm text-gray-700 dark:text-gray-300">{tech}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="text-center mt-12">
          <button
            onClick={() => router.push('/')}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors mr-4"
          >
            Analyze Another CV
          </button>
          <button className="bg-gray-100 text-gray-700 dark:text-gray-300 px-8 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
            Get Premium Analysis
          </button>
        </div>
      </main>

      <Footer />
    </div>
  )
}
