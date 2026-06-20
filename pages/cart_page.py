# pages/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Локаторы
        self.CART_ITEMS = (By.CSS_SELECTOR, ".cart-item, .basket-item, .cart-product")
        self.EMPTY_CART = (By.CSS_SELECTOR, ".empty-cart, .cart-empty, .empty")
        self.CHECKOUT_BTN = (By.CSS_SELECTOR, ".checkout-btn, .order-btn, .proceed-btn")
        self.TOTAL_PRICE = (By.CSS_SELECTOR, ".cart-total, .total-price, .summary-total")
        self.CART_COUNTER = (By.CSS_SELECTOR, ".cart-counter, .header-cart .count")

    @allure.step("Получить количество товаров в корзине")
    def get_items_count(self):
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)

    @allure.step("Проверить, пуста ли корзина")
    def is_cart_empty(self):
        try:
            return self.driver.find_element(*self.EMPTY_CART).is_displayed()
        except Exception:
            return False

    @allure.step("Получить общую сумму корзины")
    def get_total_price(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.TOTAL_PRICE))
            return element.text
        except Exception:
            return "Не найдено"

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN))
            btn.click()
            print("✅ Переход к оформлению заказа")
            from pages.order_page import OrderPage
            return OrderPage(self.driver)
        except Exception:
            print("⚠️ Кнопка оформления заказа не найдена")
            return None

    @allure.step("Получить значение счётчика корзины")
    def get_cart_counter(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.CART_COUNTER))
            return element.text
        except Exception:
            return "0"