import sqlite3
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger("AppLogger")


class HistoryDatabase:
    def __init__(self, db_path: str = "operations_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_date TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    original_text TEXT,
                    processed_text TEXT,
                    prompt TEXT,
                    image_path TEXT
                )
            """)
            conn.commit()
            logger.info("Database initialized")

    def save_operation(
        self,
        operation_type: str,
        original_text: str,
        processed_text: str,
        prompt: str = None,
        image_path: str = None
    ) -> int:
        """Сохранение операции в базу данных"""
        timestamp = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO operations (
                    operation_date,
                    operation_type,
                    original_text,
                    processed_text,
                    prompt,
                    image_path
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, operation_type, original_text, processed_text, prompt, image_path))
            conn.commit()
            operation_id = cursor.lastrowid
        logger.info(f"Operation saved with id {operation_id}")
        return operation_id

    def get_history(self, limit: int = 20) -> List[Dict]:
        """Получение истории операций"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM operations 
                ORDER BY operation_date DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_operation_by_id(self, operation_id: int) -> Dict:
        """Получение конкретной операции по ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM operations WHERE id = ?", (operation_id,))
            result = cursor.fetchone()
            return dict(result) if result else None

    def delete_operation_by_id(self, operation_id: int) -> bool:
        """Удалить операцию по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM operations WHERE id = ?", (operation_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
        logger.info(f"Deleted operation {operation_id}: {deleted}")
        return deleted