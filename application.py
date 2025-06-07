import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QFileDialog, QMenuBar, QMenu,
                             QAction, QHBoxLayout, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QImage
import cv2
import numpy as np
from main import read_photo, correct_with_gigachat


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('Drag and drop image here\nor click "Choose file" button')
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
            }
        ''')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasImage or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toLocalFile()
            self.setPixmap(QPixmap(url).scaled(
                400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image processing')
        self.setFixedSize(800, 600)

        # Создаем меню-бар
        self.create_menu_bar()

        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Левая часть с изображением
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Правая часть с текстом
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Создаем виджеты для левой части
        self.image_label = ImageLabel()
        self.image_label.setFixedSize(400, 400)

        self.select_btn = QPushButton('Choose file')
        self.select_btn.clicked.connect(self.select_image)

        self.process_btn = QPushButton('Get text')
        self.process_btn.clicked.connect(self.process_image)

        # Создаем виджеты для правой части
        self.text_label = QLabel('Recognized text:')
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.improve_btn = QPushButton('Improve text with AI')
        self.improve_btn.clicked.connect(self.improve_text)

        # Добавляем виджеты на левый layout
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.select_btn)
        left_layout.addWidget(self.process_btn)

        # Добавляем виджеты на правый layout
        right_layout.addWidget(self.text_label)
        right_layout.addWidget(self.text_edit)
        right_layout.addWidget(self.improve_btn)

        # Добавляем левую и правую части на главный layout
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu('File')

        # Действие "Сбросить"
        reset_action = QAction('Reset', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.triggered.connect(self.reset_app)

        # Действие "Выход"
        exit_action = QAction('Close', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        # Добавляем действия в меню
        file_menu.addAction(reset_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def reset_app(self):
        self.image_label.setPixmap(QPixmap())  # Очищаем изображение
        self.image_label.setText('Drag and drop image here\nor click "Choose file" button')
        self.text_edit.clear()  # Очищаем текст

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Choose Image',
            '',
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        if file_name:
            self.current_image_path = file_name  # Сохраняем путь к файлу
            self.image_label.setPixmap(QPixmap(file_name).scaled(
                400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def process_image(self):
        if hasattr(self, 'current_image_path'):
            image = cv2.imread(self.current_image_path)

            try:
                res = read_photo(image)

                # Устанавливаем полученный текст в text_edit
                self.text_edit.setText(res)
            except Exception as e:
                self.text_edit.setText(f"Error: {e}")

    def improve_text(self):
        # Получаем текст из text_edit
        text = self.text_edit.toPlainText()

        if text:
            try:
                res = correct_with_gigachat(text)
                self.text_edit.setText(res)
            except Exception as e:
                self.text_edit.setText(f"Error: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
