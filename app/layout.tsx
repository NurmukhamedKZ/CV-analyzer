import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ClerkProvider } from '@clerk/nextjs'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI CV Checker - Professional CV Analysis & Optimization',
  description: 'Upload your CV and get AI-powered feedback on grammar, skills match, ATS compatibility, and improvement suggestions.',
  keywords: 'CV checker, resume analysis, AI feedback, ATS optimization, job application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
            {children}
          </div>
        </body>
      </html>
    </ClerkProvider>
  )
}
