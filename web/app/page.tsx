'use client'

import { useState, useEffect } from 'react'

type Tab = 'home' | 'ai' | 'tasks' | 'finance' | 'habits' | 'goals' | 'journal' | 'health' | 'shopping' | 'roadmap' | 'more'

const TABS: [Tab, string, string][] = [
  ['home', '🏠', 'Главная'],
  ['ai', '🤖', 'AI'],
  ['tasks', '📋', 'Задачи'],
  ['finance', '💰', 'Финансы'],
  ['habits', '🔥', 'Привычки'],
  ['goals', '🎯', 'Цели'],
  ['journal', '📖', 'Дневник'],
  ['health', '❤️', 'Здоровье'],
  ['shopping', '🛒', 'Покупки'],
  ['roadmap', '🧭', 'План'],
  ['more', '⋯', 'Ещё'],
]

export default function Home() {
  const [tab, setTab] = useState<Tab>('home')
  const [time, setTime] = useState('')

  useEffect(() => {
    const update = () => {
      const now = new Date()
      setTime(now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' }))
    }
    update()
    const i = setInterval(update, 60000)
    return () => clearInterval(i)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Status Bar */}
      <div className="glass px-4 py-2 flex justify-between items-center text-sm">
        <span className="font-semibold text-gray-800">{time}</span>
        <span className="text-gray-500">LifeOS v1.0</span>
      </div>

      {/* Header */}
      {tab === 'home' && (
        <div className="px-4 pt-4 pb-2 text-white">
          <h1 className="text-2xl font-bold">Доброе утро! 👋</h1>
          <p className="text-white/80">Что планируешь сегодня?</p>
        </div>
      )}

      {/* Main Content */}
      <main className="px-4 pb-24">
        {tab === 'home' && <HomeTab setTab={setTab} />}
        {tab === 'ai' && <AITab />}
        {tab === 'tasks' && <TasksTab />}
        {tab === 'finance' && <FinanceTab />}
        {tab === 'habits' && <HabitsTab />}
        {tab === 'goals' && <GoalsTab />}
        {tab === 'journal' && <JournalTab />}
        {tab === 'health' && <HealthTab />}
        {tab === 'shopping' && <ShoppingTab />}
        {tab === 'roadmap' && <RoadmapTab />}
        {tab === 'more' && <MoreTab />}
      </main>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 glass border-t border-gray-200/50">
        <div className="flex justify-around items-center py-2">
          {TABS.map(([key, icon, label]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`flex flex-col items-center py-1 px-2 rounded-xl transition-all ${
                tab === key
                  ? 'text-indigo-600 bg-indigo-50 scale-110'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <span className="text-xl">{icon}</span>
              <span className="text-xs mt-1">{label}</span>
            </button>
          ))}
        </div>
      </nav>
    </div>
  )
}

function HomeTab({ setTab }: { setTab: (t: Tab) => void }) {
  return (
    <div className="space-y-4 slide-in">
      {/* Stats Cards */}
      <div className="grid grid-cols-2 gap-3">
        <StatCard icon="📋" label="Задачи" value="3" sub="активных" color="blue" onClick={() => setTab('tasks')} />
        <StatCard icon="🔥" label="Привычки" value="4/6" sub="выполнено" color="orange" onClick={() => setTab('habits')} />
        <StatCard icon="💰" label="Расходы" value="470₽" sub="сегодня" color="green" onClick={() => setTab('finance')} />
        <StatCard icon="🎯" label="Цели" value="3" sub="в процессе" color="purple" onClick={() => setTab('goals')} />
      </div>

      {/* Daily Habit Loop */}
      <div className="glass rounded-2xl p-4 bg-white/90">
        <div className="flex items-start gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center text-2xl">
            🌅
          </div>
          <div className="flex-1">
            <p className="font-semibold text-gray-800">Ежедневный сценарий</p>
            <p className="text-sm text-gray-600 mt-1">AI собирает задачи, бюджет, цели и привычки в один понятный план дня.</p>
            <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs">
              <button onClick={() => setTab('ai')} className="rounded-xl bg-indigo-50 px-2 py-2 text-indigo-700">🧠 Спросить</button>
              <button onClick={() => setTab('tasks')} className="rounded-xl bg-red-50 px-2 py-2 text-red-700">🔴 Важное</button>
              <button onClick={() => setTab('habits')} className="rounded-xl bg-orange-50 px-2 py-2 text-orange-700">🔥 Серия</button>
            </div>
          </div>
        </div>
      </div>

      {/* Quick AI */}
      <div className="glass rounded-2xl p-4 card-hover cursor-pointer" onClick={() => setTab('ai')}>
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-2xl">
            🤖
          </div>
          <div className="flex-1">
            <p className="font-semibold text-gray-800">AI Ассистент</p>
            <p className="text-sm text-gray-500">Спроси что угодно...</p>
          </div>
          <span className="text-gray-400">→</span>
        </div>
      </div>

      {/* Today's Tasks */}
      <div className="glass rounded-2xl p-4">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-gray-800">Сегодня</h3>
          <button onClick={() => setTab('tasks')} className="text-indigo-500 text-sm">Все →</button>
        </div>
        <div className="space-y-2">
          <TaskItem title="Купить продукты" priority="high" done={false} />
          <TaskItem title="Позвонить маме" priority="medium" done={false} />
          <TaskItem title="Пробежка 5 км" priority="low" done={true} />
        </div>
      </div>

      {/* Habits Progress */}
      <div className="glass rounded-2xl p-4">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-gray-800">Привычки</h3>
          <button onClick={() => setTab('habits')} className="text-indigo-500 text-sm">Все →</button>
        </div>
        <div className="flex gap-3 overflow-x-auto pb-2">
          <HabitMini icon="💧" name="Вода" progress={60} />
          <HabitMini icon="🏃" name="Спорт" progress={100} />
          <HabitMini icon="📚" name="Чтение" progress={30} />
        </div>
      </div>
    </div>
  )
}

function AITab() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<{role: string; content: string}[]>([
    { role: 'ai', content: 'Привет! 👋 Я твой AI ассистент.\n\nМогу помочь с:\n• Задачами и планами\n• Финансами\n• Привычками\n• Здоровьем\n\nПросто напиши что нужно!' }
  ])
  const [loading, setLoading] = useState(false)

  const send = async () => {
    if (!message.trim() || loading) return
    const userMsg = { role: 'user', content: message }
    setMessages(prev => [...prev, userMsg])
    setMessage('')
    setLoading(true)
    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'ai', content: data.response }])
    } catch {
      setMessages(prev => [...prev, { role: 'ai', content: 'Ошибка соединения' }])
    }
    setLoading(false)
  }

  return (
    <div className="glass rounded-2xl overflow-hidden slide-in" style={{ height: 'calc(100vh - 180px)' }}>
      <div className="h-full overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] p-3 rounded-2xl ${
              msg.role === 'user'
                ? 'bg-indigo-500 text-white rounded-br-md'
                : 'bg-gray-100 text-gray-800 rounded-bl-md'
            }`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-2xl rounded-bl-md">
              <span className="pulse">Думаю...</span>
            </div>
          </div>
        )}
      </div>
      <div className="p-3 border-t bg-white/50">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && send()}
            placeholder="Напиши сообщение..."
            className="flex-1 bg-gray-100 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button onClick={send} disabled={loading}
            className="bg-indigo-500 text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-indigo-600 disabled:opacity-50">
            →
          </button>
        </div>
      </div>
    </div>
  )
}

function TasksTab() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Купить продукты', priority: 'high', done: false },
    { id: 2, title: 'Позвонить маме', priority: 'medium', done: false },
    { id: 3, title: 'Оплатить аренду', priority: 'high', done: true },
    { id: 4, title: 'Пробежка 5 км', priority: 'low', done: false },
  ])

  const toggle = (id: number) => setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))

  return (
    <div className="space-y-4 slide-in">
      <h2 className="text-xl font-bold text-white">📋 Задачи</h2>
      <div className="glass rounded-2xl divide-y">
        {tasks.map(task => (
          <div key={task.id} className="flex items-center p-4 gap-3">
            <button onClick={() => toggle(task.id)}
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                task.done ? 'bg-green-500 border-green-500' : 'border-gray-300'
              }`}>
              {task.done && <span className="text-white text-xs">✓</span>}
            </button>
            <div className={`w-2 h-2 rounded-full ${
              task.priority === 'high' ? 'bg-red-500' : task.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
            }`} />
            <span className={`flex-1 ${task.done ? 'line-through text-gray-400' : 'text-gray-800'}`}>{task.title}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function FinanceTab() {
  const expenses = [
    { amount: 350, cat: '🍔 Еда', desc: 'Обед', time: '12:30' },
    { amount: 120, cat: '🚌 Транспорт', desc: 'Метро', time: '08:15' },
    { amount: 2500, cat: '🏠 ЖКХ', desc: 'Электричество', time: 'Вчера' },
  ]
  const total = expenses.reduce((s, e) => s + e.amount, 0)

  return (
    <div className="space-y-4 slide-in">
      <div className="glass rounded-2xl p-5 bg-gradient-to-br from-green-400 to-emerald-600 text-white">
        <p className="text-white/80 text-sm">Расходы сегодня</p>
        <p className="text-4xl font-bold mt-1">{total} ₽</p>
        <div className="mt-3 bg-white/20 rounded-full h-2">
          <div className="bg-white h-2 rounded-full" style={{ width: '47%' }}></div>
        </div>
        <p className="text-white/70 text-xs mt-1">Бюджет: 1,000 ₽</p>
      </div>

      <h3 className="text-white font-semibold">Операции</h3>
      <div className="glass rounded-2xl divide-y">
        {expenses.map((exp, i) => (
          <div key={i} className="flex items-center p-4 gap-3">
            <div className="text-2xl">{exp.cat.split(' ')[0]}</div>
            <div className="flex-1">
              <p className="font-medium text-gray-800">{exp.desc}</p>
              <p className="text-xs text-gray-500">{exp.time}</p>
            </div>
            <span className="text-red-500 font-semibold">-{exp.amount} ₽</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function HabitsTab() {
  const [habits, setHabits] = useState([
    { id: 1, icon: '💧', name: 'Вода 8 стаканов', done: false, streak: 12 },
    { id: 2, icon: '🏃', name: 'Спорт 30 мин', done: true, streak: 5 },
    { id: 3, icon: '📚', name: 'Чтение 20 стр', done: false, streak: 8 },
    { id: 4, icon: '🧘', name: 'Медитация', done: false, streak: 3 },
    { id: 5, icon: '😴', name: 'Сон 8 часов', done: true, streak: 15 },
    { id: 6, icon: '🌍', name: 'Язык 15 мин', done: false, streak: 7 },
  ])

  const toggle = (id: number) => setHabits(habits.map(h => h.id === id ? { ...h, done: !h.done } : h))
  const done = habits.filter(h => h.done).length

  return (
    <div className="space-y-4 slide-in">
      <div className="glass rounded-2xl p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold text-gray-800">Прогресс</span>
          <span className="text-indigo-600 font-bold">{done}/{habits.length}</span>
        </div>
        <div className="bg-gray-200 rounded-full h-3">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full progress-bar"
            style={{ width: `${(done/habits.length)*100}%` }}></div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {habits.map(habit => (
          <div key={habit.id} onClick={() => toggle(habit.id)}
            className={`glass rounded-2xl p-4 card-hover cursor-pointer ${
              habit.done ? 'ring-2 ring-green-500 bg-green-50/50' : ''
            }`}>
            <div className="text-3xl mb-2">{habit.icon}</div>
            <p className="font-medium text-gray-800 text-sm">{habit.name}</p>
            <div className="flex items-center gap-1 mt-2">
              <span className="streak-fire">🔥</span>
              <span className="text-xs text-gray-500">{habit.streak} дн.</span>
            </div>
            {habit.done && (
              <div className="mt-2 text-green-500 text-sm font-medium">✓ Выполнено</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function GoalsTab() {
  const goals = [
    { title: 'Накопить 100 000 ₽', progress: 35000, target: 100000, icon: '💰' },
    { title: 'Похудеть на 5 кг', progress: 2, target: 5, icon: '⚖️' },
    { title: 'Прочитать 24 книги', progress: 18, target: 24, icon: '📚' },
  ]

  return (
    <div className="space-y-4 slide-in">
      <h2 className="text-xl font-bold text-white">🎯 Цели</h2>
      {goals.map((goal, i) => (
        <div key={i} className="glass rounded-2xl p-4 card-hover">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-3xl">{goal.icon}</span>
            <div className="flex-1">
              <p className="font-semibold text-gray-800">{goal.title}</p>
              <p className="text-sm text-gray-500">{goal.progress.toLocaleString()} / {goal.target.toLocaleString()}</p>
            </div>
            <span className="text-indigo-600 font-bold">{Math.round(goal.progress/goal.target*100)}%</span>
          </div>
          <div className="bg-gray-200 rounded-full h-3">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full progress-bar"
              style={{ width: `${(goal.progress/goal.target)*100}%` }}></div>
          </div>
        </div>
      ))}
    </div>
  )
}

function JournalTab() {
  const entries = [
    { date: 'Сегодня', mood: 8, emoji: '😊', text: 'Отличный день! Много сделал, вечером кино.' },
    { date: 'Вчера', mood: 6, emoji: '😐', text: 'Обычный день. Работа напряжённая.' },
    { date: '2 дня назад', mood: 9, emoji: '🥰', text: 'Родился малыш у друга! Поздравлял весь день.' },
  ]

  return (
    <div className="space-y-4 slide-in">
      <h2 className="text-xl font-bold text-white">📖 Дневник</h2>
      {entries.map((entry, i) => (
        <div key={i} className="glass rounded-2xl p-4 card-hover">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-500">{entry.date}</span>
            <span className="text-3xl">{entry.emoji}</span>
          </div>
          <p className="text-gray-800">{entry.text}</p>
          <div className="mt-2 flex gap-1">
            {[1,2,3,4,5,6,7,8,9,10].map(n => (
              <div key={n} className={`w-2 h-2 rounded-full ${n <= entry.mood ? 'bg-indigo-500' : 'bg-gray-200'}`} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function HealthTab() {
  return (
    <div className="space-y-4 slide-in">
      <h2 className="text-xl font-bold text-white">❤️ Здоровье</h2>
      <div className="grid grid-cols-2 gap-3">
        <HealthCard icon="😴" label="Сон" value="7.5ч" color="indigo" />
        <HealthCard icon="💧" label="Вода" value="5/8" color="blue" />
        <HealthCard icon="😊" label="Настроение" value="8/10" color="yellow" />
        <HealthCard icon="🏃" label="Шаги" value="8,432" color="green" />
        <HealthCard icon="⚖️" label="Вес" value="75.5 кг" color="purple" />
        <HealthCard icon="💪" label="Тренировка" value="30 мин" color="red" />
      </div>
    </div>
  )
}

function ShoppingTab() {
  const [items, setItems] = useState([
    { id: 1, name: 'Молоко', price: 80, checked: false },
    { id: 2, name: 'Хлеб', price: 50, checked: true },
    { id: 3, name: 'Яйца', price: 120, checked: false },
    { id: 4, name: 'Курица', price: 250, checked: false },
    { id: 5, name: 'Овощи', price: 300, checked: false },
  ])

  const toggle = (id: number) => setItems(items.map(i => i.id === id ? { ...i, checked: !i.checked } : i))
  const total = items.filter(i => !i.checked).reduce((s, i) => s + i.price, 0)

  return (
    <div className="space-y-4 slide-in">
      <div className="glass rounded-2xl p-4 bg-gradient-to-br from-orange-400 to-pink-500 text-white">
        <p className="text-white/80 text-sm">Осталось купить</p>
        <p className="text-3xl font-bold">{total} ₽</p>
      </div>

      <div className="glass rounded-2xl divide-y">
        {items.map(item => (
          <div key={item.id} className="flex items-center p-4 gap-3">
            <button onClick={() => toggle(item.id)}
              className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                item.checked ? 'bg-green-500 border-green-500' : 'border-gray-300'
              }`}>
              {item.checked && <span className="text-white text-xs">✓</span>}
            </button>
            <span className={`flex-1 ${item.checked ? 'line-through text-gray-400' : 'text-gray-800'}`}>{item.name}</span>
            <span className="text-gray-500">{item.price} ₽</span>
          </div>
        ))}
      </div>
    </div>
  )
}


const MODULE_LEVELS = [
  {
    name: 'Core',
    badge: 'MVP',
    color: 'from-emerald-400 to-teal-600',
    description: 'Обязательные модули, которые отвечают на вопрос «что мне сегодня делать?»',
    modules: ['🧠 AI Personal Assistant', '📅 Smart Planner', '💰 Finance Manager', '🎯 Goals', '🔥 Habit Tracker'],
  },
  {
    name: 'Retention',
    badge: 'Ежедневно',
    color: 'from-amber-400 to-orange-600',
    description: 'Ритуалы и память, из-за которых пользователь возвращается утром и вечером.',
    modules: ['📖 AI Journal', '🧠 Personal Memory', '📚 Knowledge Vault', '🎤 Voice Assistant', '📸 AI Scanner'],
  },
  {
    name: 'Advanced',
    badge: 'Уникальность',
    color: 'from-blue-400 to-indigo-600',
    description: 'Расширения для семьи, коучинга, покупок, безопасности и личной хроники.',
    modules: ['👨‍👩‍👧 Family Mode', '🤖 AI Life Coach', '🏆 Gamification', '🛒 Smart Shopping', '🛡 Digital Safety'],
  },
]

function RoadmapTab() {
  return (
    <div className="space-y-4 slide-in">
      <div className="text-white">
        <h2 className="text-xl font-bold">🧭 Стратегия модулей</h2>
        <p className="text-sm text-white/80 mt-1">Не набор функций, а ежедневная привычка для людей любого возраста.</p>
      </div>

      <div className="glass rounded-2xl p-4">
        <p className="text-xs uppercase tracking-wide text-indigo-600 font-bold">Главный retention loop</p>
        <p className="text-gray-800 font-semibold mt-1">Утро: план дня → День: быстрый ввод голосом → Вечер: журнал и прогресс.</p>
      </div>

      {MODULE_LEVELS.map(level => (
        <div key={level.name} className="glass rounded-2xl overflow-hidden card-hover">
          <div className={`bg-gradient-to-r ${level.color} p-4 text-white`}>
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold">{level.name}</h3>
              <span className="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold">{level.badge}</span>
            </div>
            <p className="text-sm text-white/85 mt-2">{level.description}</p>
          </div>
          <div className="p-4 grid gap-2">
            {level.modules.map(module => (
              <div key={module} className="flex items-center justify-between rounded-xl bg-white/60 px-3 py-2">
                <span className="text-sm font-medium text-gray-800">{module}</span>
                <span className="text-indigo-500">→</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function MoreTab() {
  const items = [
    { icon: '🚗', label: 'Имущество', desc: 'Автомобиль, техника' },
    { icon: '👨‍👩‍👧', label: 'Семья', desc: 'Общий бюджет и задачи' },
    { icon: '🌍', label: 'Переводчик', desc: 'AI перевод текста' },
    { icon: '🛡️', label: 'Безопасность', desc: 'Проверка сообщений' },
    { icon: '⚙️', label: 'Настройки', desc: 'Язык, валюта, тема' },
  ]

  return (
    <div className="space-y-4 slide-in">
      <h2 className="text-xl font-bold text-white">Ещё</h2>
      <div className="glass rounded-2xl divide-y">
        {items.map((item, i) => (
          <div key={i} className="flex items-center p-4 gap-3 cursor-pointer hover:bg-gray-50 transition">
            <span className="text-2xl">{item.icon}</span>
            <div className="flex-1">
              <p className="font-medium text-gray-800">{item.label}</p>
              <p className="text-sm text-gray-500">{item.desc}</p>
            </div>
            <span className="text-gray-400">→</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// Shared Components
function StatCard({ icon, label, value, sub, color, onClick }: { icon: string; label: string; value: string; sub: string; color: string; onClick: () => void }) {
  const colors: Record<string, string> = {
    blue: 'from-blue-400 to-blue-600',
    orange: 'from-orange-400 to-orange-600',
    green: 'from-green-400 to-green-600',
    purple: 'from-purple-400 to-purple-600',
  }
  return (
    <div onClick={onClick} className="glass rounded-2xl p-4 card-hover cursor-pointer">
      <span className="text-2xl">{icon}</span>
      <p className="text-2xl font-bold text-gray-800 mt-2">{value}</p>
      <p className="text-xs text-gray-500">{sub}</p>
    </div>
  )
}

function TaskItem({ title, priority, done }: { title: string; priority: string; done: boolean }) {
  const p = { high: 'bg-red-500', medium: 'bg-yellow-500', low: 'bg-green-500' }
  return (
    <div className="flex items-center gap-2 py-2">
      <div className={`w-2 h-2 rounded-full ${p[priority as keyof typeof p]}`} />
      <span className={`text-sm ${done ? 'line-through text-gray-400' : 'text-gray-700'}`}>{title}</span>
    </div>
  )
}

function HabitMini({ icon, name, progress }: { icon: string; name: string; progress: number }) {
  return (
    <div className="flex-shrink-0 w-20 text-center">
      <div className={`w-14 h-14 mx-auto rounded-xl flex items-center justify-center text-2xl ${
        progress >= 100 ? 'bg-green-100' : 'bg-gray-100'
      }`}>{icon}</div>
      <p className="text-xs text-gray-600 mt-1">{name}</p>
      <div className="bg-gray-200 rounded-full h-1 mt-1">
        <div className="bg-indigo-500 h-1 rounded-full" style={{ width: `${progress}%` }}></div>
      </div>
    </div>
  )
}

function HealthCard({ icon, label, value, color }: { icon: string; label: string; value: string; color: string }) {
  return (
    <div className="glass rounded-2xl p-4 card-hover text-center">
      <span className="text-3xl">{icon}</span>
      <p className="text-xl font-bold text-gray-800 mt-2">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  )
}
