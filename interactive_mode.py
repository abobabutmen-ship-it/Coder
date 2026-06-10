from core.analyzer import CodeAnalyzer
from core.fixer import CodeFixer
from core.generator import CodeGenerator

def interactive_mode():
    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Проанализировать код")
        print("2. Исправить ошибки в коде")
        print("3. Генерация улучшения")
        print("4. Проверить стиль кода")
        print("0. Выйти")
        action = input("Выберите номер: ")

        if action == "0":
            print("До свидания!")
            break
        elif action == "1":
            code = input("Введите ваш код:\n")
            issues = CodeAnalyzer.analyze_code(code)
            print("Проблемы:", issues)
        elif action == "2":
            code = input("Введите ваш код:\n")
            issues = CodeAnalyzer.analyze_code(code)
            fixed_code = CodeFixer.fix_code(code, issues)
            print("Исправленный код:\n", fixed_code)
        elif action == "3":
            code = input("Введите ваш код:\n")
            improved_code = CodeGenerator.improve_code(code)
            print("Улучшенный код:\n", improved_code)
        elif action == "4":
            code = input("Введите ваш код:\n")
            style_feedback = CodeAnalyzer.analyze_code_style(code)
            print("Результат анализа стиля:\n", style_feedback)
        else:
            print("Выберите корректный пункт!")
