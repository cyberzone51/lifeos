#!/usr/bin/env python3
"""Start Telegram bot."""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.telegram.bot import telegram_bot
from app.core.config import settings


def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in .env")
        print("   Get a token from @BotFather on Telegram")
        return

    print("🤖 Starting LifeOS Telegram Bot...")
    telegram_bot.setup()
    telegram_bot.run()


if __name__ == "__main__":
    main()
