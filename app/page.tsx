'use client'

import { useState } from 'react'
import { Upload, FileText, Briefcase, Sparkles, Shield, CheckCircle } from 'lucide-react'
import CVUploadForm from '@/components/CVUploadForm'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function HomePage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-blue-100 rounded-full">
              <Sparkles className="w-12 h-12 text-blue-600" />
            </div>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered CV Analysis
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload your CV and get instant AI feedback on grammar, skills match, ATS compatibility, 
            and professional improvement suggestions.
          </p>
          
          {/* Free Scan Banner */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-full inline-flex items-center gap-2 mb-8">
            <CheckCircle className="w-5 h-5" />
            <span className="font-semibold">Free 1 Scan / Login for Unlimited</span>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="text-center p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload CV</h3>
            <p className="text-gray-600">Support for PDF and DOCX formats with secure processing</p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Analysis</h3>
            <p className="text-gray-600">Advanced GPT-4 analysis for comprehensive feedback</p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Briefcase className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Results</h3>
            <p className="text-gray-600">Detailed insights and actionable improvement suggestions</p>
          </div>
        </div>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <CVUploadForm setIsAnalyzing={setIsAnalyzing} />
        </div>

        {/* Security Notice
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-2 bg-green-50 text-green-800 px-6 py-3 rounded-lg border border-green-200">
            <Shield className="w-5 h-5" />
            <span className="font-medium">Your CV is not stored. Only analyzed for feedback.</span>
          </div>
        </div> */}

        {/* How It Works */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold text-lg">1</div>
              <h3 className="font-semibold text-gray-900 mb-2">Upload CV</h3>
              <p className="text-gray-600 text-sm">Upload your CV in PDF or DOCX format</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold text-lg">2</div>
              <h3 className="font-semibold text-gray-900 mb-2">Add Job Description</h3>
              <p className="text-gray-600 text-sm">Paste the job description you're applying for</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold text-lg">3</div>
              <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600 text-sm">Our AI analyzes compatibility and provides feedback</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 font-bold text-lg">4</div>
              <h3 className="font-semibold text-gray-900 mb-2">Get Results</h3>
              <p className="text-gray-600 text-sm">Receive detailed insights and improvement tips</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
