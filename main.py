import cv2
import easyocr
import numpy as np
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole


def correct_with_gigachat(text):
    # Request to GigaChat
    try:
        giga = GigaChat(
            credentials="<Your API-key to GigaChat>",
            ca_bundle_file="<Your file (path2file> for certification"
        )

        response = giga.chat("<Promt>: Задача: Исправь граммитические ошибки в передаваемом тебе тексте. "
                             "В ответ передай тот же, но уже исправленный текст. "
                             f"Вот текст: {text} <Promt>")

        # Return responce from GigaChat
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error with GigaChat API: {e}")
        return text


def read_photo(image):
    # Read photo
    try:
        if image is None:
            print('Error: image is None')
            return None

        reader = easyocr.Reader(['ru', 'en'])
        results = reader.readtext(image)

        if not results:
            print("Text is None")
            return None

        full_text = ' '.join([text for _, text, _ in results])

        # Return the entire text read
        return full_text

    except Exception as e:
        print(f"Error: {e}")
        return None
