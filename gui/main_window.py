from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QFileDialog, QTextEdit, QLabel,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
)
from config import OCR_LANGUAGES
from services.ocr_processing import OCRREADER
from services.gigachat_api import GigaChatCorrector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ocr = OCRREADER(['ru', 'en'])
        self.corrector = GigaChatCorrector()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OCR + GigaChat Correction")

        layout = QVBoxLayout()

        # Поле для отображения/редактирования текста
        self.text_area = QTextEdit()

        # Поле для ввода промта
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter promt for GigaChat (optional)")

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.load_button = QPushButton("Load image")
        self.correct_button = QPushButton("Upgrade with GigaChat")
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.correct_button)

        # Статус
        self.status_label = QLabel()

        # Подключение событий
        self.load_button.clicked.connect(self.load_image)
        self.correct_button.clicked.connect(self.correct_text_with_prompt)

        # Сборка интерфейса
        layout.addWidget(self.text_area)
        layout.addWidget(QLabel("Promt for AI:"))
        layout.addWidget(self.prompt_input)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image")
        if file_path:
            try:
                extracted_text = self.ocr.extract_text(file_path)
                self.text_area.setPlainText(extracted_text)
                self.status_label.setText("Recognition complete")
            except Exception as e:
                self.status_label.setText(f"Recognition error: {e}")

    def correct_text_with_prompt(self):
        text = self.text_area.toPlainText()
        prompt = self.prompt_input.text() or None  # Если пусто — None
        if text.strip():
            try:
                corrected_text = self.corrector.correct_text(text, prompt)
                self.text_area.setPlainText(corrected_text)
                self.status_label.setText("Correction completed")
            except Exception as e:
                self.status_label.setText(f"Correction error: {e}")
