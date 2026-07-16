'use client'

import { useState, useEffect } from 'react'

type Task = { id: number; title: string; done: boolean }
type Expense = { id: number; amount: number; category: string; description: string }
type Habit = { id: number; name: string; done: boolean; streak: number }

export default function Home() {
  const [tab, setTab] = useState<'chat' | 'tasks' | 'finance' | 'habits'>('chat')
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, title: 'Buy groceries', done: false },
    { id: 2, title: 'Call dentist', done: false },
    { id: 3, title: 'Finish project', done: true },
  ])
  const [expenses, setExpenses] = useState<Expense[]>([
    { id: 1, amount: 25, category: 'Food', description: 'Lunch' },
    { id: 2, amount: 15, category: 'Transport', description: 'Taxi' },
  ])
  const [habits, setHabits] = useState<Habit[]>([
    { id: 1, name: 'Water 8 glasses', done: false, streak: 5 },
    { id: 2, name: 'Exercise 30min', done: true, streak: 12 },
    { id: 3, name: 'Read 20 pages', done: false, streak: 3 },
    { id: 4, name: 'Sleep 8 hours', done: true, streak: 7 },
  ])

  const toggleTask = (id: number) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  const toggleHabit = (id: number) => {
    setHabits(habits.map(h => h.id === id ? { ...h, done: !h.done } : h))
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-indigo-600 text-white p-4 shadow-lg">
        <h1 className="text-xl font-bold">LifeOS</h1>
        <p className="text-indigo-200 text-sm">AI Personal Operating System</p>
      </header>

      <nav className="bg-white shadow flex overflow-x-auto">
        {(['chat', 'tasks', 'finance', 'habits'] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-6 py-3 font-medium whitespace-nowrap ${
              tab === t 
                ? 'text-indigo-600 border-b-2 border-indigo-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {t === 'chat' ? 'AI Chat' : t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </nav>

      <main className="max-w-4xl mx-auto p-4">
        {tab === 'chat' && <ChatTab />}
        {tab === 'tasks' && <TasksTab tasks={tasks} toggleTask={toggleTask} />}
        {tab === 'finance' && <FinanceTab expenses={expenses} />}
        {tab === 'habits' && <HabitsTab habits={habits} toggleHabit={toggleHabit} />}
      </main>
    </div>
  )
}

function ChatTab() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<{role: string; content: string}[]>([
    { role: 'assistant', content: 'Привет! Я твой AI ассистент LifeOS.\n\nПопробуй:\n• "Потратил 200 на еду"\n• "Напомни завтра в 9"\n• "Добавь задачу купить молоко"\n• "Сколько я потратил сегодня?"' }
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
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Ошибка соединения с AI' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-sm">
      <div className="h-[500px] overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-2xl whitespace-pre-wrap ${
                msg.role === 'user'
                  ? 'bg-indigo-500 text-white rounded-br-md'
                  : 'bg-gray-100 text-gray-800 rounded-bl-md'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-2xl rounded-bl-md">
              Думаю...
            </div>
          </div>
        )}
      </div>
      <div className="border-t p-4 flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Напиши сообщение..."
          className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-indigo-500 text-white px-6 py-2 rounded-full hover:bg-indigo-600 disabled:opacity-50"
        >
          Отправить
        </button>
      </div>
    </div>
  )
}

function TasksTab({ tasks, toggleTask }: { tasks: Task[]; toggleTask: (id: number) => void }) {
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Задачи</h2>
        <span className="text-gray-500">{tasks.filter(t => !t.done).length} активных</span>
      </div>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {tasks.map(task => (
          <div key={task.id} className="flex items-center p-4 gap-3">
            <input
              type="checkbox"
              checked={task.done}
              onChange={() => toggleTask(task.id)}
              className="w-5 h-5 text-indigo-500 rounded"
            />
            <span className={task.done ? 'line-through text-gray-400' : ''}>
              {task.title}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

function FinanceTab({ expenses }: { expenses: Expense[] }) {
  const total = expenses.reduce((sum, e) => sum + e.amount, 0)
  
  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl p-6">
        <p className="text-green-100">Расходы сегодня</p>
        <p className="text-4xl font-bold">${total}</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {expenses.map(exp => (
          <div key={exp.id} className="flex justify-between items-center p-4">
            <div>
              <p className="font-medium">{exp.description}</p>
              <p className="text-sm text-gray-500">{exp.category}</p>
            </div>
            <span className="text-red-500 font-semibold">-${exp.amount}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function HabitsTab({ habits, toggleHabit }: { habits: Habit[]; toggleHabit: (id: number) => void }) {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Привычки</h2>
      <div className="grid grid-cols-2 gap-4">
        {habits.map(habit => (
          <div
            key={habit.id}
            onClick={() => toggleHabit(habit.id)}
            className={`bg-white rounded-xl shadow-sm p-4 cursor-pointer transition ${
              habit.done ? 'ring-2 ring-green-500' : ''
            }`}
          >
            <div className="flex justify-between items-start">
              <p className="font-medium">{habit.name}</p>
              {habit.done && <span className="text-green-500 text-xl">✓</span>}
            </div>
            <p className="text-sm text-gray-500 mt-2">🔥 {habit.streak} дней подряд</p>
          </div>
        ))}
      </div>
    </div>
  )
}
