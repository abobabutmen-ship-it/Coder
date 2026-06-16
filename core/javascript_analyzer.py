import shutil
import subprocess
import tempfile
import os
from core.schema import format_result

class JavaScriptAnalyzer:
    @staticmethod
    def analyze_js(code, timeout=10):
        """
        Run eslint on a temporary file and return normalized result dict.
        """
        if shutil.which("eslint") is None:
            return {"success": False, "issues": [{"message": "eslint not found", "line": None, "rule": None}], "raw": None, "returncode": None, "language": "js"}
        tf = None
        try:
            tf = tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8")
            tf.write(code)
            tf.flush()
            tf.close()
            # prefer JSON output if available
            # eslint --format json returns JSON array; we still capture stdout/stderr
            result = subprocess.run(["eslint", tf.name, "--no-color", "--format", "json"], capture_output=True, text=True, timeout=timeout)
            stdout = result.stdout
            stderr = result.stderr
            # try to parse JSON to extract messages
            issues = None
            try:
                import json
                parsed = json.loads(stdout) if stdout else None
                msgs = []
                if isinstance(parsed, list) and parsed:
                    for file_report in parsed:
                        for m in file_report.get("messages", []):
                            msgs.append({"message": m.get("message"), "line": m.get("line"), "rule": m.get("ruleId")})
                    # return structured result
                    return {"success": (result.returncode == 0), "issues": msgs, "raw": stdout + ("\nSTDERR:\n" + stderr if stderr else ""), "returncode": result.returncode, "language": "js"}
            except Exception:
                # fallback to normalized raw parsing
                pass
            return format_result(result.returncode, result.stdout, result.stderr, language="js")
        except subprocess.TimeoutExpired as e:
            return format_result(None, None, f"eslint timed out: {e}", language="js")
        except Exception as e:
            return format_result(None, None, str(e), language="js")
        finally:
            if tf is not None and os.path.exists(tf.name):
                try:
                    os.unlink(tf.name)
                except Exception:
                    pass
