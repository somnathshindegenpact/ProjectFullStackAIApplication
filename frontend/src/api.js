function getApiBase() {
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search)
    const apiOverride = params.get('api') || params.get('apiUrl')
    if (apiOverride && apiOverride.trim()) {
      return apiOverride.trim().replace(/\/$/, '')
    }
  }

  const configured = process.env.REACT_APP_API_URL && process.env.REACT_APP_API_URL.trim()
  if (configured) {
    return configured.replace(/\/$/, '')
  }

  if (typeof window !== 'undefined') {
    const host = window.location.hostname
    if (host === 'localhost' || host === '127.0.0.1' || host === '::1') {
      return 'http://localhost:5000'
    }
  }

  return process.env.REACT_APP_API_URL || 'https://task-manager-api-346f.onrender.com'
}

// Keep the deployment target explicit for GitHub Pages builds.

const API_BASE = getApiBase()

function authHeaders() {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
}

async function request(path, options = {}) {
  if (!API_BASE) {
    return {
      msg: 'The backend API is not configured for this deployment. Set REACT_APP_API_URL to your public Flask backend URL before using login or registration.'
    }
  }

  const defaultHeaders = {
    'Content-Type': 'application/json'
  }

  const finalOptions = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {})
    }
  }

  const targetUrl = `${API_BASE}${path}`

  try {
    const res = await fetch(targetUrl, finalOptions)
    const text = await res.text()
    let data = {}

    try {
      data = text ? JSON.parse(text) : {}
    } catch {
      data = { msg: text || 'Invalid JSON response' }
    }

    if (!res.ok) {
      return { ...data, _status: res.status, _url: targetUrl }
    }

    return { ...data, _url: targetUrl }
  } catch (error) {
    return {
      msg: 'Unable to reach the API server. Check the backend deployment and CORS settings.',
      error: error.message,
      _url: targetUrl
    }
  }
}

export async function register(email, password) {
  return request('/api/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) })
}

export async function login(email, password) {
  return request('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
}

export async function forgotPassword(email) {
  return request('/api/auth/forgot-password', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ email }) })
}

export async function resetPassword(token, password) {
  return request('/api/auth/reset-password', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ token, password }) })
}

export async function fetchTasks() {
  return request('/api/tasks/', { headers: authHeaders() })
}

export async function fetchTask(id) {
  return request(`/api/tasks/${id}`, { headers: authHeaders() })
}

export async function createTask(payload) {
  return request('/api/tasks/', { method: 'POST', headers: authHeaders(), body: JSON.stringify(payload) })
}

export async function updateTask(id, payload) {
  return request(`/api/tasks/${id}`, { method: 'PUT', headers: authHeaders(), body: JSON.stringify(payload) })
}

export async function deleteTask(id) {
  return request(`/api/tasks/${id}`, { method: 'DELETE', headers: authHeaders() })
}

export async function askAI(query) {
  return request('/api/ai/ask', { method: 'POST', headers: authHeaders(), body: JSON.stringify({ query }) })
}

export async function ingestDoc(payload) {
  return request('/api/ai/ingest', { method: 'POST', headers: authHeaders(), body: JSON.stringify(payload) })
}

export default { register, login, forgotPassword, resetPassword, fetchTasks, fetchTask, createTask, updateTask, deleteTask, askAI, ingestDoc }
