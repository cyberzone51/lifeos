"""Telegram Bot — обработка команд и уведомлений."""

import asyncio
from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from app.core.config import settings


class TelegramBot:
    """Telegram бот для LifeOS."""

    def __init__(self):
        self.app = None

    def setup(self):
        """Настройка бота."""
        self.app = (
            Application.builder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .build()
        )

        # Handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        # Set menu button
        self.app.post_init = self.post_init

    async def post_init(self, application: Application):
        """Действия после инициализации."""
        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Open LifeOS",
                web_app=WebAppInfo(url=settings.TELEGRAM_MINI_APP_URL),
            )
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start."""
        user = update.effective_user
        
        keyboard = [[
            {
                "text": "🚀 Open LifeOS",
                "web_app": {"url": settings.TELEGRAM_MINI_APP_URL},
            }
        ]]

        await update.message.reply_text(
            f"👋 Welcome to LifeOS, {user.first_name}!\n\n"
            "I'm your AI Life Operating System.\n\n"
            "Tap the button below to open LifeOS:",
            reply_markup={"keyboard": keyboard, "resize_keyboard": True},
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help."""
        await update.message.reply_text(
            "📱 LifeOS — AI Personal Operating System\n\n"
            "Features:\n"
            "• AI Assistant — talk naturally\n"
            "• Finance — track expenses\n"
            "• Tasks — manage your day\n"
            "• Habits — build good habits\n"
            "• Health — track wellness\n\n"
            "Open the mini app to get started!"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений."""
        text = update.message.text
        
        # Forward to AI
        from app.services.ai_service import AIService
        from app.database.session import async_session_factory
        
        async with async_session_factory() as db:
            import uuid
            ai_service = AIService(db)
            result = await ai_service.process_message(
                user_id=uuid.uuid4(),  # TODO: real user_id
                message=text,
            )
            await update.message.reply_text(result["response"])

    def run(self):
        """Запуск бота."""
        if self.app:
            self.app.run_polling()


# Singleton
telegram_bot = TelegramBot()
