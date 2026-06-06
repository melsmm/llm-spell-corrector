"""
Централизованная конфигурация — все константы берутся из .env.
"""

import os

from dotenv import load_dotenv


load_dotenv()


def _require(key: str) -> str:
    """Получает обязательную переменную окружения или падает с понятной ошибкой."""
    value = os.environ.get(key)
    if not value:
        raise EnvironmentError(
            f"Переменная окружения '{key}' не задана. Проверьте .env файл."
        )
    return value


# VK
VK_TOKEN: str = _require("VK_TOKEN")

# Spell-correction API
SPELL_API_KEY: str = _require("SPELL_API_KEY")
SPELL_API_BASE_URL: str = _require("SPELL_API_BASE_URL")
SPELL_MODEL: str = _require("SPELL_MODEL")
SPELL_TEMPERATURE: float = 0.1
SPELL_TOP_P: float = 0.7

# Промпт
SPELL_PROMPT_TEMPLATE: str = (
    "Исходный текст:\n{text}\n\nОтредактируй исходный текст, исправив ошибки."
)

# Сообщения бота
MSG_WELCOME: str = (
    "👋 Привет! Я бот для автоматического исправления ошибок в тексте.\n\n"
    "Просто отправь мне любое сообщение — и я верну его исправленную версию. ✍️"
)

MSG_PROCESSING_ERROR: str = (
    "⚠️ Не удалось обработать текст. Попробуй ещё раз чуть позже."
)

# Команды, на которые бот показывает приветствие
GREETING_TRIGGERS: list[str] = [
    "start",
    "/start",
    "начать",
    "меню",
    "привет",
    "помощь",
    "help",
    "/help",
]
