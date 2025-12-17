import time
import allure
import pytest
import os
from selenium.webdriver.common.by import By


@pytest.mark.android
@allure.id('1111')
@allure.title('Проверка шильдика 0-0-12 через диплинк')
def test_shelbik_full(product_screen, case_data, env):

    current_env = os.getenv('ENV', env.get('env', 'PROD'))
    item_ids = case_data['item_ids'][current_env]
    shelbik_data = case_data['shelbik_0_0_12']

    SHELBIK_TEXT = shelbik_data['shelbik_text']
    EXPECTED_TITLE = shelbik_data['expected_title']
    EXPECTED_DESCRIPTION = shelbik_data['expected_description']
    EXPECTED_PROMO_TITLE = shelbik_data['expected_promo_title']
    CLICKABLE_TEXT = shelbik_data['clickable_text']

    print(f"Тестируем в окружении: {current_env}")
    print(f"Артикулы для проверки: {item_ids}")

    # поиск товара с шильдиком
    suitable_item_id = None

    for item_id in item_ids:
        with allure.step(f"Поиск шильдика на товаре {item_id}"):
            try:
                print(f"\nПроверяем артикул: {item_id}")

                # Открыть диплинк
                product_screen.open_product_by_deeplink(str(item_id))
                time.sleep(3)

                # Открыть КТ
                product_screen.wait_for_product_page(timeout=10)

                # Проверка артикул
                opened_item_id = product_screen.get_item_id()
                print(f"Открыт товар с артикулом: {opened_item_id}")
                assert opened_item_id == str(item_id), \
                    f"Открылся товар с артикулом {opened_item_id}, а ожидался {item_id}"

                # Поиск шильдика
                shelbik = product_screen.find_shelbik_by_text(SHELBIK_TEXT)
                if shelbik:
                    print(f"Найден шильдик: {SHELBIK_TEXT}")
                    suitable_item_id = item_id
                    break
                else:
                    print(f"Шильдик не найден, взят следующий артикул")
                    allure.attach(
                        f"Товар {item_id} не содержит шильдик '{SHELBIK_TEXT}'",
                        attachment_type=allure.attachment_type.TEXT)

            except Exception:
                import traceback
                traceback.print_exc()
            finally:
                # закрытие кт если не нашлось
                if suitable_item_id is None:
                    try:
                        product_screen._driver.back()
                        time.sleep(2)
                    except:
                        pass

    # Если не нашли подходящий товар
    if not suitable_item_id:
        pytest.fail(f"Ни один из артикулов {item_ids} не содержит шильдик '{SHELBIK_TEXT}'. "
                   f"Возможно, тестовые данные устарели.")

    print(f"Основной тест на {suitable_item_id}")

    # ОСНОВНОЙ ТЕСТ
    with allure.step(f"Проверка шильдика 0-0-12 на товаре {suitable_item_id}"):
        # 1. Клик по шильдику
        with allure.step(f"1. Нажать на шильдик '{SHELBIK_TEXT}'"):
            product_screen.click_shelbik_by_text(SHELBIK_TEXT)
            print("Клик по шильдику выполнен")
            time.sleep(2)

        # 2. Проверка боттомщита
        with allure.step("2. Проверить, что открылся Bottom sheet"):
            bottom_sheet = product_screen.find_bottom_sheet()
            assert bottom_sheet is not None, "Bottom sheet не отображается после клика на шильдик"
            print("Bottom sheet открылся")

        # 3. Проверка заголовка
        with allure.step(f"3. Проверить заголовок в боттомшите: '{EXPECTED_TITLE}'"):
            title_element = product_screen.find_bottom_sheet_title_with_text(EXPECTED_TITLE)
            assert title_element is not None, \
                f"Заголовок bottom sheet не совпадает с ожидаемым. Ожидался текст: '{EXPECTED_TITLE}'"
            print(f"Заголовок '{EXPECTED_TITLE}' найден")

        # 4. Проверка описания
        with allure.step(f"4. Проверить, что описание содержит текст: '{EXPECTED_DESCRIPTION}'"):
            description_element = product_screen.find_bottom_sheet_description()
            assert description_element is not None, "Элемент описания не найден в bottom sheet"

            actual_text = description_element.text
            assert EXPECTED_DESCRIPTION in actual_text, \
                f"Не соответствует.\nОжидалось: '{EXPECTED_DESCRIPTION}'\nПолучено: '{actual_text}'"
            print(f"Описание содержит текст: '{EXPECTED_DESCRIPTION}'")

        # 5. Проверка кликабельности текста "Подробнее"
        with allure.step(f"5. Проверить что '{CLICKABLE_TEXT}' кликабелен"):
            details_element = product_screen.find_clickable_text(CLICKABLE_TEXT)
            assert details_element is not None, \
                f"Текст '{CLICKABLE_TEXT}' не найден"
            print(f"Текст '{CLICKABLE_TEXT}' найден и кликабелен")

        # 6. Проверка кнопки "Понятно"
        with allure.step("6. Проверить наличие красной кнопки 'Понятно'"):
            ok_button = product_screen.find_ok_button()
            assert ok_button is not None, "Кнопка 'Понятно' не найдена"
            print("Кнопка 'Понятно' найдена")

        # 7. Клик по "Подробнее"
        with allure.step(f"7. Нажать на '{CLICKABLE_TEXT}'"):
            product_screen.click_details_tap(CLICKABLE_TEXT)
            print(f"Клик по '{CLICKABLE_TEXT}' выполнен")
            time.sleep(3)

        # 8. Обработка SSL предупреждения
        with allure.step("8. Обработать SSL предупреждение, если появилось"):
            ssl_handled = product_screen.handle_ssl_warning()
            if ssl_handled:
                print("SSL предупреждение обработано")
            time.sleep(2)

        # 9. Проверка веб-вью
        with allure.step("9. Проверить открытие веб-вью"):
            webview = product_screen.find_webview()
            assert webview is not None, "Веб-вью не отображается после клика на 'Подробнее'"
            print("Веб-вью открылось")

        # 10. Проверка заголовка промо-акции в веб-вью
        with allure.step(f"10. Проверить заголовок промо-акции'{EXPECTED_PROMO_TITLE}'"):
            promo_title = product_screen.find_webview_promo_title(EXPECTED_PROMO_TITLE)
            assert promo_title is not None, (
                f"Заголовок промо-акции '{EXPECTED_PROMO_TITLE}' не найден в веб-вью")

            print(f"Заголовок промо-акции найден: '{promo_title.text}'")
            time.sleep(2)

        # 11. Возврат из веб-вью
        with allure.step("11. Вернуться из веб-вью"):
            product_screen.back_from_webview()
            print("Возврат из веб-вью выполнен")
            time.sleep(2)

        # 12. Проверка что боттомшит остался открытым
        with allure.step("12. Проверить что боттомшит открыт после возврата"):
            bottom_sheet_after_back = product_screen.find_bottom_sheet()
            assert bottom_sheet_after_back is not None, \
                "Bottom sheet не открыт после возврата из веб-вью"
            print("Bottom sheet открыт после возврата")
            time.sleep(2)

        # 13. Клик по кнопке "Понятно"
        with allure.step("13. Нажать на кнопку 'Понятно'"):
            product_screen.click_ok_button()
            print("Клик по кнопке 'Понятно' выполнен")

        # 14. Проверка закрытия боттомшита
        with allure.step("14. Проверить что боттомшит закрылся"):
            time.sleep(1)
            bottom_sheet_closed = product_screen.find_bottom_sheet() is None
            assert bottom_sheet_closed, "Bottom sheet не закрылся после нажатия 'Понятно'"
            print("Bottom sheet закрылся")


        print(f"Тест успешно завершен на {suitable_item_id}")


# Запуск теста:
# python -m pytest tests/tests/shelbik_test.py::test_shelbik_full -v -s --alluredir=./allure-results
