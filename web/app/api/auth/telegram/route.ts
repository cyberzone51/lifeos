import { NextResponse } from 'next/server'
import { createServerSupabaseClient } from '@/lib/supabase/server'

export async function POST(request: Request) {
  try {
    const { initData } = await request.json()
    
    // Parse Telegram initData
    const urlParams = new URLSearchParams(initData)
    const user = JSON.parse(urlParams.get('user') || '{}')
    const hash = urlParams.get('hash')
    
    // TODO: Verify hash with Telegram Bot API
    
    const supabase = createServerSupabaseClient()
    
    // Sign in or create user
    const { data, error } = await supabase.auth.signInWithOtp({
      email: `${user.id}@telegram.local`,
      options: {
        data: {
          telegram_id: user.id,
          username: user.username,
          first_name: user.first_name,
        }
      }
    })

    if (error) throw error

    return NextResponse.json({ success: true, user })
  } catch (error) {
    return NextResponse.json({ error: 'Auth failed' }, { status: 400 })
  }
}
