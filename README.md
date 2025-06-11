# OCR--AI-agent

========================================================================================== test session starts ==========================================================================================
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
(.venv) daniilbelokonev@Noutbuk-Daniil aiAgent % 
