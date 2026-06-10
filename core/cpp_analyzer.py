import subprocess
import tempfile
import os
import shutil

class CppAnalyzer:
    @staticmethod
    def analyze_cpp(code, timeout=10):
        if shutil.which("cppcheck") is None:
            return "cppcheck not found. Install it (for example: apt install cppcheck) or add it to PATH."

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False, encoding="utf-8") as temp_file:
                temp_file.write(code)
                tmp_path = temp_file.name

            result = subprocess.run(
                ["cppcheck", "--enable=all", tmp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout or result.stderr or ""
            if result.returncode == 0:
                return "C++ code analysis passed successfully!"
            return output or f"cppcheck returned code {result.returncode}"
        except subprocess.TimeoutExpired:
            return "C++ analysis timed out."
        except Exception as e:
            return f"Error running cppcheck: {e}"
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
