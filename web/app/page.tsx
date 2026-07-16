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

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null)
    })

    return () => subscription.unsubscribe()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return <LoginPage supabase={supabase} />
  }

  return <DashboardPage user={user} supabase={supabase} />
}

function LoginPage({ supabase }: { supabase: any }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const { error } = isSignUp
      ? await supabase.auth.signUp({ email, password })
      : await supabase.auth.signInWithPassword({ email, password })

    if (error) {
      setError(error.message)
    }
    setLoading(false)
  }

  const handleTelegramLogin = async () => {
    // For Telegram Mini App
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const initData = (window as any).Telegram?.WebApp?.initData
    if (initData) {
      await fetch('/api/auth/telegram', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData }),
      })
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">LifeOS</h1>
        <p className="text-gray-500 text-center mb-8">AI Personal Operating System</p>

        <form onSubmit={handleAuth} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
          
          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-500 text-white py-3 rounded-lg font-semibold hover:bg-indigo-600 disabled:opacity-50"
          >
            {loading ? 'Loading...' : isSignUp ? 'Sign Up' : 'Sign In'}
          </button>
        </form>

        <div className="mt-4 text-center">
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-indigo-500 hover:underline"
          >
            {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
          </button>
        </div>

        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="bg-white px-2 text-gray-500">or</span>
            </div>
          </div>

          <button
            onClick={handleTelegramLogin}
            className="w-full mt-4 bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 flex items-center justify-center gap-2"
          >
            <span>Open in Telegram</span>
          </button>
        </div>
      </div>
    </div>
  )
}

function DashboardPage({ user, supabase }: { user: any; supabase: any }) {
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
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <DashboardCard title="Tasks" value="3" subtitle="to do today" color="blue" />
          <DashboardCard title="Habits" value="2/5" subtitle="completed" color="orange" />
          <DashboardCard title="Expenses" value="$45" subtitle="today" color="green" />
        </div>
        
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">AI Assistant</h2>
          <ChatInterface userId={user.id} />
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

function ChatInterface({ userId }: { userId: string }) {
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
        body: JSON.stringify({ message, userId }),
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
