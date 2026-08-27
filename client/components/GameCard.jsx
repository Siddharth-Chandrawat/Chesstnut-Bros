import { Link } from 'react-router-dom'

const STATUS_LABEL = {
  in_progress: 'In progress',
  white_won: 'You won',
  black_won: 'Chesstnut won',
}

export default function GameCard({ game }) {
  const moveCount = game.moves?.length ?? 0
  const isLive = game.status === 'in_progress'

  return (
    <Link to={isLive ? `/play/${game.game_id}` : `/games/${game.game_id}`} className="game-card">
      <div className={`status-pill status-${game.status}`}>
        {STATUS_LABEL[game.status] ?? game.status}
      </div>
      <div className="game-card-body">
        <span className="game-card-id">Game #{game.game_id.slice(0, 6)}</span>
        <span className="game-card-meta">
          {moveCount} {moveCount === 1 ? 'ply' : 'plies'} · vs Chesstnut Engine
        </span>
      </div>
      <span className="game-card-arrow">→</span>
    </Link>
  )
}
