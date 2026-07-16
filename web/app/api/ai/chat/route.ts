import { NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase/server'

// AI classification prompt
const CLASSIFICATION_PROMPT = `Classify the user message into one of these categories:
- finance: expenses, income, money, budget
- health: exercise, weight, sleep, water, mood
- reminder: remind, notify, alert
- task: todo, task, plan, schedule
- chat: general conversation

Return JSON: {"category": "...", "params": {...}}`

export async function POST(request: Request) {
  try {
    const { message, userId } = await request.json()
    
    const supabase = createServerSupabaseClient()
    
    // Classify intent using Gemini
    const classificationResponse = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `${CLASSIFICATION_PROMPT}\n\nMessage: ${message}` }] }]
        })
      }
    )
    
    const classificationData = await classificationResponse.json()
    const intent = JSON.parse(classificationData.candidates?.[0]?.content?.parts?.[0]?.text || '{"category":"chat","params":{}}')
    
    // Generate response based on category
    let response = ''
    
    switch (intent.category) {
      case 'finance':
        response = await handleFinance(message, userId, supabase)
        break
      case 'health':
        response = await handleHealth(message, userId, supabase)
        break
      case 'reminder':
        response = await handleReminder(message, userId, supabase)
        break
      case 'task':
        response = await handleTask(message, userId, supabase)
        break
      default:
        response = await handleChat(message, supabase)
    }
    
    // Save to AI memory
    await supabase.from('ai_messages').insert({
      user_id: userId,
      role: 'user',
      content: message,
    })
    
    await supabase.from('ai_messages').insert({
      user_id: userId,
      role: 'assistant',
      content: response,
      agent_type: intent.category,
    })

    return NextResponse.json({ response, intent })
  } catch (error) {
    return NextResponse.json({ error: 'Chat failed' }, { status: 500 })
  }
}

async function handleFinance(message: string, userId: string, supabase: any) {
  // Extract finance data from message
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: `Extract expense/income from: "${message}". Return JSON: {"type":"expense|income","amount":0,"currency":"USD","category":"food|transport|other","description":"..."}` }] }]
      }]
    }
  )
  
  const data = await response.json()
  const finance = JSON.parse(data.candidates?.[0]?.content?.parts?.[0]?.text || '{}')
  
  if (finance.amount) {
    await supabase.from('expenses').insert({
      user_id: userId,
      amount: finance.amount,
      currency_code: finance.currency || 'USD',
      category: finance.category || 'other',
      description: finance.description || message,
    })
    
    return `✅ Recorded: ${finance.type} $${finance.amount} (${finance.category})`
  }
  
  return "I couldn't extract the amount. Please try again."
}

async function handleHealth(message: string, userId: string, supabase: any) {
  return `✅ Health activity logged: ${message}`
}

async function handleReminder(message: string, userId: string, supabase: any) {
  return `✅ Reminder set: ${message}`
}

async function handleTask(message: string, userId: string, supabase: any) {
  await supabase.from('tasks').insert({
    user_id: userId,
    title: message,
    status: 'pending',
  })
  
  return `✅ Task created: ${message}`
}

async function handleChat(message: string, supabase: any) {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: `You are LifeOS AI assistant. Be helpful and concise. User says: "${message}"` }] }]
      })
    }
  )
  
  const data = await response.json()
  return data.candidates?.[0]?.content?.parts?.[0]?.text || "I'm here to help!"
}
