import shutil
import subprocess
import tempfile
import os
from core.schema import format_result

class CppAnalyzer:
    @staticmethod
    def analyze_cpp(code, timeout=10):
        """
        Run cppcheck on a temporary file and return normalized result dict.
        """
        if shutil.which("cppcheck") is None:
            return {"success": False, "issues": [{"message": "cppcheck not found", "line": None, "rule": None}], "raw": None, "returncode": None, "language": "cpp"}
        tf = None
        try:
            tf = tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False, encoding="utf-8")
            tf.write(code)
            tf.flush()
            tf.close()
            # cppcheck writes diagnostics to stderr by default
            result = subprocess.run(["cppcheck", "--enable=all", tf.name], capture_output=True, text=True, timeout=timeout)
            return format_result(result.returncode, result.stdout, result.stderr, language="cpp")
        except subprocess.TimeoutExpired as e:
            return format_result(None, None, f"cppcheck timed out: {e}", language="cpp")
        except Exception as e:
            return format_result(None, None, str(e), language="cpp")
        finally:
            if tf is not None and os.path.exists(tf.name):
                try:
                    os.unlink(tf.name)
                except Exception:
                    pass
