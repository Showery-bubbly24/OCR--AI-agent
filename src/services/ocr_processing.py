import cv2
import easyocr
import numpy as np
import logging

logger = logging.getLogger("AppLogger")


class OCRREADER:
    def __init__(self, languages: list | None):
        if languages is None:
            languages = ['ru', 'en']

        try:
            logger.info("Loading OCR")
            self.ocr_processor = easyocr.Reader(languages, gpu=False)
        except Exception as e:
            logger.error("OCR initialization failed: %s", e)
            raise

    def extract_text(self, image: str) -> str:
        try:
            logger.info("Extracting text from image: %s", image)
            self.img = cv2.imread(image)
            if self.img is None:
                logger.error("Image not found or invalid format: %s", image)
                raise FileNotFoundError(f"Image not found: {image}")

            self.text = self.ocr_processor.readtext(self.img)
            return ' '.join([text for _, text, _ in self.text])
        except Exception as e:
            logger.error("OCR processing failed for image: %s", image)
            logger.exception("OCR error details")
            raise
