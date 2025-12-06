import React, { useState } from 'react'
import { AlertCircle, Settings, Video, Shield, Bell } from 'lucide-react'
import CameraConfiguration from './screens/CameraConfiguration'
import RuleCreation from './screens/RuleCreation'
import LiveDetectionDashboard from './screens/LiveDetectionDashboard'
import AlertSettings from './screens/AlertSettings'

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('camera')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-black">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-black/80 backdrop-blur-md border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-8 h-8 text-red-500" />
              <h1 className="text-2xl font-bold text-white">Intruder Detection System</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-slate-800/50 border-b border-slate-700 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-8">
            <button
              onClick={() => setCurrentScreen('camera')}
              className={`flex items-center gap-2 px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
                currentScreen === 'camera'
                  ? 'border-red-500 text-red-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Video className="w-4 h-4" />
              Camera Setup
            </button>
            <button
              onClick={() => setCurrentScreen('rules')}
              className={`flex items-center gap-2 px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
                currentScreen === 'rules'
                  ? 'border-red-500 text-red-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Shield className="w-4 h-4" />
              Detection Rules
            </button>
            <button
              onClick={() => setCurrentScreen('dashboard')}
              className={`flex items-center gap-2 px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
                currentScreen === 'dashboard'
                  ? 'border-red-500 text-red-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Video className="w-4 h-4" />
              Live Dashboard
            </button>
            <button
              onClick={() => setCurrentScreen('alerts')}
              className={`flex items-center gap-2 px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
                currentScreen === 'alerts'
                  ? 'border-red-500 text-red-400'
                  : 'border-transparent text-gray-400 hover:text-gray-200'
              }`}
            >
              <Bell className="w-4 h-4" />
              Alert Settings
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentScreen === 'camera' && <CameraConfiguration />}
        {currentScreen === 'rules' && <RuleCreation />}
        {currentScreen === 'dashboard' && <LiveDetectionDashboard />}
        {currentScreen === 'alerts' && <AlertSettings />}
      </main>
    </div>
  )
}
