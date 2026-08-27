// Maps between chess.js's algebraic squares ("e4") and the server's
// 0-63 board indices. index = row*8+col, row 0 = rank 8 — this is
// the convention chesstnut's board_to_fen()/readFen() use (row 0 is
// the first rank written in a FEN string, i.e. rank 8 on a standard
// board), so it must match exactly on this side too.

export function algebraicToIndex(square) {
  const file = square.charCodeAt(0) - 'a'.charCodeAt(0) // 0-7
  const rank = parseInt(square[1], 10) // 1-8
  const row = 8 - rank
  return row * 8 + file
}

export function indexToAlgebraic(index) {
  const row = Math.floor(index / 8)
  const col = index % 8
  const file = String.fromCharCode('a'.charCodeAt(0) + col)
  const rank = 8 - row
  return `${file}${rank}`
}
