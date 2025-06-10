import pytest
import numpy as np
from src.services.ocr_processing import OCRREADER


class DummyOCRProcessor:
    def readtext(self, img):
        return [(0, "TestText", 0.9)]


@pytest.fixture
def patch_easyocr(monkeypatch):
    def dummy_reader(languages, gpu):
        return DummyOCRProcessor()

    monkeypatch.setattr("services.ocr_processing.easyocr.Reader", dummy_reader)


@pytest.fixture
def patch_cv2(monkeypatch):
    def dummy_imread(path):
        return np.zeros((100, 100, 3), dtype=np.uint8)  # Поддельное изображение

    monkeypatch.setattr("services.ocr_processing.cv2.imread", dummy_imread)


def test_extract_text_success(patch_easyocr, patch_cv2):
    reader = OCRREADER(['en'])
    text = reader.extract_text("dummy_path.png")
    assert text == "TestText"


def test_extract_text_file_not_found(patch_easyocr, monkeypatch):
    # Подменяем cv2.imread, чтобы возвращал None (симулируем отсутствие файла)
    monkeypatch.setattr("services.ocr_processing.cv2.imread", lambda path: None)

    reader = OCRREADER(['en'])
    with pytest.raises(FileNotFoundError):
        reader.extract_text("missing_image.png")
