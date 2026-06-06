"""
Точка входа — VK-бот для автоматического исправления ошибок в тексте.
"""

import logging

from openai import OpenAIError
from vkbottle.bot import Bot, Message

from config import VK_TOKEN, GREETING_TRIGGERS, MSG_WELCOME, MSG_PROCESSING_ERROR
from spell_service import correct_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=VK_TOKEN)


# Приветствие / помощь
@bot.on.message(func=lambda m: m.text.lower().strip() in [t.lower() for t in GREETING_TRIGGERS])
async def welcome_handler(message: Message) -> None:
    """Отвечает на приветствия и команды помощи."""
    await message.answer(MSG_WELCOME)


# Основной обработчик: исправление текста
@bot.on.message()
async def spell_handler(message: Message) -> None:
    """Принимает произвольный текст, исправляет ошибки и возвращает результат."""
    user_text = (message.text or "").strip()

    if not user_text:
        await message.answer("Пришли мне текст, и я исправлю в нём ошибки ✍️")
        return

    logger.info("Received message from user_id=%s, length=%d", message.from_id, len(user_text))

    try:
        corrected = await correct_text(user_text)
        await message.answer(corrected)
    except OpenAIError as exc:
        logger.error("Spell API error for user_id=%s: %s", message.from_id, exc)
        await message.answer(MSG_PROCESSING_ERROR)
    except Exception as exc:
        logger.exception("Unexpected error for user_id=%s: %s", message.from_id, exc)
        await message.answer(MSG_PROCESSING_ERROR)


# Запуск
if __name__ == "__main__":
    logger.info("Starting spell-correction bot...")
    bot.run()
