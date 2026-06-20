# pages/search_results_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class SearchResultsPage:
    """Страница результатов поиска"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.PRODUCT_CARDS = (By.CSS_SELECTOR, "[data-testid-product-item]")
        self.BOOK_TITLE = (By.CSS_SELECTOR, '[title*="СДВГ 2.0"]')

    @allure.step("Открыть книгу 'СДВГ 2.0'")
    def open_book(self):
        """Находит книгу по заголовку и открывает её"""
        # ✅ Находим элемент с нужным title
        book_element = self.wait.until(
            EC.presence_of_element_located(self.BOOK_TITLE)
        )
        
        # ✅ Поднимаемся до карточки и ищем ссылку
        card = book_element.find_element(By.XPATH, "./ancestor::*[contains(@data-testid-product-item, '')]")
        link = card.find_element(By.CSS_SELECTOR, "a")
        link.click()
        
        print("✅ Книга 'СДВГ 2.0' открыта")
        
        from pages.product_page import ProductPage
        return ProductPage(self.driver)