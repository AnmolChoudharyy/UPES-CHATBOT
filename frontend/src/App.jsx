import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import Chat from './components/Chat'
import Admin from './components/Admin'
import './App.css'

const API = 'http://127.0.0.1:5000'

function App() {
  const [page, setPage] = useState('chat')

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <div className="logo">UPES</div>
          <div>
            <div className="header-title">Student Assistant</div>
            <div className="header-sub">Dehradun Campus</div>
          </div>
        </div>
        <nav>
          <button onClick={() => setPage('chat')} className={page === 'chat' ? 'active' : ''}>Chat</button>
          <button onClick={() => setPage('admin')} className={page === 'admin' ? 'active' : ''}>Admin</button>
        </nav>
      </header>
      <main>
        {page === 'chat' ? <Chat API={API} /> : <Admin API={API} />}
      </main>
    </div>
  )
}

export default App