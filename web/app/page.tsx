'use client'

import { useState } from 'react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">LifeOS</h1>
          <span className="text-gray-500">AI Personal Operating System</span>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <DashboardCard title="Tasks" value="3" subtitle="to do today" color="blue" />
          <DashboardCard title="Habits" value="2/5" subtitle="completed" color="orange" />
          <DashboardCard title="Expenses" value="$45" subtitle="today" color="green" />
        </div>
        
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">AI Assistant</h2>
          <ChatInterface />
        </div>
      </main>
    </div>
  )
}

function DashboardCard({ title, value, subtitle, color }: { title: string; value: string; subtitle: string; color: string }) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-50 text-blue-600',
    orange: 'bg-orange-50 text-orange-600',
    green: 'bg-green-50 text-green-600',
  }
  
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium mb-2 ${colors[color]}`}>
        {title}
      </div>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
      <p className="text-gray-400 text-sm">{subtitle}</p>
    </div>
  )
}

function ChatInterface() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<{role: string; content: string}[]>([
    { role: 'assistant', content: "Hi! I'm your LifeOS AI assistant. Try:\n• \"I spent 200 on food\"\n• \"Remind me tomorrow at 9\"\n• \"Add task: buy groceries\"" }
  ])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!message.trim() || loading) return

    const userMessage = { role: 'user', content: message }
    setMessages(prev => [...prev, userMessage])
    setMessage('')
    setLoading(true)

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })

      const data = await response.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.response || data.error || 'Error occurred' }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not connect to AI' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="h-80 overflow-y-auto mb-4 space-y-3 p-4 bg-gray-50 rounded-lg">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-[85%] whitespace-pre-wrap ${
              msg.role === 'user'
                ? 'bg-indigo-500 text-white ml-auto'
                : 'bg-white border'
            }`}
          >
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="bg-white border p-3 rounded-lg max-w-[85%]">
            Thinking...
          </div>
        )}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          className="flex-1 border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-indigo-500 text-white px-6 py-3 rounded-lg hover:bg-indigo-600 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  )
}
