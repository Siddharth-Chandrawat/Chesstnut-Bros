import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { ApiError } from '../api/client'

export default function LoginPage() {
  const { username: currentUsername, login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(username, password)
      // replace, not push: logging in shouldn't leave the login form
      // sitting in this tab's history right underneath /home — hitting
      // Back would otherwise show the form again while still authenticated.
      navigate('/home', { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page fade-in auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Log in</h2>
        {currentUsername && (
          <p className="auth-notice">
            This tab is currently signed in as <strong>{currentUsername}</strong>.
            Logging in below switches this tab to a different account —
            any other tab stays signed in as it was.
          </p>
        )}
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <p className="form-error">{error}</p>}
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? 'Logging in…' : 'Log in'}
        </button>
        <p className="auth-switch">No account yet? <Link to="/register">Sign up</Link></p>
      </form>
    </div>
  )
}
