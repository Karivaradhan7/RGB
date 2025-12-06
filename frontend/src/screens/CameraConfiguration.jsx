import React, { useState } from 'react'
import { Camera, Play, Square, CheckCircle, AlertCircle } from 'lucide-react'
import { configureCamera, startStream, stopStream, testConnection } from '../api'

export default function CameraConfiguration() {
  const [sourceType, setSourceType] = useState('webcam')
  const [rtspUrl, setRtspUrl] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [testingConnection, setTestingConnection] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleTestConnection = async () => {
    setTestingConnection(true)
    try {
      const response = await testConnection(sourceType, rtspUrl)
      setConnectionStatus({
        success: response.data.status === 'success',
        message: response.data.message,
      })
    } catch (error) {
      setConnectionStatus({
        success: false,
        message: 'Connection failed',
      })
    }
    setTestingConnection(false)
  }

  const handleStartStream = async () => {
    setLoading(true)
    try {
      await configureCamera(sourceType, sourceType === 'rtsp' ? rtspUrl : null)
      await startStream()
      setIsStreaming(true)
    } catch (error) {
      alert('Failed to start stream')
    }
    setLoading(false)
  }

  const handleStopStream = async () => {
    setLoading(true)
    try {
      await stopStream()
      setIsStreaming(false)
    } catch (error) {
      alert('Failed to stop stream')
    }
    setLoading(false)
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Source Selection */}
        <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
            <Camera className="w-5 h-5 text-red-500" />
            Select Camera Source
          </h2>

          <div className="space-y-4">
            {[
              { value: 'webcam', label: 'Webcam', icon: '📹' },
              { value: 'rtsp', label: 'RTSP Stream', icon: '🌐' },
              { value: 'upload', label: 'Upload Video', icon: '📂' },
            ].map((option) => (
              <label key={option.value} className="flex items-center p-4 border border-slate-700 rounded-lg cursor-pointer hover:bg-slate-700/50 transition-colors" style={{ backgroundColor: sourceType === option.value ? 'rgba(59, 130, 246, 0.1)' : 'transparent', borderColor: sourceType === option.value ? '#3b82f6' : '#475569' }}>
                <input
                  type="radio"
                  name="source"
                  value={option.value}
                  checked={sourceType === option.value}
                  onChange={(e) => setSourceType(e.target.value)}
                  className="w-4 h-4"
                />
                <span className="ml-3 text-lg">{option.icon}</span>
                <span className="ml-3 text-white font-medium">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Configuration Panel */}
        <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-6">
          <h2 className="text-xl font-bold text-white mb-6">Configuration</h2>

          <div className="space-y-4">
            {sourceType === 'rtsp' && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  RTSP URL
                </label>
                <input
                  type="text"
                  placeholder="rtsp://camera-ip:554/stream"
                  value={rtspUrl}
                  onChange={(e) => setRtspUrl(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            )}

            {sourceType === 'upload' && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Video File
                </label>
                <input
                  type="file"
                  accept="video/*"
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
                />
              </div>
            )}

            {connectionStatus && (
              <div className={`p-4 rounded-lg flex items-center gap-3 ${connectionStatus.success ? 'bg-green-500/10 border border-green-500/50' : 'bg-red-500/10 border border-red-500/50'}`}>
                {connectionStatus.success ? (
                  <CheckCircle className="w-5 h-5 text-green-400" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-red-400" />
                )}
                <span className={connectionStatus.success ? 'text-green-400' : 'text-red-400'}>
                  {connectionStatus.message}
                </span>
              </div>
            )}

            <button
              onClick={handleTestConnection}
              disabled={testingConnection || (sourceType === 'rtsp' && !rtspUrl)}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
            >
              {testingConnection ? 'Testing...' : 'Test Connection'}
            </button>
          </div>
        </div>
      </div>

      {/* Stream Controls */}
      <div className="bg-gradient-to-r from-slate-800/50 to-slate-700/50 backdrop-blur rounded-lg border border-slate-700 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Stream Control</h3>
            <p className="text-gray-400 mt-1">
              {isStreaming ? '🔴 Live stream active' : '⚪ Stream inactive'}
            </p>
          </div>
          <div className="flex gap-3">
            {!isStreaming ? (
              <button
                onClick={handleStartStream}
                disabled={loading}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
              >
                <Play className="w-5 h-5" />
                {loading ? 'Starting...' : 'Start Stream'}
              </button>
            ) : (
              <button
                onClick={handleStopStream}
                disabled={loading}
                className="flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
              >
                <Square className="w-5 h-5" />
                {loading ? 'Stopping...' : 'Stop Stream'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
