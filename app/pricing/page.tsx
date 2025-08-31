import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { Check, Star } from 'lucide-react'

export default function PricingPage() {
  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-gray-600">Choose the plan that fits your needs</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Free Plan */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Free</h3>
              <div className="text-4xl font-bold text-gray-900 mb-2">$0</div>
              <p className="text-gray-600">Perfect for trying out</p>
            </div>
            
            <ul className="space-y-3 mb-8">
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>1 CV analysis per month</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Basic feedback</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Grammar suggestions</span>
              </li>
            </ul>
            
            <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
              Get Started Free
            </button>
          </div>

          {/* Pro Plan */}
          <div className="bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-8 relative">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <div className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center space-x-1">
                <Star className="w-4 h-4" />
                <span>Most Popular</span>
              </div>
            </div>
            
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Pro</h3>
              <div className="text-4xl font-bold text-gray-900 mb-2">$19</div>
              <p className="text-gray-600">per month</p>
            </div>
            
            <ul className="space-y-3 mb-8">
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Unlimited CV analysis</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Advanced AI feedback</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>ATS optimization</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Export reports</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Priority support</span>
              </li>
            </ul>
            
            <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
              Start Pro Trial
            </button>
          </div>

          {/* Enterprise Plan */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Enterprise</h3>
              <div className="text-4xl font-bold text-gray-900 mb-2">Custom</div>
              <p className="text-gray-600">For teams & organizations</p>
            </div>
            
            <ul className="space-y-3 mb-8">
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Everything in Pro</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Team management</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>API access</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Custom integrations</span>
              </li>
              <li className="flex items-center space-x-3">
                <Check className="w-5 h-5 text-green-600" />
                <span>Dedicated support</span>
              </li>
            </ul>
            
            <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
              Contact Sales
            </button>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Frequently Asked Questions</h2>
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-2">How accurate is the AI analysis?</h3>
              <p className="text-gray-600">Our AI uses advanced GPT-4 technology to provide highly accurate and actionable feedback on your CV.</p>
            </div>
            
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-2">Can I cancel my subscription anytime?</h3>
              <p className="text-gray-600">Yes, you can cancel your subscription at any time. No long-term contracts or hidden fees.</p>
            </div>
            
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-2">What file formats do you support?</h3>
              <p className="text-gray-600">We support PDF, DOCX, and DOC files up to 10MB in size.</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
