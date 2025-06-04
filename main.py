import cv2
import easyocr
import numpy as np
from langchain_community.llms import Ollama
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

reader = None


def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['ru', 'en'])
    return reader


# def preprocess_image(image):
#     if image is None:
#         raise ValueError("Передано пустое изображение")
#     if len(image.shape) < 2:
#         raise ValueError("Некорректный формат изображения")
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     denoised = cv2.GaussianBlur(gray, (3, 3), 0)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(denoised)
#     binary = cv2.adaptiveThreshold(
#         enhanced,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11, 2)
#     return binary


def correct_with_ollama(text):
    try:
        llm = Ollama(model="qwen2:7b")
        prompt = f"""Задача: исправь текст документа.
        Правила:
        1. Исправить ошибки распознавания OCR
        2. Сохранить все даты, числа и имена собственные
        3. Исправить орфографию и пунктуацию
        4. Структурировать текст
        5. Не обогащать исходный текст своими словами (за исключением слов, которые используются для структурирования)

        Текст: {text}
        """

        corrected = llm(prompt)
        return corrected
    except Exception as e:
        logger.error(f"Ошибка при работе с Ollama: {e}")
        return text


def correct_long_text(text, max_length=500):
    if not isinstance(text, str):
        raise TypeError("Текст должен быть строкой")
    if max_length <= 0:
        raise ValueError("max_length должен быть положительным числом")

    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    corrected_parts = []
    for part in parts:
        corrected = correct_with_ollama(part)
        corrected_parts.append(corrected)
    return ' '.join(corrected_parts)


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

        corrected_text = correct_long_text(full_text)
        logger.info("Исправленный текст:")
        print(corrected_text)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
