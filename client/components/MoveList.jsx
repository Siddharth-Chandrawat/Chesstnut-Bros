// Renders SAN move pairs in a lichess-style two-column list. currentPly
// counts from 0 (starting position) — ply N means "after N half-moves
// have been played." Clicking a move (in replay mode) jumps to the
// position right after that move via onSelectPly.
export default function MoveList({ sanMoves, currentPly, onSelectPly }) {
  const rows = []
  for (let i = 0; i < sanMoves.length; i += 2) {
    rows.push({ number: i / 2 + 1, white: sanMoves[i], black: sanMoves[i + 1] })
  }

  return (
    <div className="move-list">
      {rows.length === 0 && <p className="muted">No moves yet.</p>}
      {rows.map((row) => {
        const whitePly = row.number * 2 - 1
        const blackPly = row.number * 2
        return (
          <div className="move-row" key={row.number}>
            <span className="move-number">{row.number}.</span>
            <button
              className={`move-btn ${currentPly === whitePly ? 'active' : ''}`}
              onClick={() => onSelectPly?.(whitePly)}
              disabled={!onSelectPly}
            >
              {row.white}
            </button>
            {row.black && (
              <button
                className={`move-btn ${currentPly === blackPly ? 'active' : ''}`}
                onClick={() => onSelectPly?.(blackPly)}
                disabled={!onSelectPly}
              >
                {row.black}
              </button>
            )}
          </div>
        )
      })}
    </div>
  )
}
