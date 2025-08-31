import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { Users, Target, Shield, Zap } from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">About AI CV Checker</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We're revolutionizing the way job seekers approach their applications with AI-powered CV analysis 
            that provides actionable insights and professional guidance.
          </p>
        </div>

        {/* Mission Section */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Our Mission</h2>
            <p className="text-lg text-gray-600 leading-relaxed mb-6">
              In today's competitive job market, having a standout CV is crucial. Our mission is to democratize 
              access to professional CV optimization tools, helping job seekers of all backgrounds present their 
              best selves to potential employers.
            </p>
            <p className="text-lg text-gray-600 leading-relaxed">
              We believe that everyone deserves the opportunity to showcase their skills and experience effectively, 
              regardless of their budget or access to career coaching services.
            </p>
          </div>
        </div>

        {/* Values Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Target className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Precision</h3>
            <p className="text-gray-600">AI-powered analysis that catches every detail and provides targeted improvements.</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Security</h3>
            <p className="text-gray-600">Your data is protected with enterprise-grade security and privacy measures.</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Speed</h3>
            <p className="text-gray-600">Get comprehensive feedback in seconds, not days or weeks.</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="w-8 h-8 text-yellow-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Accessibility</h3>
            <p className="text-gray-600">Professional tools available to everyone, regardless of their background.</p>
          </div>
        </div>

        {/* Technology Section */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Our Technology</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">AI-Powered Analysis</h3>
                <p className="text-gray-600 mb-4">
                  We leverage OpenAI's GPT-4 technology to provide human-like analysis of your CV, 
                  identifying areas for improvement that traditional tools might miss.
                </p>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Advanced natural language processing</li>
                  <li>• Context-aware feedback</li>
                  <li>• Industry-specific insights</li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">File Processing</h3>
                <p className="text-gray-600 mb-4">
                  Our robust file processing system handles multiple formats and ensures 
                  accurate text extraction for comprehensive analysis.
                </p>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• PDF, DOCX, and DOC support</li>
                  <li>• Secure temporary processing</li>
                  <li>• High accuracy text extraction</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Team Section */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Our Team</h2>
            <p className="text-lg text-gray-600 text-center mb-8">
              We're a team of passionate developers, designers, and career experts dedicated to 
              making professional development accessible to everyone.
            </p>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4"></div>
                <h3 className="font-semibold text-gray-900">Development Team</h3>
                <p className="text-gray-600 text-sm">Full-stack engineers building the future</p>
              </div>
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4"><img src='photos/nureke-car.png'></img></div>
                <h3 className="font-semibold text-gray-900">Design Team</h3>
                <p className="text-gray-600 text-sm">UX/UI experts crafting beautiful experiences</p>
              </div>
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-200 rounded-full mx-auto mb-4"></div>
                <h3 className="font-semibold text-gray-900">Career Experts</h3>
                <p className="text-gray-600 text-sm">HR professionals and career coaches</p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl p-8 max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold mb-4">Ready to Optimize Your CV?</h2>
            <p className="text-xl mb-6 opacity-90">
              Join thousands of job seekers who have already improved their applications with AI-powered insights.
            </p>
            <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors">
              Get Started Free
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
