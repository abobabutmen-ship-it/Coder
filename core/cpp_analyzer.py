import subprocess

class CppAnalyzer:
    @staticmethod
    def analyze_cpp(code):
        with open("temp_code.cpp", "w") as temp_file:
            temp_file.write(code)
        result = subprocess.run(["cppcheck", "temp_code.cpp"], capture_output=True, text=True)
        if result.returncode == 0:
            return "C++ code analysis passed successfully!"
        return result.stdout