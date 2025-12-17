import json
import urllib.parse
import allure
import time
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .base_screen import Screen


class ProductScreen(Screen):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, "./tests/locators/locator_shelbik.json")

    @allure.step("Открыть диплинк на товар с артикулом {item_id}")
    def open_product_by_deeplink(self, item_id: str):
        data = json.dumps({"articul": item_id})
        encoded_data = urllib.parse.quote(data)
        deeplink = f"hoff://product?data={encoded_data}"

        self._driver.execute_script(
            "mobile: deepLink",
            {
                "url": deeplink,
                "package": "ru.hoff.app.beta.gms"
            }
        )
        time.sleep(5)

    @allure.step("Ожидание открытия карточки товара")
    def wait_for_product_page(self, timeout: int = 20):
        return self.element("productShareButton", timeout=timeout)

    @allure.step("Получить артикул открытого товара")
    def get_item_id(self, timeout: int = 10) -> str:
        element = self.element("productArticul")
        text = element.text
        articul = text.replace("Артикул:", "").strip()
        allure.attach(
            f"Найден артикул: {articul}",
            name="Артикул товара",
            attachment_type=allure.attachment_type.TEXT)
        return articul

    @allure.step("Найти шильдик с текстом '{shelbik_text}'")
    def find_shelbik_by_text(self, shelbik_text, timeout: int = 5):
        # сначала через локатор
        try:
            element = self.soft_element("shelbikView", timeout=timeout,
                                      loc_kwargs={"shelbikText": shelbik_text})
            if element:
                print(f"Шильдик найден через локатор: {element.text}")
                return element
        except Exception as e:
            print(f"Ошибка при поиске через локатор: {e}")

        # поиск как fallback
        try:
            elements = self._driver.find_elements(By.XPATH, f"//*[@text='{shelbik_text}']")
            if elements:
                print(f"Найдено {len(elements)} элементов с текстом '{shelbik_text}'")
                return elements[0]
        except Exception as e:
            print(f"Ошибка при прямом поиске: {e}")
        return None

    @allure.step("Кликнуть на шильдик с текстом '{shelbik_text}'")
    def click_shelbik_by_text(self, shelbik_text):

        # проверка, что видим шильдик
        shelbik_element = self.find_shelbik_by_text(shelbik_text)
        if not shelbik_element:
            raise Exception(f"Шильдик с текстом '{shelbik_text}' не найден")
        print(f"Шильдик найден, ищу родительский контейнер для клика")

        # попытка кликнуть на родительский контейнер
        try:
            container = self.element("shelbikClick", timeout=5,
                                    loc_kwargs={"shelbikText": shelbik_text})
            if container:
                print(f"Контейнер кликабелен: {container.get_attribute('clickable')}")
                container.click()
                print("Клик по контейнеру выполнен")
                return
        except Exception as e:
            print(f"Не удалось кликнуть через контейнер: {e}")

        # Fallback: клик на сам элемент шильдика
        shelbik_element.click()
        print("Клик по элементу выполнен")

    @allure.step("Найти bottom sheet")
    def find_bottom_sheet(self, timeout: int = 5):
        return self.soft_element("bottomSheetVisible", timeout=timeout)

    @allure.step("Найти заголовок bottom sheet:'{expected_title}'")
    def find_bottom_sheet_title_with_text(self, expected_title, timeout: int = 5):

        try:
            # поиск заголовка
            element = self.soft_element("bottomSheetTitleExact", timeout=timeout)
            if element:
                print(f"Найден элемент заголовка: текст='{element.text}'")
                # проверка на соответствие ОР
                if expected_title in element.text:
                    print(f"Заголовок содержит '{expected_title}'")
                    return element
                else:
                    print(f"Заголовок не содержит '{expected_title}'. ФР: '{element.text}'")
            return None
        except Exception as e:
            print(f"Ошибка при поиске заголовка: {e}")
            return None

    @allure.step("Найти описание в bottom sheet")
    def find_bottom_sheet_description(self):
        return self.soft_element("bottomSheetDescription")

    @allure.step("Найти кликабельный текст '{clickable_text}' в bottom sheet")
    def find_clickable_text(self, clickable_text):

        # Поиск клик-текста ("Подробнее")
        element = self.soft_element("bottomSheetDescription", timeout=5)
        if element and clickable_text in element.text:
            print(f"Элемент с текстом '{clickable_text}' найден - кликабелен: {element.get_attribute('clickable')}")
            return element
        print(f"Элемент с текстом '{clickable_text}' не найден")
        return None

    @allure.step("Кликнуть на текст '{clickable_text}' (тап по координатам)")
    def click_details_tap(self, clickable_text):
        # поиск элемента с описанием
        element = self.element("bottomSheetDescription", timeout=5)

        location = element.location
        size = element.size
        # Вычисление координат (текст "Подробнее")
        x = location['x'] + size['width'] * 0.1  # левая часть
        y = location['y'] + size['height'] * 0.9  # нижняя часть

        print(f"Координаты клика по '{clickable_text}': x={x}, y={y}")
        print(f"Размер элемента: width={size['width']}, height={size['height']}")

        # Клик по координатам
        self._driver.tap([(x, y)])
        print(f"Тап по координатам выполнен")
        return element

    @allure.step("Найти кнопку 'Понятно'")
    def find_ok_button(self, timeout: int = 5):
        element = self.soft_element("bottomSheetOkButton", timeout=timeout)
        if element:
            print(f"Кнопка 'Понятно' найдена. Текст: '{element.text}', Кликабельна: {element.get_attribute('clickable')}")
        else:
            print("Кнопка 'Понятно' не найдена!")
        return element

    @allure.step("Кликнуть на кнопку 'Понятно'")
    def click_ok_button(self):
        element = self.element("bottomSheetOkButton")
        element.click()
        print("Клик по кнопке 'Понятно' выполнен")

    @allure.step("Найти веб-вью")
    def find_webview(self, timeout: int = 15):

        print(f"Ожидание веб-вью (main-header)... (таймаут: {timeout} сек)")
    
        element = self.soft_element("webViewContainer", timeout=timeout)
        if element:
            print(f"Веб-вью найдено")
            return element
        else:
            print(f"Веб-вью не найдено за {timeout} секунд")
            return None

    @allure.step("Найти заголовок промо-акции в веб-вью")
    def find_webview_promo_title(self, expected_promo_title, timeout: int = 10):

        element = self.soft_element(
            "webViewPromoTitle",
            timeout=timeout,
            loc_kwargs={"expectedPromoTitle": expected_promo_title})

        if element:
            print(f"Найден заголовок промо-акции: '{element.text}'")
            return element
        print(f"Заголовок промо-акции '{expected_promo_title}' не найден")
        return None

    @allure.step("Вернуться из веб-вью")
    def back_from_webview(self):
        back_button = self.soft_element("webViewBackButton", timeout=5)
        if back_button:
            back_button.click()
        else:
            self._driver.back()

        # ожидание закрытия веб-вью
        try:
            WebDriverWait(self._driver, 5).until(
                lambda d: self.find_webview(timeout=1) is None)
        except:
            pass  # Игнорируем таймаут, если веб-вью уже закрылось
        return back_button

    @allure.step("Обработать SSL предупреждение, если появилось")
    def handle_ssl_warning(self, timeout: int = 15):

        print(f"Проверка SSL предупреждения (таймаут: {timeout} сек)...")
    
        # soft_element для ожидания SSL диалога
        ssl_dialog = self.soft_element("sslDialog", timeout=timeout)
        if ssl_dialog:
            print(f"SSL диалог найден: {ssl_dialog.text}")
            try:
                # поиск кнопки "продолжить"
                continue_button = self.element("sslContinueButton", timeout=5)
                continue_button.click()
                time.sleep(1)  # время на закрытие диалога
                print("SSL предупреждение обработано")
                return True
            except Exception as e:
                print(f"Не удалось найти или нажать кнопку 'ПРОДОЛЖИТЬ': {e}")
                return False
        else:
            print(f"SSL диалог не появился за {timeout} секунд (это нормально)")
            return False

    