import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function NavBar() {
  const { username, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <nav className="navbar">
      <Link to={username ? '/home' : '/'} className="brand">♞ Chesstnut Bros</Link>
      <div className="nav-links">
        {username ? (
          <>
            <Link to="/home">Home</Link>
            <Link to="/games">History</Link>
            <span className="nav-user">{username}</span>
            {/* Not a redirect-away route — /login stays reachable while
                logged in specifically so a different tab's session
                doesn't need to be touched to log into another account
                in THIS tab. See client.js's sessionStorage note. */}
            <Link to="/login" className="btn-ghost">Switch account</Link>
            <button
              className="btn-ghost"
              onClick={() => {
                logout()
                navigate('/')
              }}
            >
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link to="/register" className="btn-primary-sm">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  )
}
