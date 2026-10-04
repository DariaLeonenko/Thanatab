import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@patch("backend.database.get_bookmarks")
def test_app_imports_successfully(mock_get_bookmarks):
    """Тест проверяет, что app.py импортируется без ошибок, даже если БД нет."""
    # Мокаем ответ базы данных, чтобы код внизу app.py не упал
    mock_get_bookmarks.return_value = []

    # Если импорт прошел без исключений — тест зеленый
    import frontend.app  # noqa: F401
    assert True