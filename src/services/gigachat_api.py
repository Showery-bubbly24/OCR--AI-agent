import logging
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole
from config import GIGACHAT_API_SECRET, LICENCE_FILE

logger = logging.getLogger("AppLogger")


class GigaChatCorrector:
    def __init__(self):
        self.api_key = GIGACHAT_API_SECRET
        self.file = LICENCE_FILE
        try:
            self.gigachat = GigaChat(
                credentials=self.api_key,
                ca_bundle_file=self.file
            )
        except Exception as e:
            logger.error("GigaChat initialization failed: %s", e)
            raise

    def correct_text(self, text: str, promt: str | None) -> str:
        if promt is None:
            promt = ("<Promt>: Задача: Исправь граммитические ошибки в передаваемом тебе тексте. "
                     "В ответ передай тот же, но уже исправленный текст. ")

        try:
            logger.info("Request details - Text: %s, Prompt: %s", text[:100], promt)
            response = self.gigachat.chat(f"{promt}"
                                          f"Вот текст: {text}")
            return response.choices[0].message.content
        except Exception as e:
            logger.error("GigaChat API request failed: %s", e)
            raise
