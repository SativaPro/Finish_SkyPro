import pytest
import allure
import os
from envyaml import EnvYAML
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

@pytest.fixture(scope="session")
def env():
    """Загружает общий конфиг из config.yaml"""
    config = EnvYAML("config.yaml", strict=False)
    return config

@pytest.fixture(scope="session")
def shelbik_config():
    """Загружает конфиг для теста шелбика"""
    return EnvYAML("tests/tests/config/config_shelbik.yaml", strict=False)

@pytest.fixture()
def case_data(shelbik_config):
    """Данные для тестов"""
    return shelbik_config.get("case_data")

@pytest.fixture(scope="function")
def app_driver(env):
    """Фикстура для создания драйвера Appium с новым API"""

    # Получаем конфигурацию для Android
    android_config = env['devices']['android'][0]
    app_config = env['applications']['android']
    server_config = env['server']

    # Формируем capabilities через UiAutomator2Options
    options = UiAutomator2Options()

    # Базовые настройки
    options.platform_name = 'Android'
    options.device_name = os.getenv('DEVICE_ANDROID_NAME', android_config['name'])
    options.platform_version = os.getenv('DEVICE_ANDROID_VERSION', android_config['platformVersion'])
    options.udid = os.getenv('DEVICE_ANDROID_ID', android_config['deviceId'])
    options.automation_name = 'UiAutomator2'
    options.no_reset = True  # Не сбрасывать состояние приложения
    options.auto_grant_permissions = True  # Автоматически выдавать разрешения

    # Настройки приложения
    options.app_package = os.getenv('APP_ANDROID_PACKAGE', app_config['appPackage'])
    options.app_activity = os.getenv('APP_ANDROID_ACTIVITY', app_config['appActivity'])

    # Добавляем путь к приложению, если он указан
    app_path = os.getenv('APP_ANDROID_PATH', app_config.get('appPath'))
    if app_path:
        options.app = app_path

    # Адрес сервера Appium
    appium_server_url = os.getenv('APPIUM_ADDRESS', server_config['address'])

    # Создаем драйвер с новым API
    driver = webdriver.Remote(
        command_executor=appium_server_url,
        options=options)

    driver.implicitly_wait(10)

    yield driver
    try:
        driver.quit()
    except Exception as e:
        print(f"Driver already closed: {e}")

@pytest.fixture(scope="function")
def product_screen(app_driver):
    """Фикстура для экрана продукта"""
    from tests.pages.product_kt import ProductScreen
    return ProductScreen(app_driver)
