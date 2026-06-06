"""
Сервис исправления ошибок — изолированная обёртка над spell-correction API.
"""

import logging

from openai import AsyncOpenAI, OpenAIError

from config import (
    SPELL_API_KEY,
    SPELL_API_BASE_URL,
    SPELL_MODEL,
    SPELL_PROMPT_TEMPLATE,
    SPELL_TEMPERATURE,
    SPELL_TOP_P,
)


logger = logging.getLogger(__name__)


# Клиент создаётся один раз и переиспользуется (connection pooling)
_client = AsyncOpenAI(
    api_key=SPELL_API_KEY,
    base_url=SPELL_API_BASE_URL,
)


async def correct_text(text: str) -> str:
    """
    Отправляет текст в модель и возвращает исправленную версию.

    :param text: Исходный текст с ошибками.
    :returns: Исправленный текст.
    :raises OpenAIError: При сетевых или API-ошибках.
    """
    prompt = SPELL_PROMPT_TEMPLATE.format(text=text)

    response = await _client.chat.completions.create(
        model=SPELL_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=SPELL_TEMPERATURE,
        top_p=SPELL_TOP_P,
    )

    corrected: str = response.choices[0].message.content
    logger.debug("Spell correction done. Original=%d chars, result=%d chars", len(text), len(corrected))
    return corrected
