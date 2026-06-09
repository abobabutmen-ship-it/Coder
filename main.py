from core.analyzer import CodeAnalyzer
from core.fixer import CodeFixer
from core.generator import CodeGenerator


def main():
    print("🛠 Добро пожаловать в Coder — ваш удобный ИИ для работы с кодом!")

    # Пример входных данных
    sample_code = '''
def add(a, b)
    return a + b
    '''

    print("⚙️ Анализируем код...")
    issues = CodeAnalyzer.analyze_code(sample_code)
    print("🚩 Найдены проблемы:", issues)

    print("🔧 Исправляем код...")
    fixed_code = CodeFixer.fix_code(sample_code, issues)
    print("✅ Исправленный код:\n", fixed_code)

    print("✨ Генерируем улучшения...")
    improved_code = CodeGenerator.improve_code(fixed_code)
    print("🚀 Улучшенный код:\n", improved_code)


if __name__ == "__main__":
    main()