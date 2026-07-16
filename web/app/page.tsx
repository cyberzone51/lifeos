'use client'

import { useState } from 'react'

type Tab = 'assistant' | 'tasks' | 'finance' | 'habits' | 'goals' | 'journal' | 'health' | 'shopping' | 'assets' | 'settings'

type Task = { id: number; title: string; done: boolean; priority: 'high' | 'medium' | 'low' }
type Expense = { id: number; amount: number; category: string; description: string; date: string }
type Habit = { id: number; name: string; done: boolean; streak: number; icon: string }
type Goal = { id: number; title: string; progress: number; target: number; unit: string }
type JournalEntry = { id: number; date: string; mood: number; text: string }
type ShoppingItem = { id: number; name: string; checked: boolean; price: number }

export default function Home() {
  const [tab, setTab] = useState<Tab>('assistant')
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, title: 'Купить продукты', done: false, priority: 'high' },
    { id: 2, title: 'Позвонить маме', done: false, priority: 'medium' },
    { id: 3, title: 'Оплатить аренду', done: true, priority: 'high' },
    { id: 4, title: 'Пробежка 5 км', done: false, priority: 'low' },
  ])
  const [expenses, setExpenses] = useState<Expense[]>([
    { id: 1, amount: 350, category: 'Еда', description: 'Обед в кафе', date: 'Сегодня' },
    { id: 2, amount: 120, category: 'Транспорт', description: 'Метро', date: 'Сегодня' },
    { id: 3, amount: 2500, category: 'ЖКХ', description: 'Электричество', date: 'Вчера' },
  ])
  const [habits, setHabits] = useState<Habit[]>([
    { id: 1, name: 'Вода 8 стаканов', done: false, streak: 12, icon: '💧' },
    { id: 2, name: 'Спорт 30 мин', done: true, streak: 5, icon: '🏃' },
    { id: 3, name: 'Чтение 20 стр', done: false, streak: 8, icon: '📚' },
    { id: 4, name: 'Медитация', done: false, streak: 3, icon: '🧘' },
    { id: 5, name: 'Сон 8 часов', done: true, streak: 15, icon: '😴' },
    { id: 6, name: 'Язык 15 мин', done: false, streak: 7, icon: '🌍' },
  ])
  const [goals, setGoals] = useState<Goal[]>([
    { id: 1, title: 'Накопить 100 000 ₽', progress: 35000, target: 100000, unit: '₽' },
    { id: 2, title: 'Похудеть на 5 кг', progress: 2, target: 5, unit: 'кг' },
    { id: 3, title: 'Прочитать 24 книги', progress: 18, target: 24, unit: 'книг' },
  ])
  const [journal, setJournal] = useState<JournalEntry[]>([
    { id: 1, date: 'Сегодня', mood: 8, text: 'Хороший день. Сделал много дел. Вечером пошёл в кино.' },
    { id: 2, date: 'Вчера', mood: 6, text: 'Обычный день. Работа была напряжённой.' },
  ])
  const [shopping, setShopping] = useState<ShoppingItem[]>([
    { id: 1, name: 'Молоко', checked: false, price: 80 },
    { id: 2, name: 'Хлеб', checked: true, price: 50 },
    { id: 3, name: 'Яйца', checked: false, price: 120 },
    { id: 4, name: 'Курица', checked: false, price: 250 },
  ])

  const toggleTask = (id: number) => setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  const toggleHabit = (id: number) => setHabits(habits.map(h => h.id === id ? { ...h, done: !h.done } : h))
  const toggleShopping = (id: number) => setShopping(shopping.map(s => s.id === id ? { ...s, checked: !s.checked } : s))

  const totalExpenses = expenses.reduce((s, e) => s + e.amount, 0)
  const shoppingTotal = shopping.filter(s => !s.checked).reduce((s, i) => s + i.price, 0)
  const habitsDone = habits.filter(h => h.done).length

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 shadow-lg">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold">🧠 LifeOS</h1>
            <p className="text-indigo-200 text-xs">AI Personal Operating System</p>
          </div>
          <div className="flex gap-4 text-sm">
            <span>🔥 12 days</span>
            <span>⭐ Level 8</span>
            <span>💎 2,450 XP</span>
          </div>
        </div>
      </header>

      <nav className="bg-white shadow flex overflow-x-auto max-w-6xl mx-auto">
        {([
          ['assistant', '🤖 AI'],
          ['tasks', '📋 Tasks'],
          ['finance', '💰 Finance'],
          ['habits', '🔥 Habits'],
          ['goals', '🎯 Goals'],
          ['journal', '📖 Journal'],
          ['health', '❤️ Health'],
          ['shopping', '🛒 Shopping'],
          ['assets', '🚗 Assets'],
          ['settings', '⚙️ Settings'],
        ] as [Tab, string][]).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={`px-4 py-3 font-medium whitespace-nowrap text-sm ${
              tab === key 
                ? 'text-indigo-600 border-b-2 border-indigo-600 bg-indigo-50' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {label}
          </button>
        ))}
      </nav>

      <main className="max-w-6xl mx-auto p-4">
        {tab === 'assistant' && <AssistantTab />}
        {tab === 'tasks' && <TasksTab tasks={tasks} toggleTask={toggleTask} />}
        {tab === 'finance' && <FinanceTab expenses={expenses} total={totalExpenses} />}
        {tab === 'habits' && <HabitsTab habits={habits} toggleHabit={toggleHabit} done={habitsDone} />}
        {tab === 'goals' && <GoalsTab goals={goals} />}
        {tab === 'journal' && <JournalTab entries={journal} />}
        {tab === 'health' && <HealthTab />}
        {tab === 'shopping' && <ShoppingTab items={shopping} toggle={toggleShopping} total={shoppingTotal} />}
        {tab === 'assets' && <AssetsTab />}
        {tab === 'settings' && <SettingsTab />}
      </main>
    </div>
  )
}

function AssistantTab() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<{role: string; content: string}[]>([
    { role: 'assistant', content: 'Доброе утро! 👋\n\nЯ твой AI ассистент. Вот что я знаю:\n\n📋 У тебя 3 задачи на сегодня\n🔥 Привычки: 2 из 6 выполнено\n💰 Расходы сегодня: 470 ₽\n\nПопробуй спросить:\n• "Что мне сегодня делать?"\n• "Потратил 200 на еду"\n• "Добавь задачу купить молоко"\n• "Как мои привычки?"' }
  ])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!message.trim() || loading) return
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setMessage('')
    setLoading(true)
    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Ошибка соединения' }])
    }
    setLoading(false)
  }

  return (
    <div className="bg-white rounded-xl shadow-sm">
      <div className="h-[500px] overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl whitespace-pre-wrap ${
              msg.role === 'user' ? 'bg-indigo-500 text-white rounded-br-md' : 'bg-gray-100 rounded-bl-md'
            }`}>{msg.content}</div>
          </div>
        ))}
        {loading && <div className="flex justify-start"><div className="bg-gray-100 p-3 rounded-2xl rounded-bl-md">Думаю...</div></div>}
      </div>
      <div className="border-t p-4 flex gap-2">
        <input type="text" value={message} onChange={e => setMessage(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Напиши сообщение..." className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        <button onClick={sendMessage} disabled={loading} className="bg-indigo-500 text-white px-6 py-2 rounded-full hover:bg-indigo-600">Отправить</button>
      </div>
    </div>
  )
}

function TasksTab({ tasks, toggleTask }: { tasks: Task[]; toggleTask: (id: number) => void }) {
  const priorityColors = { high: 'bg-red-500', medium: 'bg-yellow-500', low: 'bg-green-500' }
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">📋 Задачи</h2>
        <span className="text-gray-500">{tasks.filter(t => !t.done).length} активных</span>
      </div>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {tasks.map(task => (
          <div key={task.id} className="flex items-center p-4 gap-3">
            <input type="checkbox" checked={task.done} onChange={() => toggleTask(task.id)} className="w-5 h-5 text-indigo-500 rounded" />
            <div className={`w-2 h-2 rounded-full ${priorityColors[task.priority]}`}></div>
            <span className={task.done ? 'line-through text-gray-400' : ''}>{task.title}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function FinanceTab({ expenses, total }: { expenses: Expense[]; total: number }) {
  return (
    <div className="space-y-4">
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl p-6">
        <p className="text-green-100">Расходы сегодня</p>
        <p className="text-4xl font-bold">{total} ₽</p>
        <p className="text-green-200 text-sm mt-2">Бюджет: 5,000 ₽/день</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {expenses.map(exp => (
          <div key={exp.id} className="flex justify-between items-center p-4">
            <div>
              <p className="font-medium">{exp.description}</p>
              <p className="text-sm text-gray-500">{exp.category} • {exp.date}</p>
            </div>
            <span className="text-red-500 font-semibold">-{exp.amount} ₽</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function HabitsTab({ habits, toggleHabit, done }: { habits: Habit[]; toggleHabit: (id: number) => void; done: number }) {
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="font-medium">Прогресс сегодня</span>
          <span className="text-indigo-600 font-bold">{done}/{habits.length}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div className="bg-indigo-500 h-3 rounded-full transition-all" style={{ width: `${(done/habits.length)*100}%` }}></div>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        {habits.map(habit => (
          <div key={habit.id} onClick={() => toggleHabit(habit.id)}
            className={`bg-white rounded-xl shadow-sm p-4 cursor-pointer transition ${habit.done ? 'ring-2 ring-green-500 bg-green-50' : ''}`}>
            <div className="flex justify-between items-start">
              <span className="text-2xl">{habit.icon}</span>
              {habit.done && <span className="text-green-500 text-xl">✓</span>}
            </div>
            <p className="font-medium mt-2">{habit.name}</p>
            <p className="text-sm text-gray-500">🔥 {habit.streak} дней</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function GoalsTab({ goals }: { goals: Goal[] }) {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">🎯 Цели</h2>
      {goals.map(goal => (
        <div key={goal.id} className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="font-medium">{goal.title}</span>
            <span className="text-indigo-600 font-bold">{goal.progress}/{goal.target} {goal.unit}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className="bg-indigo-500 h-3 rounded-full transition-all" style={{ width: `${(goal.progress/goal.target)*100}%` }}></div>
          </div>
          <p className="text-sm text-gray-500 mt-2">Осталось {goal.target - goal.progress} {goal.unit}</p>
        </div>
      ))}
    </div>
  )
}

function JournalTab({ entries }: { entries: JournalEntry[] }) {
  const moodEmoji = (mood: number) => mood >= 8 ? '😊' : mood >= 6 ? '😐' : '😔'
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">📖 Журнал</h2>
      {entries.map(entry => (
        <div key={entry.id} className="bg-white rounded-xl shadow-sm p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-500">{entry.date}</span>
            <span className="text-2xl">{moodEmoji(entry.mood)}</span>
          </div>
          <p>{entry.text}</p>
        </div>
      ))}
    </div>
  )
}

function HealthTab() {
  const [sleep, setSleep] = useState(7.5)
  const [water, setWater] = useState(5)
  const [mood, setMood] = useState(7)
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">❤️ Здоровье</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-4 text-center">
          <span className="text-3xl">😴</span>
          <p className="text-2xl font-bold mt-2">{sleep}ч</p>
          <p className="text-sm text-gray-500">Сон</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 text-center">
          <span className="text-3xl">💧</span>
          <p className="text-2xl font-bold mt-2">{water}/8</p>
          <p className="text-sm text-gray-500">Вода</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 text-center">
          <span className="text-3xl">😊</span>
          <p className="text-2xl font-bold mt-2">{mood}/10</p>
          <p className="text-sm text-gray-500">Настроение</p>
        </div>
      </div>
    </div>
  )
}

function ShoppingTab({ items, toggle, total }: { items: ShoppingItem[]; toggle: (id: number) => void; total: number }) {
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm p-4">
        <p className="text-gray-500">Осталось купить</p>
        <p className="text-2xl font-bold">{total} ₽</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        {items.map(item => (
          <div key={item.id} className="flex items-center p-4 gap-3">
            <input type="checkbox" checked={item.checked} onChange={() => toggle(item.id)} className="w-5 h-5 text-indigo-500 rounded" />
            <span className={item.checked ? 'line-through text-gray-400' : ''}>{item.name}</span>
            <span className="ml-auto text-gray-500">{item.price} ₽</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function AssetsTab() {
  const assets = [
    { name: 'Toyota Camry', icon: '🚗', year: 2020, value: '1,500,000 ₽' },
    { name: 'iPhone 15', icon: '📱', year: 2024, value: '89,000 ₽' },
    { name: 'MacBook Pro', icon: '💻', year: 2023, value: '180,000 ₽' },
  ]
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">🚗 Имущество</h2>
      <div className="space-y-3">
        {assets.map((asset, i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm p-4 flex items-center gap-4">
            <span className="text-3xl">{asset.icon}</span>
            <div className="flex-1">
              <p className="font-medium">{asset.name}</p>
              <p className="text-sm text-gray-500">{asset.year}</p>
            </div>
            <span className="font-bold">{asset.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function SettingsTab() {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">⚙️ Настройки</h2>
      <div className="bg-white rounded-xl shadow-sm divide-y">
        <div className="p-4 flex justify-between items-center">
          <span>Язык</span>
          <span className="text-gray-500">Русский</span>
        </div>
        <div className="p-4 flex justify-between items-center">
          <span>Валюта</span>
          <span className="text-gray-500">₽ (RUB)</span>
        </div>
        <div className="p-4 flex justify-between items-center">
          <span>Тема</span>
          <span className="text-gray-500">Системная</span>
        </div>
        <div className="p-4 flex justify-between items-center">
          <span>AI Memory</span>
          <span className="text-gray-500">Управление</span>
        </div>
        <div className="p-4 flex justify-between items-center">
          <span>Уведомления</span>
          <span className="text-gray-500">Включены</span>
        </div>
      </div>
    </div>
  )
}
