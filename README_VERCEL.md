# LifeOS - Vercel + Supabase

## Quick Start

### 1. Setup Supabase

1. Go to https://supabase.com
2. Create a new project
3. Go to SQL Editor
4. Run the contents of `supabase/schema.sql`
5. Copy your project URL and keys

### 2. Setup Vercel

1. Go to https://vercel.com
2. Import your GitHub repository
3. Set environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `GEMINI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
4. Deploy

### 3. Environment Variables

Create `web/.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GEMINI_API_KEY=your-gemini-key
TELEGRAM_BOT_TOKEN=your-telegram-token
```

### 4. Telegram Bot

1. Create bot via @BotFather
2. Set WebApp URL to your Vercel domain
3. Test in Telegram

## Architecture

```
Vercel (Frontend + API)
├── web/                 # Next.js app
│   ├── app/
│   │   ├── page.tsx     # Main page
│   │   └── api/         # API routes
│   └── lib/
│       └── supabase/    # Supabase client
└── supabase/
    └── schema.sql       # Database schema

Supabase (Backend)
├── PostgreSQL           # Database
├── Auth                 # Authentication
└── Row Level Security   # Security
```

## Free Tier Limits

- **Vercel:** 100GB bandwidth, 1000 builds/month
- **Supabase:** 500MB database, 50K monthly active users
- **Gemini:** Free tier available

## Cost: $0/month
