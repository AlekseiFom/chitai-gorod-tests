# pages/order_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Локаторы (замените на реальные селекторы сайта)
        self.DELIVERY_ADDRESS = (By.CSS_SELECTOR, "input[name='address'], #address, [data-testid='address']")
        self.PAYMENT_METHOD = (By.CSS_SELECTOR, ".payment-method, .payment-option, [data-testid='payment']")
        self.SUBMIT_ORDER = (By.CSS_SELECTOR, ".submit-order-btn, .confirm-order, [data-testid='submit-order']")
        self.ORDER_SUCCESS = (By.CSS_SELECTOR, ".order-success, .success-message, .order-confirmed")

    @allure.step("Ввести адрес доставки: '{address}'")
    def enter_delivery_address(self, address):
        try:
            field = self.wait.until(EC.element_to_be_clickable(self.DELIVERY_ADDRESS))
            field.click()
            field.clear()
            field.send_keys(address)
            print(f"✅ Адрес '{address}' введён")
        except Exception:
            print("⚠️ Поле ввода адреса не найдено")
        return self

    @allure.step("Выбрать способ оплаты")
    def select_payment_method(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD))
            element.click()
            print("✅ Способ оплаты выбран")
        except Exception:
            print("⚠️ Способ оплаты не найден")
        return self

    @allure.step("Подтвердить заказ")
    def submit_order(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ORDER))
            btn.click()
            print("✅ Заказ подтверждён")
        except Exception:
            print("⚠️ Кнопка подтверждения заказа не найдена")
        return self

    @allure.step("Проверить, что заказ успешно оформлен")
    def is_order_confirmed(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.ORDER_SUCCESS))
            print("✅ Заказ успешно оформлен!")
            return True
        except Exception:
            print("❌ Сообщение об успешном оформлении не найдено")
            return False

    @allure.step("Получить текст сообщения об успехе")
    def get_success_message(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.ORDER_SUCCESS))
            return element.text
        except Exception:
            pass
            return "Сообщение не найдено"