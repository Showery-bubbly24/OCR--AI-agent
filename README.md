# OCR + GigaChat Corrector

📚 Простое desktop-приложение с графическим интерфейсом на **PyQt5**, выполняющее:
- Распознавание текста (OCR) из изображений
- Коррекцию текста с помощью **GigaChat API**
- Хранение истории операций в **SQLite**
  
> Приложение предназначено для быстрой обработки документов с использованием ИИ-корректора.

---

## 📸 Превью

![Screenshot 2025-06-11 at 3.19.48 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fth%2Fsbl35b8x2_q1x3973rds7ddr0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_b0dIBd%2FScreenshot%202025-06-11%20at%203.19.48%E2%80%AFPM.png)

---

## 🚀 Возможности

- 🔍 Распознавание текста из изображений (.png, .jpg, .jpeg, .bmp)
- 🤖 Постобработка текста с помощью GigaChat (с поддержкой промптов)
- 💾 Хранение истории операций с датой, типом, текстом, изображением
- 📂 Просмотр истории и восстановление старых операций
- 🧹 Удаление ненужных записей
- 📦 Удобный пользовательский интерфейс на PyQt5

---

## 🛠️ Установка

### 🔧 Необходимые зависимости:

Установить через `pip`:

```bash
pip install -r requirements.txt
```

### 👨‍💻 Запуск приложения
```bash
python main.py
```

---

## 📁 Структура проекта
```
ocr-gigachat-app/
├── logs/
│   ├── app_20250610_142521.log
│   ├── ...
│   └── app_20250610_192342.log
├── material/
│   ├── photo1.png
│   ├── ...
│   └── document_n.jpeg
├── screenshots/
│   ├── main.png
│   ├── ...
│   └── history.png
├── src/
│   ├── gui/
│   │   ├── main_window.py
│   │   └── history_window.py
│   ├── services/
│   │   ├── ocr_processing.py
│   │   └── gigachat_api.py
│   └── utils/
│   │   └── database.py
│   ├── tests/
│   │   ├── test_ocr_service.py
│   │   ├── ...
│   │   └── test_database.py
│   └── logger.py
├── .gitignore
├── config.py
├── main.py
├── operations_history.db    # SQLite база
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## ✅ Использование
▶️ 1. Загрузка изображения
Перетаскиваете или открываете файл → происходит OCR → текст появляется в окне.

🧠 2. Ввод промпта и коррекция
Пишете промпт (опционально) → нажимаете Upgrade with GigaChat → корректированный текст заменит оригинал.

📜 3. Запись сохраняется в истории
Можно перейти в View → History View и:
- 🔁 Повторно загрузить операцию
- 🗑 Удалить ненужную

---

## 🛡️ Тестирование
### Инициализация тестирования
```bash
pytest
```

### Предметы тестирования:
- Сохранение операций
- Получение по ID
- История
- Удаление

### Примерный результат тестирования
```bash
========================================================================================== test session starts ==========================================================================================
@user.python_ai_ocr_tool # pytest
platform darwin -- Python 3.12.2, pytest-8.4.0, pluggy-1.6.0 -- /Users/daniilbelokonev/PycharmProjects/aiAgent/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/daniilbelokonev/PycharmProjects/aiAgent
configfile: pytest.ini
plugins: anyio-4.9.0
collected 10 items                                                                                                                                                                                      

src/tests/test_database.py::test_get_save_operations PASSED                                                                                                                                       [ 10%]
src/tests/test_database.py::test_get_history PASSED                                                                                                                                               [ 20%]
src/tests/test_database.py::test_delete PASSED                                                                                                                                                    [ 30%]
src/tests/test_database.py::test_delete_non_existing_db PASSED                                                                                                                                    [ 40%]
src/tests/test_gigachat.py::TestGigaChatCorrector::test_correct_with_prompt PASSED                                                                                                                [ 50%]
src/tests/test_gigachat.py::TestGigaChatCorrector::test_correct_without_prompt PASSED                                                                                                             [ 60%]
src/tests/test_gigachat.py::TestGigaChatCorrector::test_gigachat_init_failure PASSED                                                                                                              [ 70%]
src/tests/test_gigachat.py::TestGigaChatCorrector::test_gigachat_chat_failure PASSED                                                                                                              [ 80%]
src/tests/test_ocr_reader.py::test_extract_text_success PASSED                                                                                                                                    [ 90%]
src/tests/test_ocr_reader.py::test_extract_text_file_not_found PASSED                                                                                                                             [100%]

========================================================================================== 10 passed in 2.21s ===========================================================================================
```

---

## 🤝 Вклад
### Хочешь предложить доработку?
- Сделай fork
- Разработай свою фичу / багфикс в отдельной ветке
- Оформи Pull Request

```bash
git checkout -b feature/имя
```

---

## ⚙️ Переменные окружения
ИИ работает с помощью SecretAPIkey и Сертифицирование(ca_bundle), **обрати внимания что без них проект полноценно работать не будет**: 
```python
GIGACHAT_API_SECRET = '#### <- Your api key'
LICENCE_FILE = '### <-  path to your ca bundle'
```

---

## 📌 TODO / Идеи
- Поддержка drag & drop
- Поддержка GigaChat V2 / Multimodal
- Стилизация окна и Layout UI
- Экспорт PDF / DOCX

--- 

## 📃 Лицензия
- MIT License

---

## 📬 Контакты
- Разработчик: Showery_bubbly24
- Телеграм: @miracle_boy24
