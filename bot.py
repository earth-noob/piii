import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BusinessMessagesDeleted

# Вставьте сюда токен бота из @BotFather
BOT_TOKEN = "1954489124:AAGOQjJcZdb5Ei6Wps6cgHIiX7uXYY6AGII"

# Вставьте ваш числовой Telegram ID (узнать можно у бота @userinfobot)
# Сюда будут приходить уведомления об удаленных сообщениях
YOUR_CHAT_ID = 850863512

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Временное хранилище сообщений: {message_id: (sender_id, text/caption)}
saved_messages = {}


# Обработчик новых сообщений из бизнес-подключения
@dp.business_message()
async def on_business_message(message: Message):
    sender = message.from_user.full_name if message.from_user else "Собеседник"
    text = message.text or message.caption or "[Медиафайл без подписи]"

    # Сохраняем сообщение в памяти
    saved_messages[message.message_id] = {
        "sender": sender,
        "text": text,
        "chat_id": message.chat.id
    }


# Обработчик удалений сообщений
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
            # Очищаем память
            del saved_messages[msg_id]


async def main():
    print("Бизнес-бот запущен и слушает удаленные сообщения...")
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())