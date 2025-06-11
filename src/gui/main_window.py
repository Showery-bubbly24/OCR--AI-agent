from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QLineEdit, QFileDialog, QAction, QMenuBar, QFormLayout,
    QStatusBar, QStackedWidget
)
from PyQt5.QtCore import Qt
import logging

from src.services.ocr_processing import OCRREADER
from src.services.gigachat_api import GigaChatCorrector
from src.utils.database import HistoryDatabase
from src.gui.history_window import HistoryWindow

logger = logging.getLogger("AppLogger")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            logger.info("Initializing GUI")
            self.ocr = OCRREADER(['ru', 'en'])
            self.db = HistoryDatabase()
            self.corrector = GigaChatCorrector()
            self.loaded_image_path = None
            self.init_ui()
        except Exception as e:
            logger.critical("Application initialization failed: %s", e)
            raise

    def init_ui(self):
        self.setWindowTitle("OCR + GigaChat Correction")
        self.resize(1000, 700)

        # === Центральный стек для переключения экранов ===
        self.stacked_widget = QStackedWidget()

        # === Главное окно ===
        self.main_view = self.build_main_view()
        self.stacked_widget.addWidget(self.main_view)

        # === Окно истории ===
        self.history_view = self.build_history_view()
        self.stacked_widget.addWidget(self.history_view)

        self.setCentralWidget(self.stacked_widget)

        # === Меню-бар ===
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        view_menu = menu_bar.addMenu("View")

        main_action = QAction("Main View", self)
        main_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        view_menu.addAction(main_action)

        history_action = QAction("History View", self)
        history_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        view_menu.addAction(history_action)

        # === Статус-бар ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def build_main_view(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # === Текстовое поле ===
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Extracted or corrected text will appear here...")
        layout.addWidget(self.text_area)

        # === Промпт + статус ===
        form_layout = QFormLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter prompt for GigaChat (optional)")
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: green")
        form_layout.addRow("Prompt:", self.prompt_input)
        form_layout.addRow("Status:", self.status_label)
        layout.addLayout(form_layout)

        # === Кнопки действий ===
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load image")
        self.correct_button = QPushButton("Upgrade with GigaChat")

        self.load_button.clicked.connect(self.load_image)
        self.correct_button.clicked.connect(self.correct_text_with_prompt)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.correct_button)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        return widget

    def build_history_view(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # создаем НОВЫЙ, всегда актуальный HistoryWindow
        self.history_widget = HistoryWindow()
        self.history_widget.operation_selected.connect(self.load_history_operation)

        layout.addWidget(QLabel("Recent operations:"))
        layout.addWidget(self.history_widget)

        widget.setLayout(layout)
        return widget

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Image",
            filter="Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            try:
                extracted_text = self.ocr.extract_text(file_path)
                self.text_area.setPlainText(extracted_text)
                self.status_label.setText("Recognition complete")
                self.status_bar.showMessage("Image recognized")
                self.loaded_image_path = file_path

                self.db.save_operation(
                    operation_type="OCR",
                    original_text=extracted_text,
                    processed_text=None,
                    prompt=None,
                    image_path=file_path
                )

                logger.info(f"OCR successful: {file_path}")

            except Exception as e:
                msg = f"Recognition error: {e}"
                self.status_label.setText(msg)
                self.status_bar.showMessage("OCR failed", 5000)
                logger.error(msg)

    def correct_text_with_prompt(self):
        original_text = self.text_area.toPlainText()
        prompt = self.prompt_input.text().strip() or None

        if not original_text.strip():
            self.status_bar.showMessage("No text to correct", 3000)
            return

        try:
            corrected_text = self.corrector.correct_text(original_text, prompt)
            self.text_area.setPlainText(corrected_text)
            self.status_label.setText("Correction completed")
            self.status_bar.showMessage("Text corrected with GigaChat")

            self.db.save_operation(
                operation_type="Correction",
                original_text=original_text,
                processed_text=corrected_text,
                prompt=prompt,
                image_path=self.loaded_image_path
            )
            logger.info("Correction completed and saved.")

        except Exception as e:
            msg = f"Correction error: {e}"
            self.status_label.setText(msg)
            self.status_bar.showMessage("Correction failed", 5000)
            logger.error(msg)

    def load_history_operation(self, operation: dict):
        """Загрузка текста/промпта из истории в главное окно"""
        if operation.get('processed_text'):
            self.text_area.setPlainText(operation['processed_text'])
        elif operation.get('original_text'):
            self.text_area.setPlainText(operation['original_text'])

        self.prompt_input.setText(operation.get('prompt') or "")
        self.loaded_image_path = operation.get('image_path') or None
        self.status_label.setText(f"Loaded from history (ID: {operation['id']})")
        self.status_bar.showMessage(f"History operation loaded.")

        # Автоматически переключаемся обратно на главное окно
        self.stacked_widget.setCurrentIndex(0)
