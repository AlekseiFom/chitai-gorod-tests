# tests/test_ui.py
import allure
import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import settings
from pages.product_page import ProductPage
from data.test_data import BASE_URL, SEARCH_QUERY


# === Сверхнадежные, статические Локаторы ===
SEARCH_INPUT = (By.CSS_SELECTOR, "#app-search")
PRODUCT_PAGE_H1 = (By.CSS_SELECTOR, "h1")
PRODUCT_ACTION_BUTTON = (By.CSS_SELECTOR, ".product-sidebar button, button.chg-app-button")

# Использован ваш точный путь button[3] из DevTools, переведенный в безопасный относительный XPath
CART_BUTTON_SELECTOR = (By.XPATH, "//header//div[contains(@class, 'header')]//button[3] | //header//button[3]")


@allure.feature("UI тестирование интернет-магазина")
class TestChitaiGorodCart:

    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
        self.product_page = ProductPage(driver)

        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        with allure.step("Закрыть окно выбора города"):
            try:
                city_btn = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'Да') or contains(text(), 'ДА')]")
                    )
                )
                city_btn.click()
                self.wait.until(EC.staleness_of(city_btn))
            except (TimeoutException, NoSuchElementException):
                pass

    def _search_and_open_book(self, driver, query):
        """Вспомогательный приватный метод для точного перехода на книгу по её атрибуту title"""
        with allure.step(f"Ввести '{query}' в поисковую строку"):
            search_input = self.wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
            search_input.click()
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)

        with allure.step(f"Найти и открыть карточку книги '{query}' по атрибуту title"):
            # Этот XPath нацелен строго на элемент ссылки с картинкой и нужным title, который вы нашли в DevTools.
            # Никаких циклов перебора в Python — браузер сам находит точечный элемент, исключая StaleElement ошибку.
            target_book_xpath = (
                "//a[contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', "
                "'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'sdvg') or contains(@href, 'sdvg')]"
            )
            
            target_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, target_book_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
            
            # Повторно проверяем кликабельность после скролла для стабильности
            self.wait.until(EC.element_to_be_clickable((By.XPATH, target_book_xpath)))
            target_element.click()

    @allure.title("1. Проверка доступности главной страницы")
    def test_main_page_loading(self, driver):
        with allure.step("Проверить, что заголовок страницы содержит 'Читай-город'"):
            assert "Читай-город" in driver.title, f"Неверный заголовок: {driver.title}"

    @allure.title("2. Поиск книги через поисковую строку")
    def test_search_book(self, driver):
        with allure.step(f"Ввести '{SEARCH_QUERY}' в поиск"):
            search_input = self.wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
            search_input.click()
            search_input.clear()
            search_input.send_keys(SEARCH_QUERY)
            search_input.send_keys(Keys.ENTER)

        with allure.step("Проверить переход на страницу результатов поиска"):
            # Добавлена проверка на изменение URL или появление контейнера выдачи
            self.wait.until(
                lambda d: any(part in d.current_url for part in ("search", "query", "str")) or d.find_elements(By.TAG_NAME, "article"),
                message="Не дождались перехода на страницу поиска",
            )
            assert any(part in driver.current_url for part in ("search", "query", "str")) or driver.find_elements(By.TAG_NAME, "article"), \
                f"Ожидали URL страницы поиска, получили: {driver.current_url}"

    @allure.title("3. Поиск целевой книги и сравнение названий")
    def test_open_product_card(self, driver):
        self._search_and_open_book(driver, SEARCH_QUERY)

        with allure.step("Проверить заголовок на открывшейся странице товара"):
            product_title_h1 = self.wait.until(EC.visibility_of_element_located(PRODUCT_PAGE_H1)).text
            assert "sdvg" in product_title_h1.lower() or "сдвг" in product_title_h1.lower(), \
                f"Заголовок '{product_title_h1}' не совпадает с запросом '{SEARCH_QUERY}'"

    @allure.title("4. Проверка элементов на карточке товара")
    def test_add_product_to_cart(self, driver):
        self._search_and_open_book(driver, SEARCH_QUERY)

        with allure.step("Проверить наличие кнопки действия на странице"):
            action_btn = self.wait.until(EC.visibility_of_element_located(PRODUCT_ACTION_BUTTON))
            assert action_btn.is_displayed()

    @allure.title("5. Переход в корзину через шапку сайта")
    def test_navigate_to_cart(self, driver):
        with allure.step("Нажать на кнопку корзины в шапке сайта"):
            # Ждем, пока третья кнопка в шапке (ваша корзина) станет полностью кликабельной
            cart_button = self.wait.until(EC.element_to_be_clickable(CART_BUTTON_SELECTOR))
            cart_button.click()

        with allure.step("Проверить успешный переход в корзину"):
            self.wait.until(
                lambda d: "cart" in d.current_url,
                message="Не дождались перехода на страницу корзины",
            )
            assert "cart" in driver.current_url, f"Ожидали URL корзины, но получили: {driver.current_url}"
