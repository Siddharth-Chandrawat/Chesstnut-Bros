const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const TOKEN_KEY = 'chesstnut_token'
const USERNAME_KEY = 'chesstnut_username'

// sessionStorage, not localStorage: localStorage is shared across every
// tab of the same origin, so logging in as a second user in another tab
// would silently overwrite the first tab's session. sessionStorage is
// scoped per tab, so opening a second tab and logging in as a different
// user there leaves the first tab's session untouched — this is what
// actually enables testing two concurrent users locally.
//
// Caveat: some browsers copy sessionStorage into a tab opened via
// "duplicate tab." Open a fresh tab (new tab + type/paste the URL, or a
// separate incognito/private window) for guaranteed isolation between
// two accounts.

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY)
}
export function setToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token)
}
export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(USERNAME_KEY)
}
export function setStoredUsername(username) {
  sessionStorage.setItem(USERNAME_KEY, username)
}
export function getStoredUsername() {
  return sessionStorage.getItem(USERNAME_KEY)
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

async function request(path, { method = 'GET', body, form, auth = true } = {}) {
  const headers = {}
  let payload = body

  if (form) {
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    payload = new URLSearchParams(body).toString()
  } else if (body) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  if (auth) {
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
  }

  const resp = await fetch(`${API_BASE}${path}`, { method, headers, body: payload })

  if (!resp.ok) {
    let detail = resp.statusText
    try {
      const data = await resp.json()
      detail = data.detail || detail
    } catch {
      /* body wasn't JSON — fall back to statusText */
    }
    throw new ApiError(detail, resp.status)
  }
  if (resp.status === 204) return null
  return resp.json()
}

export const api = {
  register: (username, password) =>
    request('/register', { method: 'POST', body: { username, password }, auth: false }),
  login: (username, password) =>
    request('/login', { method: 'POST', body: { username, password }, form: true, auth: false }),
  newGame: () => request('/games', { method: 'POST' }),
  listGames: () => request('/games'),
  getGame: (gameId) => request(`/games/${gameId}`),
  submitMove: (gameId, fromSq, toSq) =>
    request(`/games/${gameId}/move`, { method: 'POST', body: { from_sq: fromSq, to_sq: toSq } }),
  resignGame: (gameId) => request(`/games/${gameId}/resign`, { method: 'POST' }),
  undoMove: (gameId) => request(`/games/${gameId}/undo`, { method: 'POST' }),
}