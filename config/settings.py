# config/settings.py
"""
Настройки окружения для проекта автотестов Читай-город.
Все настройки подгружаются из .env, либо берутся дефолтные значения.
"""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env (если он создан)
load_dotenv()

# API URL (исправлено на стабильный v2 под шлюз)
API_BASE_URL = os.getenv(
    "API_BASE_URL", "https://chitai-gorod.ru"
)

# Основной сайт с www для стабильности UI-тестов
BASE_URL = os.getenv("BASE_URL", "https://www.chitai-gorod.ru")

# Таймаут ожидания элементов по умолчанию
EXPLICIT_WAIT = 15

# Тестовые данные для книг по умолчанию
TEST_BOOK_ID = os.getenv("TEST_BOOK_ID", "3107597")
TEST_BOOK_TITLE = "Я не ленивый, глупый или сумасшедший..."

# Токен авторизации
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")


class Settings:
    """Класс-синглтон для удобного импорта настроек через точку"""

    BASE_URL = BASE_URL
    API_BASE_URL = API_BASE_URL
    EXPLICIT_WAIT = EXPLICIT_WAIT
    AUTH_TOKEN = AUTH_TOKEN
    TEST_BOOK_ID = TEST_BOOK_ID
    TEST_BOOK_TITLE = TEST_BOOK_TITLE


# Создаем экземпляр для импорта в тесты
settings = Settings()
