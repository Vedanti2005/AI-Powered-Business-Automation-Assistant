import { useEffect, useRef, useState } from 'react'
import ChatbotPanel from './components/ChatbotPanel.jsx'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const CHAT_SESSION_KEY = 'codenixia.chat.sessionId'

const defaultChatMessages = [
  {
    role: 'assistant',
    content: 'Hi, I am Codenixia AI. Ask me anything and I will respond here.',
    timestamp: new Date().toISOString(),
  },
]

const getStoredSessionId = () => {
  if (typeof window === 'undefined') return ''
  return localStorage.getItem(CHAT_SESSION_KEY) ?? ''
}

const generateSessionId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }

  return `session_${Date.now()}_${Math.random().toString(16).slice(2)}`
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  const payloadText = await response.text()
  const payload = payloadText ? JSON.parse(payloadText) : null

  if (!response.ok) {
    const message = payload?.detail || payload?.message || `Request failed (${response.status})`
    throw new Error(message)
  }

  return payload
}

function App() {
  const [sessionId, setSessionId] = useState(getStoredSessionId())
  const [chatMessages, setChatMessages] = useState(defaultChatMessages)
  const [chatInput, setChatInput] = useState('')
  const [chatSending, setChatSending] = useState(false)
  const [chatNotice, setChatNotice] = useState('')

  const chatEndRef = useRef(null)

  useEffect(() => {
    if (!sessionId) {
      const newSessionId = generateSessionId()
      localStorage.setItem(CHAT_SESSION_KEY, newSessionId)
      setSessionId(newSessionId)
      return
    }

    const loadChatHistory = async () => {
      try {
        const history = await apiRequest(`/api/chat/history/${sessionId}`)
        setChatMessages(history.messages?.length ? history.messages : defaultChatMessages)
      } catch {
        setChatMessages(defaultChatMessages)
      }
    }

    loadChatHistory()
  }, [sessionId])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [chatMessages])

  const handleSendChat = async (event) => {
    event.preventDefault()
    const trimmedMessage = chatInput.trim()
    if (!trimmedMessage || chatSending) return

    const userMessage = {
      role: 'user',
      content: trimmedMessage,
      timestamp: new Date().toISOString(),
    }

    setChatSending(true)
    setChatNotice('')
    setChatMessages((current) => [...current, userMessage])
    setChatInput('')

    try {
      const response = await apiRequest('/api/chat/message', {
        method: 'POST',
        body: JSON.stringify({
          session_id: sessionId,
          message: trimmedMessage,
        }),
      })

      if (response.session_id && response.session_id !== sessionId) {
        localStorage.setItem(CHAT_SESSION_KEY, response.session_id)
        setSessionId(response.session_id)
      }

      setChatMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: response.reply,
          timestamp: response.timestamp,
        },
      ])
    } catch (error) {
      setChatNotice(error.message)
      setChatMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: error.message,
          timestamp: new Date().toISOString(),
        },
      ])
    } finally {
      setChatSending(false)
    }
  }

  const clearChat = async () => {
    if (!sessionId) return

    try {
      await apiRequest(`/api/chat/history/${sessionId}`, { method: 'DELETE' })
    } catch {
      // ignore backend delete failures and still reset the UI
    }

    const newSessionId = generateSessionId()
    localStorage.setItem(CHAT_SESSION_KEY, newSessionId)
    setSessionId(newSessionId)
    setChatMessages(defaultChatMessages)
    setChatNotice('Chat cleared.')
  }

  return (
    <div className="chat-app-shell">
      <header className="chat-header">
        <div>
          <p className="chat-kicker">Codenixia AI</p>
          <h1>Chat with the assistant</h1>
        </div>
        <button className="ghost-button" type="button" onClick={clearChat}>
          New chat
        </button>
      </header>

      <main className="chat-stage">
        <ChatbotPanel
          chatMessages={chatMessages}
          chatInput={chatInput}
          chatSending={chatSending}
          chatNotice={chatNotice}
          chatEndRef={chatEndRef}
          onInputChange={setChatInput}
          onSubmit={handleSendChat}
          onClear={clearChat}
        />
      </main>
    </div>
  )
}

export default App
