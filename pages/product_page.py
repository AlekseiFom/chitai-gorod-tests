# pages/product_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

from config.settings import settings


class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)

        self.ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".product-buttons__main-action.product-buttons__main-action--stretch")

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        # ✅ Находим кнопку заново
        add_btn = self.wait.until(EC.presence_of_element_located(self.ADD_TO_CART_BTN))
        print(f"Текст кнопки: {add_btn.text}")

        # ✅ Кликаем через JavaScript
        self.driver.execute_script("arguments[0].click();", add_btn)
        print("✅ Клик через JavaScript выполнен")

        # ✅ Ждём изменения текста (находим кнопку заново)
        self.wait.until(
            lambda d: "оформ" in d.find_element(*self.ADD_TO_CART_BTN).text.lower()
        )
        print("✅ Кнопка изменилась на 'ОФОРМИТЬ'")
        return True