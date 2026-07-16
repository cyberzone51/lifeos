import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { message } = await request.json()
    
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: 'You are LifeOS AI assistant. Be helpful and concise. User says: ' + message }] }]
        })
      }
    )

    const data = await response.json()
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "I'm here to help!"

    return NextResponse.json({ response: reply })
  } catch (error) {
    return NextResponse.json({ error: 'Chat failed' }, { status: 500 })
  }
}
