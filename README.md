Полная инструкция по установке окружения для Appium-тестирования
📋 Системные требования
 - macOS 12+ (для iOS и Android тестирования)
 - Python 3.8+
 - Права администратора для установки системных пакетов

🖥️ 1. СИСТЕМНЫЕ ЗАВИСИМОСТИ (устанавливаются глобально)

*** 1.1. Установка Homebrew (если не установлен) ***
Homebrew — пакетный менеджер для macOS

- - - - - Установка Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

- - - - - Добавление в PATH (для Apple Silicon)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc


*** 1.2. Установка Node.js и npm ***
Node.js необходим для работы Appium Server

- - - - - Установка Node.js через Homebrew
brew install node

- - - - - Проверка установки
node --version    # Должно быть v16+
npm --version     # Должно быть 8+


*** 1.3. Установка Java JDK ***
JDK необходим для работы с Android

- - - - - Установка OpenJDK (для Apple Silicon)
brew install --cask temurin

- - - - - Альтернативно можно установить через Homebrew
brew install openjdk

- - - - - Проверка установки
java --version
javac --version


*** 1.4. Установка Android SDK (без Android Studio) ***
Можно установить только командные инструменты Android

- - - - - Установка Android SDK Command Line Tools
brew install --cask android-sdk

- - - - - Настройка переменных окружения
echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.zshrc
source ~/.zshrc

- - - - - Установка необходимых Android пакетов
sdkmanager --install "platform-tools" "platforms;android-33" "build-tools;33.0.0"


*** 1.5. Установка Appium Server и драйверов ***

- - - - - Установка Appium Server глобально
npm install -g appium

- - - - - Установка Appium Doctor для проверки окружения
npm install -g appium-doctor

- - - - - Установка Android драйвера
npm install -g appium-uiautomator2-driver

- - - - - Установка iOS драйвера (только для macOS)
npm install -g appium-xcuitest-driver

- - - - - Проверка установки
appium --version


*** 1.6. Установка Appium Inspector ***
GUI-инструмент для поиска локаторов

- - - - - Через Homebrew (рекомендуется)
brew install --cask appium-inspector


*** 1.7. Установка Carthage (для iOS тестирования) ***
brew install carthage


*** 1.8. Проверка всей системы ***

- - - - - Запуск проверки окружения
appium-doctor --android
appium-doctor --ios
----------------------------------------------------------------------------------------------

🐍 2. ПРОЕКТНЫЕ ЗАВИСИМОСТИ (устанавливаются в виртуальном окружении)

*** 2.1. Создание и активация виртуального окружения ***
# Переход в папку проекта
cd ~/Documents/папка/корневая папка

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
# Для macOS/Linux:
source venv/bin/activate
# Для Windows:
venv\Scripts\activate

# Проверка активации (должна появиться приписка (venv))
which python
python --version

*** 2.2. Обновление pip ***
pip install --upgrade pip

*** 2.3. Установка базовых зависимостей проекта ***
Создать файл requirements.txt с содержимым:

# Основные библиотеки для тестирования
Appium-Python-Client==4.2.0
selenium==4.39.0
pytest==9.0.1
# Логирование и отчетность
loguru==0.7.2
allure-pytest==2.13.5
allure-python-commons==2.13.5
# Работа с конфигурацией
python-dotenv==1.2.1
PyYAML==6.0.2
# Вспомогательные библиотеки
requests==2.32.5
pytest-retry==1.6.3
webdriver-manager==4.0.2
typing_extensions==4.15.0
# Для статического анализа кода (опционально)
flake8==7.3.0
black==24.10.0

- - - - - Установить зависимости:
pip install -r requirements.txt

*** 2.4. Установка дополнительных зависимостей (при необходимости) ***
# Для работы с базами данных
pip install sqlalchemy pymysql psycopg2-binary

# Для работы с API
pip install httpx fastapi pydantic

# Для парсинга данных
pip install beautifulsoup4 lxml

*** 2.5. Генерация финального requirements.txt ***
pip freeze > requirements.txt


🔧 3. НАСТРОЙКА ПРОЕКТА

*** 3.1. Файл .env.example ***

# Appium Configuration
APPIUM_SERVER_URL=http://localhost:4723
APPIUM_SERVER_URL_ANDROID=http://localhost:4723
APPIUM_SERVER_URL_IOS=http://localhost:4724

# Android
ANDROID_AUTOMATION_NAME=UiAutomator2
ANDROID_PLATFORM_NAME=Android
ANDROID_PLATFORM_VERSION=13.0
ANDROID_DEVICE_NAME=Android_Emulator
ANDROID_APP=/path/to/app.apk
ANDROID_APP_PACKAGE=com.example.app
ANDROID_APP_ACTIVITY=.MainActivity

# iOS
IOS_AUTOMATION_NAME=XCUITest
IOS_PLATFORM_NAME=iOS
IOS_PLATFORM_VERSION=16.0
IOS_DEVICE_NAME=iPhone_15_Pro
IOS_APP=/path/to/app.app
IOS_BUNDLE_ID=com.example.app

