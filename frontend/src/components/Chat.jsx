import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

function Chat({ API }) {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hi! I am the UPES Student Assistant. How can I help you today?' }
  ])
  const [input, setInput] = useState('')
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [showSubmit, setShowSubmit] = useState(false)
  const [submitData, setSubmitData] = useState({ question: '', answer: '', category: '' })
  const [submitMsg, setSubmitMsg] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    axios.get(`${API}/categories`).then(res => setCategories(res.data))
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const question = input.trim()
    setInput('')
    setShowSubmit(false)
    setSubmitMsg('')

    const newMessages = [...messages, { from: 'user', text: question }]
    setMessages(newMessages)
    setLoading(true)

    try {
      const res = await axios.post(`${API}/chat`, {
        question,
        category: selectedCategory || null,
        history: newMessages.slice(-10)
      })

      if (res.data.matched) {
        setMessages(prev => [...prev, { from: 'bot', text: res.data.answer }])
        setShowSubmit(false)
      } else {
        setMessages(prev => [...prev, { from: 'bot', text: res.data.message }])
        setShowSubmit(true)
        setSubmitData(prev => ({ ...prev, question }))
      }
    } catch {
      setMessages(prev => [...prev, { from: 'bot', text: 'Something went wrong. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!submitData.answer || !submitData.category) return
    try {
      const res = await axios.post(`${API}/submit`, submitData)
      setSubmitMsg(res.data.message)
      setShowSubmit(false)
    } catch {
      setSubmitMsg('Failed to submit. Try again.')
    }
  }

  return (
    <div className="chat-container">
      <div className="category-bar">
        <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}>
          <option value="">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.from}`}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        {submitMsg && <div className="submit-msg">{submitMsg}</div>}
        <div ref={bottomRef} />
      </div>

      {showSubmit && (
        <div className="submit-box">
          <p>Know the answer? Help other UPES students by submitting it below.</p>
          <select onChange={e => setSubmitData(prev => ({ ...prev, category: e.target.value }))}>
            <option value="">Select category</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <textarea
            placeholder="Type the answer here..."
            onChange={e => setSubmitData(prev => ({ ...prev, answer: e.target.value }))}
          />
          <button onClick={handleSubmit}>Submit Answer</button>
        </div>
      )}

      <div className="input-bar">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question about UPES..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default Chat