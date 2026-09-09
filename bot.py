import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BusinessMessagesDeleted

# 1. Вставьте ваши данные сюда
BOT_TOKEN = "1954489124:AAGOQjJcZdb5Ei6Wps6cgHIiX7uXYY6AGII"
YOUR_CHAT_ID = 850863512  # Ваш числовой ID из @userinfobot

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Временное хранилище сообщений: {message_id: (sender, text, chat_id)}
saved_messages = {}

# Хэндлер входящих бизнес-сообщений
@dp.business_message()
async def on_business_message(message: Message):
    sender = message.from_user.full_name if message.from_user else "Собеседник"
    text = message.text or message.caption or "[Медиафайл без подписи]"
    
    saved_messages[message.message_id] = {
        "sender": sender,
        "text": text,
        "chat_id": message.chat.id
    }

# Хэндлер удаления сообщений
@dp.business_messages_deleted()
async def on_messages_deleted(event: BusinessMessagesDeleted):
    for msg_id in event.message_ids:
        cached = saved_messages.get(msg_id)
        if cached:
            alert = (
                f"🗑 **Удалено сообщение!**\n\n"
                f"👤 От: {cached['sender']}\n"
                f"💬 **Текст:**\n{cached['text']}"
            )
            await bot.send_message(chat_id=YOUR_CHAT_ID, text=alert, parse_mode="Markdown")
            del saved_messages[msg_id]

# Веб-сервер для прохождения проверки портов Render
async def health_check(request):
    return web.Response(text="Bot is running!")

async def main():
    # Запуск микро-сервера
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Запуск прослушивания Telegram
    print("Бот запущен и слушает события...")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
