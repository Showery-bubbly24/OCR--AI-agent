import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.logger import setup_logger

if __name__ == "__main__":
    logger = setup_logger()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
