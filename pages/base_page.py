# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator):
        """Клик по элементу"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self

    def enter_text(self, locator, text):
        """Ввод текста в поле"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element.text

    def is_element_present(self, locator):
        """Проверить, что элемент присутствует"""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def close_city_modal(self):
        """Закрыть окно выбора города (если появляется)"""
        try:
            close_btn = (By.CSS_SELECTOR, ".chg-app-button--breeze.chg-app-button--block")
            if self.is_element_present(close_btn):
                self.click(close_btn)
                return True
        except Exception:
            pass
        return False