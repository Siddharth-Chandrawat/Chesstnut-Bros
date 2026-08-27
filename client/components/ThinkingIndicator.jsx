export default function ThinkingIndicator({ label = 'Chesstnut is thinking…' }) {
  return (
    <div className="thinking">
      <span className="thinking-dot" />
      <span className="thinking-dot" />
      <span className="thinking-dot" />
      <span className="thinking-label">{label}</span>
    </div>
  )
}
