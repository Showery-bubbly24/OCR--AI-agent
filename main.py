import cv2
import easyocr
import numpy as np
from langchain_community.llms import Ollama
import logging
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

reader = None


def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['ru', 'en'])
    return reader


def correct_with_gigachat(text):
    try:
        giga = GigaChat(
            credentials="<Ваш апи токен>",
            ca_bundle_file="<Ваш файл для сертификации>"
        )

        response = giga.chat("Задача: Исправь граммитические ошибки в передаваемом тебе тексте. "
                             "В ответ передай тот же, но уже исправленный текст. "
                             f"Вот текст: {text}")
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Ошибка при работе с GigaChat API: {e}")
        return text


# def correct_long_text(text, max_length=500):
#     if not isinstance(text, str):
#         raise TypeError("Текст должен быть строкой")
#     if max_length <= 0:
#         raise ValueError("max_length должен быть положительным числом")
#
#     parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
#     corrected_parts = []
#     for part in parts:
#         corrected = correct_with_gigachat(part)
#         corrected_parts.append(corrected)
#     return ' '.join(corrected_parts)


if __name__ == "__main__":
    try:
        logger.info("Начало обработки изображения")
        image = cv2.imread('./material/photo.jpg')
        if image is None:
            raise FileNotFoundError("Не удалось загрузить изображение")

        # binary = preprocess_image(image)

        try:
            reader = get_reader()
            results = reader.readtext(image)
        except Exception as e:
            logger.error(f"Ошибка при распознавании текста: {e}")
            results = []

        if not results:
            logger.error("Текст не распознан")
            exit(1)

        full_text = ' '.join([text for _, text, _ in results])
        logger.info("Исходный текст:")
        print(full_text)

        # corrected_text = correct_long_text(full_text)
        corrected_text = correct_with_gigachat(full_text)
        logger.info("Исправленный текст:")
        print(corrected_text)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
