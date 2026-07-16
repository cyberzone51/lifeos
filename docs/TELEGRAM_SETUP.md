# Telegram Mini App Setup Guide

## 1. Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Enter a name for your bot (e.g., "LifeOS AI")
4. Enter a username (e.g., "lifeos_ai_bot")
5. Copy the **API token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 2. Configure Environment

Add to your `.env` file:

```bash
TELEGRAM_BOT_TOKEN=your-token-here
TELEGRAM_MINI_APP_URL=https://your-domain.com
```

## 3. Set Bot Commands

Send to @BotFather:

```
/setcommands
```

Then paste:

```
start - Open LifeOS
help - Show help
```

## 4. Configure Mini App

Send to @BotFather:

```
/newapp
```

Follow the prompts:
1. Select your bot
2. Enter app name: "LifeOS"
3. Enter app description
4. Enter the Mini App URL
5. Upload a square logo (512x512)
6. Upload a GIF or video (optional)

## 5. Set Menu Button

Send to @BotFather:

```
/setmenubutton
```

1. Select your bot
2. Enter the Mini App URL
3. Enter button text: "Open LifeOS"

## 6. Test Locally

### Option A: ngrok (for testing)

```bash
# Install ngrok
ngrok http 8000

# Use the HTTPS URL in TELEGRAM_MINI_APP_URL
```

### Option B: Telegram Desktop

1. Open your bot in Telegram Desktop
2. Click the menu button
3. The Mini App should open

## 7. Deploy to Production

### Domain Requirements
- Must be HTTPS
- Must have valid SSL certificate
- Must be accessible from Telegram's servers

### Recommended Services
- **Vercel**: Free tier supports Flutter Web
- **Netlify**: Free tier with custom domains
- **Cloudflare Pages**: Fast, free tier available

### Flutter Web Build

```bash
cd frontend
flutter build web --release
```

Upload the `build/web` folder to your hosting service.

## 8. Deep Links

### Start Parameter

```
https://t.me/your_bot?start=abc123
```

In your bot handler:

```python
@CommandHandler("start")
async def start(update, context):
    # Get start parameter
    args = context.args
    if args:
        param = args[0]  # "abc123"
        # Handle the parameter
```

### Share Links

```
https://t.me/your_bot?startapp=task_123
```

## 9. Payments (Telegram Stars)

### Configure Payments

1. Send to @BotFather:

```
/setpayments
```

2. Configure your payment provider

### Process Payment

```python
from telegram import LabeledPrice

async def send_invoice(update, context):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="LifeOS Premium",
        description="Unlimited AI messages",
        payload="premium_monthly",
        provider_token=PROVIDER_TOKEN,
        currency="XTR",  # Telegram Stars
        prices=[LabeledPrice("Premium", 100)],
    )
```

## 10. Theme Integration

Telegram Mini Apps automatically receive theme colors:

```javascript
// In JavaScript
const themeParams = Telegram.WebApp.themeParams;

// Colors available:
// themeParams.bg_color
// themeParams.text_color
// themeParams.hint_color
// themeParams.link_color
// themeParams.button_color
// themeParams.button_text_color
// etc.
```

In Flutter, you can access these via the `telegram_web_app` package.

## Troubleshooting

### Mini App not opening
- Check if URL is HTTPS
- Verify bot has Mini App configured
- Ensure URL is accessible

### Authentication failing
- Verify TELEGRAM_BOT_TOKEN is correct
- Check bot is not in test mode
- Ensure initData is properly formatted

### Theme not applying
- Use `Telegram.WebApp.colorScheme` for dark/light mode
- Apply theme params from `Telegram.WebApp.themeParams`

## Resources

- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps)
- [Telegram WebApp JS SDK](https://core.telegram.org/bots/webapps#initializing-the-mini-app)
- [BotFather Commands](https://core.telegram.org/bots#creating-a-new-bot)
