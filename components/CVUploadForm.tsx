'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@clerk/nextjs'

interface CVUploadFormProps {
  setIsAnalyzing: (value: boolean) => void
}

export default function CVUploadForm({ setIsAnalyzing }: CVUploadFormProps) {
  const [cvFile, setCvFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const router = useRouter()
  const { getToken, isSignedIn } = useAuth()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setCvFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    multiple: false
  })

  const removeFile = () => {
    setCvFile(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!isSignedIn) {
      alert('Please sign in to analyze your CV')
      return
    }
    
    if (!cvFile || !jobDescription.trim()) {
      alert('Please upload a CV and enter a job description')
      return
    }

    setIsUploading(true)
    setIsAnalyzing(true)

    try {
      // Get authentication token
      const token = await getToken()
      
      const formData = new FormData()
      formData.append('cv', cvFile)
      formData.append('jobDescription', jobDescription)

      const response = await fetch('/api/analyze-cv', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Backend response received:', result)
        
        // Store result in localStorage for the results page
        localStorage.setItem('cvAnalysisResult', JSON.stringify(result))
        console.log('Result stored in localStorage')
        
        router.push('/results')
      } else {
        const errorData = await response.json().catch(() => ({}))
        console.error('Backend error response:', errorData)
        throw new Error(`Analysis failed: ${errorData.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred during analysis. Please try again.')
    } finally {
      setIsUploading(false)
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 p-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Analyze Your CV</h2>
        <p className="text-gray-600 dark:text-gray-300">Upload your CV and paste the job description for AI-powered analysis</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* CV Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Upload Your CV
          </label>
          
          {!cvFile ? (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {isDragActive ? 'Drop your CV here' : 'Click to upload or drag and drop'}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Supports PDF, DOCX, and DOC files (max 10MB)
              </p>
            </div>
          ) : (
            <div className="border border-gray-200 dark:border-gray-600 rounded-lg p-4 bg-gray-50 dark:bg-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileText className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{cvFile.name}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {(cvFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={removeFile}
                  className="p-2 text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Job Description */}
        <div>
          <label htmlFor="jobDescription" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Job Description
          </label>
          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description you're applying for here..."
            className="w-full h-32 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            required
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!cvFile || !jobDescription.trim() || isUploading}
          className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
        >
          {isUploading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Analyzing CV...
            </>
          ) : (
            'Analyze CV with AI'
          )}
        </button>

        {/* Disclaimer */}
        <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
          By uploading your CV, you agree that it will be processed for analysis purposes only.
        </p>
      </form>
    </div>
  )
}
