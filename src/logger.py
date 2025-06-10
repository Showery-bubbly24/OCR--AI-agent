import logging
import os
from datetime import datetime


def setup_logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):  # Исправлено: убрано src.
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"app_{timestamp}.log")

    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.INFO)  # Установка уровня для логгера

    # Создание форматтера
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Добавление обработчиков к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger