from PyQt5.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from src.utils.database import HistoryDatabase


class HistoryWindow(QWidget):
    operation_selected = pyqtSignal(dict)  # Сигнал для передачи выбранной операции

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operation History")
        self.resize(700, 500)

        self.db = HistoryDatabase()
        self.operations = []

        self.layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.layout.addWidget(QLabel("Recent operations:"))
        self.layout.addWidget(self.list_widget)

        # Кнопки действий
        button_layout = QHBoxLayout()
        self.select_button = QPushButton("Use selected")
        self.delete_button = QPushButton("Delete selected")

        self.select_button.clicked.connect(self.select_operation)
        self.delete_button.clicked.connect(self.delete_operation)

        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

        self.populate_list()

    def populate_list(self):
        """Обновить список операций"""
        self.operations = self.db.get_history()
        self.list_widget.clear()

        for op in self.operations:
            preview = op['operation_date'] + " | " + op['operation_type']
            prompt = op.get('prompt')
            if prompt:
                preview += f" | Prompt: {prompt[:30]}..."
            self.list_widget.addItem(preview)

    def select_operation(self):
        selected_index = self.list_widget.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "No selection", "Please select an operation from the list.")
            return
        selected_op = self.operations[selected_index]
        self.operation_selected.emit(selected_op)

    def delete_operation(self):
        selected_index = self.list_widget.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "No selection", "Select a record to delete.")
            return

        selected_op = self.operations[selected_index]
        op_id = selected_op["id"]

        confirm = QMessageBox.question(
            self,
            "Delete operation",
            f"Do you really want to delete operation ID {op_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success = self.db.delete_operation_by_id(op_id)
            if success:
                QMessageBox.information(self, "Deleted", f"Operation {op_id} was deleted.")
                self.populate_list()
            else:
                QMessageBox.warning(self, "Error", "Could not delete operation.")