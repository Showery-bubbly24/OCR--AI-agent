import pytest
from src.services.gigachat_api import GigaChatCorrector
from unittest.mock import MagicMock, patch


class TestGigaChatCorrector:
    @patch('src.services.gigachat_api.GigaChat')
    def test_correct_with_prompt(self, mock_giga):
        # Настраиваем mock
        mock_instance = mock_giga.return_value
        mock_instance.chat.return_value.choices = [MagicMock()]
        mock_instance.chat.return_value.choices[0].message.content = "Исправленный текст"

        # Тестируем
        corrector = GigaChatCorrector()
        result = corrector.correct_text("орфографические ошибки в тексте", "Сделай текст официальным:")
        assert result == "Исправленный текст"

    @patch('src.services.gigachat_api.GigaChat')
    def test_correct_without_prompt(self, mock_giga):
        # Настраиваем mock
        mock_instance = mock_giga.return_value
        mock_instance.chat.return_value.choices = [MagicMock()]
        mock_instance.chat.return_value.choices[0].message.content = "Исправленный текст"

        # Тестируем
        corrector = GigaChatCorrector()
        result = corrector.correct_text("ошибки в тексте", None)
        assert result == "Исправленный текст"

    @patch('src.services.gigachat_api.GigaChat', side_effect=Exception("Auth Error"))
    def test_gigachat_init_failure(self, mock_giga):
        with pytest.raises(Exception) as e:
            GigaChatCorrector()
        assert "Auth Error" in str(e.value)

    def test_gigachat_chat_failure(self):
        with patch('src.services.gigachat_api.GigaChat') as mock_giga:
            # Настраиваем mock для вызова исключения при chat
            mock_instance = mock_giga.return_value
            mock_instance.chat.side_effect = Exception("API Failure")

            corrector = GigaChatCorrector()
            with pytest.raises(Exception) as e:
                corrector.correct_text("ошибки", None)
            assert "API Failure" in str(e.value)