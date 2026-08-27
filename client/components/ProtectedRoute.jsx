import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { username, ready } = useAuth()
  if (!ready) return null
  if (!username) return <Navigate to="/login" replace />
  return children
}
