import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Chess } from 'chess.js'
import NavBar from '../components/NavBar'
import ChessBoardView from '../components/ChessBoardView'
import MoveList from '../components/MoveList'
import ThinkingIndicator from '../components/ThinkingIndicator'
import { api, ApiError } from '../api/client'
import { algebraicToIndex, indexToAlgebraic } from '../api/chessSquares'

export default function PlayPage() {
  const { gameId } = useParams()
  const navigate = useNavigate()
  const chessRef = useRef(new Chess())

  const [fen, setFen] = useState(null)
  const [sanMoves, setSanMoves] = useState([])
  const [lastMove, setLastMove] = useState(null)
  const [status, setStatus] = useState('in_progress')
  const [thinking, setThinking] = useState(false)
  const [busyLabel, setBusyLabel] = useState('Chesstnut is thinking…')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .getGame(gameId)
      .then((game) => {
        chessRef.current.load(game.fen)
        setFen(game.fen)
        setStatus(game.status)
        setSanMoves(rebuildSanHistory(game.moves))
        setLoading(false)
      })
      .catch(() => {
        setError('Could not load this game.')
        setLoading(false)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gameId])

  // The server only stores [from, to] index pairs, not SAN — replay
  // them from the start on a scratch chess.js instance purely to get
  // readable notation for the move list.
  function rebuildSanHistory(moves) {
    const replay = new Chess()
    const sans = []
    for (const [from, to] of moves) {
      const move = applyIndexMove(replay, from, to)
      if (move) sans.push(move.san)
    }
    return sans
  }

  function applyIndexMove(chess, fromIdx, toIdx) {
    const from = indexToAlgebraic(fromIdx)
    const to = indexToAlgebraic(toIdx)
    const piece = chess.get(from)
    // Chesstnut always auto-promotes to queen (see engine notes) —
    // match that here so replay never desyncs on a promoting move.
    const isPromotion = piece?.type === 'p' && (to[1] === '8' || to[1] === '1')
    try {
      return chess.move({ from, to, promotion: isPromotion ? 'q' : undefined })
    } catch {
      return null // shouldn't happen against server-validated moves; fail closed rather than crash
    }
  }

  function handleDrop(sourceSquare, targetSquare) {
    if (thinking || status !== 'in_progress') return false

    const fromIdx = algebraicToIndex(sourceSquare)
    const toIdx = algebraicToIndex(targetSquare)
    const preMoveFen = chessRef.current.fen()

    // Local legality check + SAN capture happens synchronously, so
    // this function can return true/false immediately as react-
    // chessboard expects. The server round-trip is kicked off
    // separately below and reconciles state once it resolves.
    const humanMove = applyIndexMove(chessRef.current, fromIdx, toIdx)
    if (!humanMove) return false

    setSanMoves((prev) => [...prev, humanMove.san])
    setFen(chessRef.current.fen())
    setLastMove({ from: sourceSquare, to: targetSquare })
    setError(null)
    setBusyLabel('Chesstnut is thinking…')
    setThinking(true)

    submitToServer(fromIdx, toIdx, preMoveFen)
    return true
  }

  async function submitToServer(fromIdx, toIdx, preMoveFen) {
    try {
      const result = await api.submitMove(gameId, fromIdx, toIdx)

      if (result.engine_move) {
        const [ef, et] = result.engine_move
        const engineMove = applyIndexMove(chessRef.current, ef, et)
        if (engineMove) setSanMoves((prev) => [...prev, engineMove.san])
        setLastMove({ from: indexToAlgebraic(ef), to: indexToAlgebraic(et) })
      }

      // Server is authoritative — hard-sync to its FEN rather than
      // trusting our own local replay for anything beyond SAN display.
      chessRef.current.load(result.fen)
      setFen(result.fen)
      setStatus(result.status)
    } catch (err) {
      // Roll back the optimistic local move: illegal per the server,
      // a stale/conflicting game state, or the request failed outright.
      chessRef.current.load(preMoveFen)
      setFen(preMoveFen)
      setSanMoves((prev) => prev.slice(0, -1))
      setError(err instanceof ApiError ? err.message : 'Move failed — try again.')
    } finally {
      setThinking(false)
    }
  }

  async function handleResign() {
    if (thinking || status !== 'in_progress') return
    if (!window.confirm('Resign this game?')) return

    setBusyLabel('Resigning…')
    setThinking(true)
    setError(null)
    try {
      const result = await api.resignGame(gameId)
      setStatus(result.status)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not resign — try again.')
    } finally {
      setThinking(false)
    }
  }

  async function handleUndo() {
    if (thinking || status !== 'in_progress' || sanMoves.length < 2) return

    setBusyLabel('Undoing your last move…')
    setThinking(true)
    setError(null)
    try {
      const result = await api.undoMove(gameId)
      chessRef.current.load(result.fen)
      setFen(result.fen)
      setStatus(result.status)
      setSanMoves(rebuildSanHistory(result.moves))
      const moves = result.moves
      const last = moves[moves.length - 1]
      setLastMove(last ? { from: indexToAlgebraic(last[0]), to: indexToAlgebraic(last[1]) } : null)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not undo — try again.')
    } finally {
      setThinking(false)
    }
  }

  if (loading) {
    return (
      <div className="page fade-in">
        <NavBar />
        <p className="muted center">Loading game…</p>
      </div>
    )
  }

  return (
    <div className="page fade-in play-page">
      <NavBar />
      <div className="play-layout">
        <div className="board-column">
          <ChessBoardView
            fen={fen}
            onPieceDrop={handleDrop}
            arePiecesDraggable={!thinking && status === 'in_progress'}
            lastMove={lastMove}
          />
          {status === 'in_progress' && (
            <div className="game-actions">
              <button className="btn-ghost" onClick={handleUndo} disabled={thinking || sanMoves.length < 2}>
                Undo last move
              </button>
              <button className="btn-danger" onClick={handleResign} disabled={thinking}>
                Resign
              </button>
            </div>
          )}
          {thinking && <ThinkingIndicator label={busyLabel} />}
          {error && <p className="form-error">{error}</p>}
          {status !== 'in_progress' && (
            <div className="game-over-banner">
              <h3>{status === 'white_won' ? 'You won!' : 'Chesstnut won.'}</h3>
              <button className="btn-primary" onClick={() => navigate('/home')}>Back to home</button>
            </div>
          )}
        </div>
        <aside className="side-panel">
          <h3>Moves</h3>
          <MoveList sanMoves={sanMoves} currentPly={sanMoves.length} />
        </aside>
      </div>
    </div>
  )
}
