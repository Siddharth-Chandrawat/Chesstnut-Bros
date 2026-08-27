export default function ReplayControls({ currentPly, maxPly, onChange }) {
  return (
    <div className="replay-controls">
      <button onClick={() => onChange(0)} disabled={currentPly === 0} title="First position">⏮</button>
      <button
        onClick={() => onChange(Math.max(0, currentPly - 1))}
        disabled={currentPly === 0}
        title="Previous move"
      >
        ◀
      </button>
      <span className="replay-position">{currentPly} / {maxPly}</span>
      <button
        onClick={() => onChange(Math.min(maxPly, currentPly + 1))}
        disabled={currentPly === maxPly}
        title="Next move"
      >
        ▶
      </button>
      <button onClick={() => onChange(maxPly)} disabled={currentPly === maxPly} title="Last position">⏭</button>
    </div>
  )
}
