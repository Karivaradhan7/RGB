import React, { useState, useEffect, useRef } from 'react'
import { Video, Users, AlertCircle, Eye } from 'lucide-react'
import { connectWebSocket, getDetections, getAlerts } from '../api'

export default function LiveDetectionDashboard() {
  const [frameData, setFrameData] = useState(null)
  const [detections, setDetections] = useState({ person: 0, animal: 0, vehicle: 0 })
  const [alerts, setAlerts] = useState([])
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    // Connect to WebSocket
    wsRef.current = connectWebSocket((data) => {
      if (data.type === 'frame') {
        setFrameData(data.data)
        setDetections(data.detections)
      } else if (data.type === 'alert') {
        setAlerts((prev) => [data.data, ...prev].slice(0, 10))
      }
    })

    setIsConnected(true)

    // Poll for detections
    const detectionInterval = setInterval(async () => {
      try {
        const response = await getDetections()
        setDetections(response.data)
      } catch (error) {
        console.error('Failed to get detections')
      }
    }, 1000)

    // Poll for alerts
    const alertInterval = setInterval(async () => {
      try {
        const response = await getAlerts(10)
        setAlerts(response.data)
      } catch (error) {
        console.error('Failed to get alerts')
      }
    }, 2000)

    return () => {
      clearInterval(detectionInterval)
      clearInterval(alertInterval)
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  return (
    <div className="space-y-8">
      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Video Feed - Large Left Side */}
        <div className="lg:col-span-2">
          <div className="bg-black rounded-lg border border-slate-700 overflow-hidden h-[500px] relative">
            {frameData ? (
              <div className="relative w-full h-full flex items-center justify-center bg-gray-900">
                <img
                  src={`data:image/jpeg;base64,${frameData}`}
                  alt="Live Stream"
                  className="w-full h-full object-contain"
                />
                <div className="absolute top-4 left-4 flex items-center gap-2 px-3 py-1 bg-black/70 rounded-full">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-red-400 font-bold text-sm">LIVE</span>
                </div>
              </div>
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 to-black">
                <Video className="w-16 h-16 text-gray-600 mb-4" />
                <p className="text-gray-500">No stream active</p>
                <p className="text-gray-600 text-sm mt-1">Start a stream from Camera Setup</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Side Stats Panel */}
        <div className="space-y-4">
          {/* Detection Stats */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg border border-slate-700 p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-400" />
              Real-time Detections
            </h3>

            <div className="space-y-3">
              {[
                { label: 'Persons', count: detections.person, color: 'green', icon: '👤' },
                { label: 'Animals', count: detections.animal, color: 'yellow', icon: '🐾' },
                { label: 'Vehicles', count: detections.vehicle, color: 'purple', icon: '🚗' },
              ].map((item) => (
                <div key={item.label} className={`bg-slate-900/50 rounded-lg p-4 border-l-4 border-${item.color}-500`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{item.icon}</span>
                      <div>
                        <p className="text-gray-400 text-sm">{item.label}</p>
                      </div>
                    </div>
                    <div className="text-3xl font-bold text-white">{item.count}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Connection Status */}
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg border border-slate-700 p-4">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Alerts Section */}
      <div className="bg-slate-800/50 backdrop-blur rounded-lg border border-slate-700 p-6">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-red-500" />
          Recent Alerts ({alerts.length})
        </h3>

        {alerts.length === 0 ? (
          <div className="text-center py-12">
            <Eye className="w-8 h-8 text-gray-600 mx-auto mb-2" />
            <p className="text-gray-400">No alerts yet</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {alerts.map((alert, idx) => (
              <div
                key={idx}
                className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 flex items-start gap-4"
              >
                <div className="flex-1">
                  <div className="font-semibold text-red-400">{alert.rule_name}</div>
                  <div className="text-sm text-gray-300 mt-1">
                    {alert.object_type.charAt(0).toUpperCase() + alert.object_type.slice(1)}: {alert.count} detected
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </div>
                </div>
                <div className="text-2xl font-bold text-red-400">{alert.count}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
