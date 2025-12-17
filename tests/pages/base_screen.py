import json
import allure
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Screen:
    def __init__(self, driver: WebDriver, locators_path: str = None):
        self._driver = driver
        self.locators = {}
        if locators_path:
            self._load_locators(locators_path)

    def _load_locators(self, path: str):
        """Загружает локаторы из JSON файла"""
        with open(path, 'r', encoding='utf-8') as f:
            self.locators = json.load(f)

    def _parse_locator(self, locator_name: str, **kwargs) -> tuple:
        """Парсит локатор из JSON в формат (By, locator)"""
        locator_template = self.locators[locator_name]

        # Заменяем плейсхолдеры
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            locator_template = locator_template.replace(placeholder, str(value))

        # Разбираем тип локатора и значение
        if locator_template.startswith("xpath:: "):
            return (By.XPATH, locator_template[8:])
        elif locator_template.startswith("id:: "):
            return (By.ID, locator_template[5:])
        else:
            raise ValueError(f"Неизвестный формат локатора: {locator_template}")

    def element(self, locator_name: str, timeout: int = 10, **kwargs) -> WebElement:
        """Находит элемент с ожиданием"""
        by, locator = self._parse_locator(locator_name, **kwargs)
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(EC.presence_of_element_located((by, locator)))

    def soft_element(self, locator_name: str, timeout: int = 3, **kwargs):
        """Находит элемент без падения теста если не найден"""
        try:
            return self.element(locator_name, timeout, **kwargs)
        except:
            return None

    def click(self, locator_name: str, **kwargs):
        """Кликает по элементу"""
        element = self.element(locator_name, **kwargs)
        element.click()
        return element

    def error_report(self, message: str):
        """Логирует ошибку"""
        print(f"ERROR: {message}")
        allure.attach(message, name="Error", attachment_type=allure.attachment_type.TEXT)
