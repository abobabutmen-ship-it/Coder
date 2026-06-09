# Инструкции для работы с проектом Coder

Coder — это проект ИИ, предназначенный для анализа, исправления и улучшения программного кода.

## Как запустить проект

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/abobabutmen-ship-it/Coder.git
    ```
2. Установите зависимости (если потребуется):
    ```bash
    pip install -r requirements.txt
    ```
3. Запустите основной файл:
    ```bash
    python main.py
    ```

## Тесты

Тесты хранятся в директории `tests`. Для запуска выполните:
```bash
python -m unittest discover tests
```