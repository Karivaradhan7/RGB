import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const configureCamera = (sourceType, rtspUrl = null, videoFile = null) => {
  return api.post('/configure_camera', {
    source_type: sourceType,
    rtsp_url: rtspUrl,
    video_file: videoFile,
  })
}

export const startStream = () => {
  return api.post('/start_stream')
}

export const stopStream = () => {
  return api.post('/stop_stream')
}

export const getDetections = () => {
  return api.get('/get_detections')
}

export const createRule = (name, objectType, threshold) => {
  return api.post('/create_rule', {
    name,
    object_type: objectType,
    threshold,
  })
}

export const getRules = () => {
  return api.get('/get_rules')
}

export const deleteRule = (ruleId) => {
  return api.delete(`/delete_rule/${ruleId}`)
}

export const configureAlerts = (emails) => {
  return api.post('/configure_alerts', {
    emails,
  })
}

export const sendTestEmail = (emails) => {
  return api.post('/send_test_email', emails)
}

export const getAlerts = (limit = 20) => {
  return api.get('/get_alerts', { params: { limit } })
}

export const testConnection = (sourceType, rtspUrl = null) => {
  return api.post('/test_connection', {
    source_type: sourceType,
    rtsp_url: rtspUrl,
  })
}

export const getHealth = () => {
  return api.get('/health')
}

export const connectWebSocket = (onMessage) => {
  const ws = new WebSocket('ws://localhost:8000/ws/stream')
  
  ws.onopen = () => {
    console.log('WebSocket connected')
    ws.send(JSON.stringify({ type: 'start' }))
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
  }
  
  return ws
}

export default api
