# utils/helpers.py
import allure


@allure.step("Авторизовать пользователя через инъекцию токена")
def authorize_user_via_token(driver, base_url, token):
    """Открывает сайт и подкладывает рабочий Bearer-токен напрямую в браузер"""
    # Включаем быстрое неявное ожидание элементов на 5 секунд
    driver.implicitly_wait(5)
    
    driver.get(base_url)
    
    # Внедряем JWT-токен в LocalStorage
    script = f"localStorage.setItem('token', '{token}');"
    driver.execute_script(script)
    
    # Перезагружаем страницу, чтобы сайт подтянул внедренный токен
    driver.refresh()

