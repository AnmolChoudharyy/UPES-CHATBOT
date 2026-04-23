import { useState, useEffect } from 'react'
import axios from 'axios'

function Admin({ API }) {
  const [loggedIn, setLoggedIn] = useState(false)
  const [creds, setCreds] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [pending, setPending] = useState([])
  const [msg, setMsg] = useState('')

  const login = async () => {
    try {
      const res = await axios.post(`${API}/admin/login`, creds, { withCredentials: true })
      if (res.data.success) {
        setLoggedIn(true)
        loadPending()
      }
    } catch {
      setError('Invalid username or password')
    }
  }

  const loadPending = async () => {
    const res = await axios.get(`${API}/admin/pending`, { withCredentials: true })
    setPending(res.data)
  }

  const approve = async (id) => {
    await axios.post(`${API}/admin/approve/${id}`, {}, { withCredentials: true })
    setMsg('Approved successfully')
    loadPending()
  }

  const reject = async (id) => {
    await axios.post(`${API}/admin/reject/${id}`, {}, { withCredentials: true })
    setMsg('Rejected and removed')
    loadPending()
  }

  const logout = async () => {
    await axios.post(`${API}/admin/logout`, {}, { withCredentials: true })
    setLoggedIn(false)
  }

  if (!loggedIn) {
    return (
      <div className="admin-login">
        <h2>Admin Login</h2>
        <input
          placeholder="Username"
          onChange={e => setCreds(p => ({ ...p, username: e.target.value }))}
        />
        <input
          type="password"
          placeholder="Password"
          onChange={e => setCreds(p => ({ ...p, password: e.target.value }))}
        />
        {error && <p className="error">{error}</p>}
        <button onClick={login}>Login</button>
      </div>
    )
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h2>Pending Submissions</h2>
        <button onClick={logout}>Logout</button>
      </div>
      {msg && <p className="success-msg">{msg}</p>}
      {pending.length === 0 ? (
        <p className="empty">No pending submissions right now.</p>
      ) : (
        pending.map(p => (
          <div key={p.id} className="pending-card">
            <div className="pending-category">{p.category}</div>
            <div className="pending-question"><strong>Q:</strong> {p.question}</div>
            <div className="pending-answer"><strong>A:</strong> {p.answer}</div>
            <div className="pending-actions">
              <button className="approve" onClick={() => approve(p.id)}>Approve</button>
              <button className="reject" onClick={() => reject(p.id)}>Reject</button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}

export default Admin