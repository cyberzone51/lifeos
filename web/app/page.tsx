'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export default function Home() {
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
      setLoading(false)
    }
    getUser()
  }, [])

  const handleTelegramLogin = async () => {
    // Telegram Mini App sends initData
    // We'll verify it on the server
    const initData = window.Telegram?.WebApp?.initData
    
    if (initData) {
      const response = await fetch('/api/auth/telegram', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData }),
      })
      
      const data = await response.json()
      if (data.session) {
        window.location.reload()
      }
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-4">LifeOS</h1>
          <p className="text-white/80 mb-8">AI Personal Operating System</p>
          <button
            onClick={handleTelegramLogin}
            className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-white/90 transition"
          >
            Open in Telegram
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">LifeOS</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user.email}</span>
            <button
              onClick={() => supabase.auth.signOut()}
              className="text-red-500 hover:text-red-600"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <DashboardCard title="Tasks" value="3" subtitle="to do today" />
          <DashboardCard title="Habits" value="2/5" subtitle="completed" />
          <DashboardCard title="Expenses" value="$45" subtitle="today" />
        </div>
        
        <div className="mt-8 bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">AI Assistant</h2>
          <ChatInterface userId={user.id} />
        </div>
      </main>
    </div>
  )
}

function DashboardCard({ title, value, subtitle }: { title: string; value: string; subtitle: string }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-gray-500 text-sm">{title}</h3>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
      <p className="text-gray-400 text-sm">{subtitle}</p>
    </div>
  )
}

function ChatInterface({ userId }: { userId: string }) {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<{role: string; content: string}[]>([])

  const sendMessage = async () => {
    if (!message.trim()) return

    const userMessage = { role: 'user', content: message }
    setMessages(prev => [...prev, userMessage])
    setMessage('')

    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, userId }),
    })

    const data = await response.json()
    setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
  }

  return (
    <div>
      <div className="h-64 overflow-y-auto mb-4 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg ${
              msg.role === 'user'
                ? 'bg-indigo-100 ml-auto max-w-[80%]'
                : 'bg-gray-100 max-w-[80%]'
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          className="flex-1 border rounded-lg px-4 py-2"
        />
        <button
          onClick={sendMessage}
          className="bg-indigo-500 text-white px-6 py-2 rounded-lg hover:bg-indigo-600"
        >
          Send
        </button>
      </div>
    </div>
  )
}
