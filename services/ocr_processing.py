import cv2
import easyocr
import numpy as np


class OCRREADER:
    def __init__(self, languages: list | None):
        if languages is None:
            languages = ['ru', 'en']

        self.ocr_processor = easyocr.Reader(languages, gpu=False)

    def extract_text(self, image: str) -> str:
        self.img = cv2.imread(image)
        self.text = self.ocr_processor.readtext(self.img)
        return ' '.join([text for _, text, _ in self.text])
