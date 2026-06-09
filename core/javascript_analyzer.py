import subprocess

class JavaScriptAnalyzer:
    @staticmethod
    def analyze_js(code):
        with open("temp_code.js", "w") as temp_file:
            temp_file.write(code)
        result = subprocess.run(["eslint", "temp_code.js"], capture_output=True, text=True)
        if result.returncode == 0:
            return "JavaScript code analysis passed successfully!"
        return result.stdout