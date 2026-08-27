import { Routes, Route } from 'react-router-dom'
import LandingPage from '../pages/LandingPage'
import LoginPage from '../pages/LoginPage'
import RegisterPage from '../pages/RegisterPage'
import HomePage from '../pages/HomePage'
import PlayPage from '../pages/PlayPage'
import HistoryPage from '../pages/HistoryPage'
import ReplayPage from '../pages/ReplayPage'
import ProtectedRoute from '../components/ProtectedRoute'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/home" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
      <Route path="/play/:gameId" element={<ProtectedRoute><PlayPage /></ProtectedRoute>} />
      <Route path="/games" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
      <Route path="/games/:gameId" element={<ProtectedRoute><ReplayPage /></ProtectedRoute>} />
    </Routes>
  )
}
