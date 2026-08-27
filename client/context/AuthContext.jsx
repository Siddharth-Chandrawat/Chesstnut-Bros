import { createContext, useContext, useEffect, useState } from 'react'
import { api, getToken, setToken, clearToken, setStoredUsername, getStoredUsername } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [username, setUsername] = useState(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    // We don't decode the JWT client-side — a stored token just means
    // "was logged in as this cached username." If the token is stale
    // or invalid, the first API call 401s and ProtectedRoute bounces
    // to /login, which is a fine failure mode for a local test app.
    if (getToken()) setUsername(getStoredUsername())
    setReady(true)
  }, [])

  async function login(user, pass) {
    const { access_token } = await api.login(user, pass)
    setToken(access_token)
    setStoredUsername(user)
    setUsername(user)
  }

  async function register(user, pass) {
    const { access_token } = await api.register(user, pass)
    setToken(access_token)
    setStoredUsername(user)
    setUsername(user)
  }

  function logout() {
    clearToken()
    setUsername(null)
  }

  return (
    <AuthContext.Provider value={{ username, ready, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
