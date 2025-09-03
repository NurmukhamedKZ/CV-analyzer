'use client'

import { useState, useEffect } from 'react'
import { useAuth, useUser } from '@clerk/nextjs'
import { FileText, BarChart3, Clock, User } from 'lucide-react'

interface UserStats {
  user_id: number
  cv_uploads: number
  analyses_completed: number
  member_since: string
}

export default function UserDashboard() {
  const { getToken } = useAuth()
  const { user } = useUser()
  const [stats, setStats] = useState<UserStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchUserStats = async () => {
      try {
        const token = await getToken()
        const response = await fetch('/api/users/stats', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        if (response.ok) {
          const data = await response.json()
          setStats(data)
        }
      } catch (error) {
        console.error('Error fetching user stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchUserStats()
  }, [getToken])

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
      <div className="flex items-center mb-6">
        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
          <User className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Welcome back!</h2>
          <p className="text-gray-600">
            {user?.firstName || user?.emailAddresses[0].emailAddress}
          </p>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-600 text-sm font-medium">CV Uploads</p>
                <p className="text-2xl font-bold text-blue-900">{stats.cv_uploads}</p>
              </div>
              <FileText className="w-8 h-8 text-blue-600" />
            </div>
          </div>

          <div className="bg-green-50 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-600 text-sm font-medium">Analyses</p>
                <p className="text-2xl font-bold text-green-900">{stats.analyses_completed}</p>
              </div>
              <BarChart3 className="w-8 h-8 text-green-600" />
            </div>
          </div>

          <div className="bg-purple-50 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-600 text-sm font-medium">Member Since</p>
                <p className="text-lg font-bold text-purple-900">
                  {new Date(stats.member_since).toLocaleDateString()}
                </p>
              </div>
              <Clock className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>
      )}

      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="space-y-3">
          <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors">
            <div className="flex items-center">
              <FileText className="w-5 h-5 text-gray-400 mr-3" />
              <span className="text-gray-700">Upload New CV</span>
            </div>
          </button>
          <button className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors">
            <div className="flex items-center">
              <BarChart3 className="w-5 h-5 text-gray-400 mr-3" />
              <span className="text-gray-700">View Analysis History</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  )
}
