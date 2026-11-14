
import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './Chat.css'

function Chat() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const latestAssistantRef = useRef(null)

  useEffect(() => {
    latestAssistantRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }, [messages])

  async function handleSubmit(event) {
    event.preventDefault()

    if (!question.trim() || loading) return

    const currentQuestion = question.trim()

    setQuestion('')
    setError('')
    setLoading(true)

    // Add the user question and an empty assistant message
    const updatedMessages = [
      ...messages,
      { role: 'user', content: currentQuestion },
      { role: 'assistant', content: '' },
    ]

    setMessages(updatedMessages)

    try {
      const response = await fetch('http://127.0.0.1:8000/chat/stream', {
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

      if (!response.body) {
        throw new Error('Streaming response is not supported by this browser.')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { value, done } = await reader.read()

        if (done) break

        const chunk = decoder.decode(value, { stream: true })

        setMessages((previousMessages) => {
          const updated = [...previousMessages]
          const lastIndex = updated.length - 1

          updated[lastIndex] = {
            ...updated[lastIndex],
            content: updated[lastIndex].content + chunk,
          }

          return updated
        })
      }

      const remaining = decoder.decode()

      if (remaining) {
        setMessages((previousMessages) => {
          const updated = [...previousMessages]
          const lastIndex = updated.length - 1

          updated[lastIndex] = {
            ...updated[lastIndex],
            content: updated[lastIndex].content + remaining,
          }

          return updated
        })
      }

    } catch (err) {
      setError(err.message || 'Something went wrong.')
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
            ref={
              message.role === 'assistant' &&
              index === messages.length - 1
                ? latestAssistantRef
                : null
            }
            className={`message ${message.role}`}
          >
            <div className="message-label">
              {message.role === 'user' ? 'You' : 'NageshAI'}
            </div>

            <div className="message-content">
              {message.role === 'assistant' ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              ) : (
                message.content
              )}
            </div>
          </div>
        ))}

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
          {loading ? 'Generating...' : 'Send ↑'}
        </button>
      </form>

      <p className="chat-disclaimer">
        NageshAI provides answers based on the candidate's profile.
      </p>

    </div>
  )
}

export default Chat
