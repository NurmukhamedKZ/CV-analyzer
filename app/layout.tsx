import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ClerkProvider } from '@clerk/nextjs'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'CVlytics',
  description: 'Upload your CV and get AI-powered feedback on grammar, skills match, ATS compatibility, and improvement suggestions.',
  keywords: 'CV checker, resume analysis, AI feedback, ATS optimization, job application',
  icons: {
    icon: '/Users/nurma/vscode_projects/CVaiStartup/public/favicon.ico',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <head>
          <script
            dangerouslySetInnerHTML={{
              __html: `
                try {
                  // Always enable dark mode by default
                  document.documentElement.classList.add('dark')
                  localStorage.setItem('theme', 'dark')
                } catch (_) {}
              `,
            }}
          />
        </head>
        <body className={inter.className}>
          <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
            {children}
          </div>
        </body>
      </html>
    </ClerkProvider>
  )
}
