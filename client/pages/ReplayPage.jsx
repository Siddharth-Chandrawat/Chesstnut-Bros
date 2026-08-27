import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Chess } from 'chess.js'
import NavBar from '../components/NavBar'
import ChessBoardView from '../components/ChessBoardView'
import MoveList from '../components/MoveList'
import ReplayControls from '../components/ReplayControls'
import { api } from '../api/client'
import { indexToAlgebraic } from '../api/chessSquares'

export default function ReplayPage() {
  const { gameId } = useParams()
  const [game, setGame] = useState(null)
  const [positions, setPositions] = useState([]) // FEN snapshot at each ply; positions[0] = starting position
  const [sanMoves, setSanMoves] = useState([])
  const [ply, setPly] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getGame(gameId).then((g) => {
      setGame(g)
      const { positions: pos, sans } = buildPositions(g.moves)
      setPositions(pos)
      setSanMoves(sans)
      setPly(pos.length - 1) // land on the final position by default
      setLoading(false)
    })
  }, [gameId])

  // Precomputing every position up front means stepping through the
  // game is instant — no re-derivation on each button click.
  function buildPositions(moves) {
    const chess = new Chess()
    const pos = [chess.fen()]
    const sans = []
    for (const [from, to] of moves) {
      const fromSq = indexToAlgebraic(from)
      const toSq = indexToAlgebraic(to)
      const piece = chess.get(fromSq)
      const isPromotion = piece?.type === 'p' && (toSq[1] === '8' || toSq[1] === '1')
      const move = chess.move({ from: fromSq, to: toSq, promotion: isPromotion ? 'q' : undefined })
      if (move) sans.push(move.san)
      pos.push(chess.fen())
    }
    return { positions: pos, sans }
  }

  if (loading || !game) {
    return (
      <div className="page fade-in">
        <NavBar />
        <p className="muted center">Loading game…</p>
      </div>
    )
  }

  const lastMoveIndices = ply > 0 ? game.moves[ply - 1] : null
  const lastMove = lastMoveIndices
    ? { from: indexToAlgebraic(lastMoveIndices[0]), to: indexToAlgebraic(lastMoveIndices[1]) }
    : null

  return (
    <div className="page fade-in play-page">
      <NavBar />
      <div className="play-layout">
        <div className="board-column">
          <ChessBoardView fen={positions[ply]} arePiecesDraggable={false} lastMove={lastMove} />
          <ReplayControls currentPly={ply} maxPly={positions.length - 1} onChange={setPly} />
        </div>
        <aside className="side-panel">
          <h3>Moves</h3>
          <MoveList sanMoves={sanMoves} currentPly={ply} onSelectPly={setPly} />
        </aside>
      </div>
    </div>
  )
}
