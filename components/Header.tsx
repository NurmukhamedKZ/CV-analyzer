'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, User } from 'lucide-react'
import { useAuth, useUser, SignInButton, UserButton } from '@clerk/nextjs'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { isSignedIn } = useAuth()
  const { user } = useUser()

  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">AI</span>
            </div>
            <span className="text-xl font-bold text-gray-900">CV Checker</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-600 hover:text-blue-600 transition-colors">
              Home
            </Link>
            <Link href="/about" className="text-gray-600 hover:text-blue-600 transition-colors">
              About
            </Link>
            <Link href="/pricing" className="text-gray-600 hover:text-blue-600 transition-colors">
              Pricing
            </Link>
          </nav>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isSignedIn ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-700">
                  Welcome, {user?.firstName || user?.emailAddresses[0].emailAddress}
                </span>
                <UserButton 
                  appearance={{
                    elements: {
                      avatarBox: 'w-8 h-8',
                      userButtonPopoverCard: 'shadow-xl border',
                      userButtonPopoverActionButton: 'hover:bg-gray-50'
                    }
                  }}
                />
              </div>
            ) : (
              <>
                <SignInButton mode="modal">
                  <button className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition-colors">
                    <User className="w-4 h-4" />
                    <span>Sign In</span>
                  </button>
                </SignInButton>
                <Link
                  href="/sign-up"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <X className="w-6 h-6 text-gray-600" />
            ) : (
              <Menu className="w-6 h-6 text-gray-600" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <nav className="flex flex-col space-y-4">
              <Link href="/" className="text-gray-600 hover:text-blue-600 transition-colors">
                Home
              </Link>
              <Link href="/about" className="text-gray-600 hover:text-blue-600 transition-colors">
                About
              </Link>
              <Link href="/pricing" className="text-gray-600 hover:text-blue-600 transition-colors">
                Pricing
              </Link>
              <div className="pt-4 border-t border-gray-100">
                {isSignedIn ? (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700 text-sm">
                      {user?.firstName || user?.emailAddresses[0].emailAddress}
                    </span>
                    <UserButton 
                      appearance={{
                        elements: {
                          avatarBox: 'w-8 h-8'
                        }
                      }}
                    />
                  </div>
                ) : (
                  <>
                    <SignInButton mode="modal">
                      <button className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition-colors mb-2 w-full">
                        <User className="w-4 h-4" />
                        <span>Sign In</span>
                      </button>
                    </SignInButton>
                    <Link
                      href="/sign-up"
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors w-full block text-center"
                    >
                      Sign Up
                    </Link>
                  </>
                )}
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
