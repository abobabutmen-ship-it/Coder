import subprocess

class CodeAnalyzer:
    @staticmethod
    def analyze_code_style(code):
        with open("temp_code.py", "w") as temp_file:
            temp_file.write(code)
        result = subprocess.run(["flake8", "temp_code.py"], capture_output=True, text=True)
        return result.stdout if result.returncode != 0 else "Код соответствует стилю!"