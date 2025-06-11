import os
import pytest
from src.utils.database import HistoryDatabase

DB_TEST_PATH = "test_operations_history.db"


@pytest.fixture
def test_db():
    # Удалим базу перед каждым прогоном
    if os.path.exists(DB_TEST_PATH):
        os.remove(DB_TEST_PATH)
    db = HistoryDatabase(db_path=DB_TEST_PATH)
    yield db
    # После теста — удалить
    if os.path.exists(DB_TEST_PATH):
        os.remove(DB_TEST_PATH)


def test_get_save_operations(test_db):
    op_id = test_db.save_operation(
        operation_type="OCR",
        original_text="original text",
        processed_text=None,
        prompt=None,
        image_path="some/path/to/image.jpg"
    )

    assert isinstance(op_id, int)
    assert op_id > 0

    data = test_db.get_operation_by_id(op_id)
    assert data is not None
    assert data["original_text"] == "original text"
    assert data["operation_type"] == "OCR"


def test_get_history(test_db):
    test_db.save_operation("OCR", "text1", None, None, "path1")
    test_db.save_operation("Correction", "text2", "corrected", "promt", "path2")

    history = test_db.get_history()
    assert isinstance(history, list)
    assert len(history) == 2
    assert history[0]["operation_type"] in ("OCR", "Correction")


def test_delete(test_db):
    op_id = test_db.save_operation(
        operation_type="OCR",
        original_text="to delete",
        processed_text=None,
        prompt=None,
        image_path=None
    )

    op = test_db.get_operation_by_id(op_id)
    assert op is not None

    deleted = test_db.delete_operation_by_id(op_id)
    assert deleted is True

    op_after = test_db.get_operation_by_id(op_id)
    assert op_after is None


def test_delete_non_existing_db(test_db):
    deleted = test_db.delete_operation_by_id(9999)
    assert deleted is False
