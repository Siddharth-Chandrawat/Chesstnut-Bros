import { Chessboard } from 'react-chessboard'

const LIGHT_SQUARE = '#eeeed2'
const DARK_SQUARE = '#769656'
const LAST_MOVE_HIGHLIGHT = 'rgba(226, 183, 20, 0.55)'

export default function ChessBoardView({
  fen,
  onPieceDrop,
  boardOrientation = 'white',
  arePiecesDraggable = true,
  lastMove,
  boardWidth = 440,
}) {
  const customSquareStyles = {}
  if (lastMove) {
    customSquareStyles[lastMove.from] = { backgroundColor: LAST_MOVE_HIGHLIGHT }
    customSquareStyles[lastMove.to] = { backgroundColor: LAST_MOVE_HIGHLIGHT }
  }

  return (
    <div className="board-shell">
      <Chessboard
        position={fen}
        onPieceDrop={onPieceDrop}
        boardOrientation={boardOrientation}
        arePiecesDraggable={arePiecesDraggable}
        boardWidth={boardWidth}
        customDarkSquareStyle={{ backgroundColor: DARK_SQUARE }}
        customLightSquareStyle={{ backgroundColor: LIGHT_SQUARE }}
        customSquareStyles={customSquareStyles}
        animationDuration={200}
      />
    </div>
  )
}
