import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { message } = await request.json()
    
    const apiKey = process.env.GEMINI_API_KEY
    
    if (!apiKey) {
      return NextResponse.json({ 
        response: 'AI not configured. Add GEMINI_API_KEY to Vercel environment variables.' 
      })
    }

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: 'You are LifeOS AI assistant. Be helpful, concise, and speak in the same language as the user. If user speaks Russian - reply in Russian. User says: ' + message }] }]
        })
      }
    )

    if (!response.ok) {
      const error = await response.text()
      return NextResponse.json({ response: 'API error: ' + error })
    }

    const data = await response.json()
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || "Sorry, I couldn't process that."

    return NextResponse.json({ response: reply })
  } catch (error: any) {
    return NextResponse.json({ response: 'Error: ' + error.message })
  }
}
