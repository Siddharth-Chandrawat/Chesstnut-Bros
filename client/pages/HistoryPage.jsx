import { useEffect, useState } from 'react'
import NavBar from '../components/NavBar'
import GameCard from '../components/GameCard'
import { api } from '../api/client'

export default function HistoryPage() {
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.listGames().then(setGames).finally(() => setLoading(false))
  }, [])

  const sorted = [...games].sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))

  return (
    <div className="page fade-in">
      <NavBar />
      <section className="history-page">
        <h1>Your games</h1>
        {loading ? (
          <p className="muted">Loading…</p>
        ) : sorted.length === 0 ? (
          <p className="muted">No games yet.</p>
        ) : (
          <div className="game-list">
            {sorted.map((g) => <GameCard key={g.game_id} game={g} />)}
          </div>
        )}
      </section>
    </div>
  )
}
