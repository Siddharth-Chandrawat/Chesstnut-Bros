import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import NavBar from '../components/NavBar'
import GameCard from '../components/GameCard'
import { api } from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function HomePage() {
  const { username } = useAuth()
  const navigate = useNavigate()
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(true)
  const [starting, setStarting] = useState(false)

  useEffect(() => {
    api.listGames().then(setGames).finally(() => setLoading(false))
  }, [])

  async function handleNewGame() {
    setStarting(true)
    try {
      const { game_id } = await api.newGame()
      navigate(`/play/${game_id}`)
    } finally {
      setStarting(false)
    }
  }

  const recent = [...games]
    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
    .slice(0, 5)

  return (
    <div className="page fade-in">
      <NavBar />
      <section className="home-header">
        <h1>Welcome back, {username}</h1>
        <button className="btn-primary" onClick={handleNewGame} disabled={starting}>
          {starting ? 'Setting up board…' : 'New game'}
        </button>
      </section>
      <section className="home-recent">
        <div className="section-heading">
          <h2>Recent games</h2>
          <a href="/games" onClick={(e) => { e.preventDefault(); navigate('/games') }}>View all →</a>
        </div>
        {loading ? (
          <p className="muted">Loading…</p>
        ) : recent.length === 0 ? (
          <p className="muted">No games yet — start one above.</p>
        ) : (
          <div className="game-list">
            {recent.map((g) => <GameCard key={g.game_id} game={g} />)}
          </div>
        )}
      </section>
    </div>
  )
}
