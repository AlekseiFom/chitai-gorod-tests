# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.keys import Keys

from config.settings import settings


class MainChitaiGorodPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(settings.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @allure.step("Закрыть окно выбора города")
    def close_city_banner_if_present(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".chg-app-button--breeze.chg-app-button--block")
            ))
            btn.click()
            print("✅ Окно города закрыто")
        except Exception:
            print("ℹ️ Окно города не появилось")

    @allure.step("Выполнить поиск товара по запросу '{query}'")
    def search_for_item(self, query):
        search_field = self.wait.until(EC.element_to_be_clickable((By.ID, "app-search")))
        search_field.click()
        search_field.clear()
        search_field.send_keys(query)
        search_field.send_keys(Keys.ENTER)
        print(f"✅ Поиск '{query}' отправлен")