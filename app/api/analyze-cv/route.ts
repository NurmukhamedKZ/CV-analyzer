import { NextRequest, NextResponse } from 'next/server'

// FastAPI backend URL
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    console.log('Frontend API route called - forwarding to FastAPI backend')
    
    const formData = await request.formData()
    const cvFile = formData.get('cv') as File
    const jobDescription = formData.get('jobDescription') as string

    console.log('Form data received:', { 
      hasCV: !!cvFile, 
      cvType: cvFile?.type, 
      cvSize: cvFile?.size,
      hasJobDesc: !!jobDescription 
    })

    if (!cvFile || !jobDescription) {
      console.log('Missing required fields')
      return NextResponse.json(
        { error: 'CV file and job description are required' },
        { status: 400 }
      )
    }

    // Forward the request to FastAPI backend with correct field names
    const backendFormData = new FormData()
    backendFormData.append('cv_file', cvFile)  // Changed from 'cv' to 'cv_file'
    backendFormData.append('job_description', jobDescription)  // Changed from 'jobDescription' to 'job_description'

    console.log('Forwarding request to FastAPI backend:', BACKEND_URL)
    
    const backendResponse = await fetch(`${BACKEND_URL}/api/analyze-cv`, {
      method: 'POST',
      body: backendFormData,
    })

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({}))
      console.error('Backend error:', backendResponse.status, errorData)
      
      return NextResponse.json(
        { 
          error: 'Backend analysis failed', 
          details: errorData.detail || 'Unknown error',
          status: backendResponse.status
        },
        { status: backendResponse.status }
      )
    }

    const analysisResult = await backendResponse.json()
    console.log('Backend analysis completed successfully')
    
    return NextResponse.json(analysisResult)

  } catch (error) {
    console.error('Error in frontend API route:', error)
    
    // Return a proper error response
    return NextResponse.json(
      { 
        error: 'Internal server error during CV analysis',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}
