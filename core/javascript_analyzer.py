import subprocess
import tempfile
import os
import shutil

class JavaScriptAnalyzer:
    @staticmethod
    def analyze_js(code, timeout=10):
        if shutil.which("eslint") is None:
            return "eslint not found. Install with `npm install -g eslint` or add it to PATH."

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as temp_file:
                temp_file.write(code)
                tmp_path = temp_file.name

            result = subprocess.run(
                ["eslint", tmp_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += ("\n" + result.stderr) if output else result.stderr

            if result.returncode == 0:
                return "JavaScript code analysis passed successfully!"
            return output or f"eslint returned code {result.returncode}"
        except subprocess.TimeoutExpired:
            return "JavaScript analysis timed out."
        except Exception as e:
            return f"Error running eslint: {e}"
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
