import { Link } from 'react-router-dom'
import NavBar from '../components/NavBar'
import { useAuth } from '../context/AuthContext'

export default function LandingPage() {
  const { username } = useAuth()

  return (
    <div className="page fade-in">
      <NavBar />
      <section className="hero">
        {username ? (
          <>
            <h1>Welcome back, {username}.</h1>
            <p className="hero-sub">
              This tab is signed in and ready to go — jump back into your
              dashboard, or use "Switch account" above to sign into a
              different account in this tab without affecting any other
              tab you have open.
            </p>
            <div className="hero-actions">
              <Link to="/home" className="btn-primary">Go to your dashboard</Link>
            </div>
          </>
        ) : (
          <>
            <h1>Play chess against an engine built from scratch.</h1>
            <p className="hero-sub">
              No third-party chess library, no borrowed engine — Chesstnut
              searches every move itself. Create a free account and see
              how far you can push it.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="btn-primary">Create free account</Link>
              <Link to="/login" className="btn-ghost">I already have one</Link>
            </div>
          </>
        )}
      </section>
      <section className="hero-board-preview">
        <div className="preview-board" aria-hidden="true">
          {Array.from({ length: 64 }).map((_, i) => {
            const row = Math.floor(i / 8)
            const col = i % 8
            const dark = (row + col) % 2 === 1
            return <div key={i} className={dark ? 'sq-dark' : 'sq-light'} />
          })}
        </div>
      </section>
    </div>
  )
}
