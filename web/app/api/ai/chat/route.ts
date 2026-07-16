import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { message } = await request.json()
    
    const apiKey = process.env.GEMINI_API_KEY
    
    if (!apiKey) {
      return NextResponse.json({ response: 'Добавь GEMINI_API_KEY в переменные окружения Vercel.' })
    }

    const systemPrompt = `Ты — AI ассистент LifeOS. Отвечай на русском языке.
Ты помогаешь с: задачами, финансами, привычками, целями, здоровьем.
Будь дружелюбным, кратким и полезным.
Если пользователь сообщает о расходе — подтверди запись.
Если просит задачу — помоги сформулировать.
Если спрашивает о привычках — дай совет.`

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: systemPrompt + '\n\nПользователь: ' + message }] }]
        })
      }
    )

    if (!response.ok) {
      return NextResponse.json({ response: 'Ошибка API. Проверь ключ GEMINI_API_KEY.' })
    }

    const data = await response.json()
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || 'Не удалось обработать запрос.'

    return NextResponse.json({ response: reply })
  } catch (error: any) {
    return NextResponse.json({ response: 'Ошибка: ' + error.message })
  }
}
