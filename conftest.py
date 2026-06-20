# conftest.py
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data.test_data import BASE_URL, API_BASE_URL, AUTH_TOKEN


@pytest.fixture(scope="session")
def auth_token():
    """Возвращает токен авторизации"""
    if not AUTH_TOKEN:
        pytest.fail("AUTH_TOKEN не задан! Проверьте файл .env")
    return AUTH_TOKEN


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def api_base_url():
    return API_BASE_URL


@pytest.fixture(scope="session")
def api_session(auth_token):
    """Сессия curl_cffi, имитирующая реальный Chrome для обхода 403 ошибки"""
    from curl_cffi.requests import Session as CurlSession
    
    session = CurlSession(impersonate="chrome")
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    return session


@pytest.fixture
def driver():
    """Фикстура для создания драйвера браузера."""
    options = Options()
    # options.add_argument("--headless")  # Раскомментировать для фонового режима
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.implicitly_wait(10)
    yield driver
    driver.quit()