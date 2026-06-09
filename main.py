from core.analyzer import CodeAnalyzer
from core.javascript_analyzer import JavaScriptAnalyzer
from core.cpp_analyzer import CppAnalyzer
from language_manager import LanguageManager

def main():
    lang = input("Choose language (en/ru): ").lower()
    lm = LanguageManager(lang)

    print(lm.translate("welcome"))

    code_type = input("Select code type (python/js/cpp): ").lower()

    if code_type == "python":
        code = input(lm.translate("analyze_prompt") + "\n")
        issues = CodeAnalyzer.analyze_code(code)
        if issues:
            print(lm.translate("error_found"), issues)
        else:
            print(lm.translate("no_errors"))

    elif code_type == "js":
        code = input("Enter JavaScript code:\n")
        result = JavaScriptAnalyzer.analyze_js(code)
        print(result)

    elif code_type == "cpp":
        code = input("Enter C++ code:\n")
        result = CppAnalyzer.analyze_cpp(code)
        print(result)

if __name__ == "__main__":
    main()