import LoginForm from '@/components/auth/LoginForm'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function LoginPage() {
  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 text-center mb-8">
            Welcome Back
          </h1>
          
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
            <LoginForm />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}