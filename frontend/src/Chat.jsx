
import { useState } from 'react'
import './Chat.css'

function Chat() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()

    if (!question.trim() || loading) return

    const currentQuestion = question.trim()

    setQuestion('')
    setError('')
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentQuestion,
          history: messages,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get a response from NageshAI.')
      }

      const data = await response.json()

      setMessages((previousMessages) => [
        ...previousMessages,
        { role: 'user', content: currentQuestion },
        { role: 'assistant', content: data.answer },
      ])

    } catch (err) {
      setError(err.message || 'Something went wrong.')
      setQuestion(currentQuestion)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-container">

      <div className="chat-heading">
        <div>
          <h1>Chat with NageshAI</h1>
          <p>Ask anything about Nagesh's professional profile.</p>
        </div>
      </div>

      <div className="chat-messages">

        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <div className="chat-empty-icon">✦</div>
            <h2>How can I help you?</h2>
            <p>
              Ask me about Nagesh's education, technical skills,
              projects or professional background.
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role}`}
          >
            <div className="message-label">
              {message.role === 'user' ? 'You' : 'NageshAI'}
            </div>

            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-label">NageshAI</div>
            <div className="message-content typing">
              Thinking...
            </div>
          </div>
        )}

        {error && (
          <div className="chat-error">
            {error}
          </div>
        )}

      </div>

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask something about Nagesh..."
          disabled={loading}
        />

        <button
          type="submit"
          disabled={!question.trim() || loading}
        >
          {loading ? 'Sending...' : 'Send ↑'}
        </button>
      </form>

      <p className="chat-disclaimer">
        NageshAI provides answers based on the candidate's profile.
      </p>

    </div>
  )
}

export default Chat
