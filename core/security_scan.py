"""
core/security_scan.py

Wrapper for running Bandit (Python SAST) if available. Returns normalized result
similar to the project's schema: { success, issues, raw, returncode, language }
"""
import shutil
import subprocess
import tempfile
import os
import json
from core.schema import format_result


def scan_python_with_bandit(code: str, timeout: int = 10):
    if shutil.which("bandit") is None:
        return {"success": False, "issues": [{"message": "bandit not installed", "line": None, "rule": None}], "raw": None, "returncode": None, "language": "py"}
    tf = None
    try:
        tf = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8")
        tf.write(code)
        tf.flush()
        tf.close()
        # bandit -f json -r <file> will produce JSON output
        result = subprocess.run(["bandit", "-f", "json", "-r", tf.name], capture_output=True, text=True, timeout=timeout)
        stdout = result.stdout
        stderr = result.stderr
        issues = []
        try:
            parsed = json.loads(stdout) if stdout else None
            if isinstance(parsed, dict):
                for item in parsed.get("results", []):
                    issues.append({
                        "message": item.get("issue_text"),
                        "line": item.get("line_number"),
                        "rule": item.get("test_id"),
                    })
                return {"success": (result.returncode == 0), "issues": issues, "raw": stdout + ("\nSTDERR:\n" + stderr if stderr else ""), "returncode": result.returncode, "language": "py"}
        except Exception:
            pass
        return format_result(result.returncode, result.stdout, result.stderr, language="py")
    except subprocess.TimeoutExpired as e:
        return format_result(None, None, f"bandit timed out: {e}", language="py")
    except Exception as e:
        return format_result(None, None, str(e), language="py")
    finally:
        if tf is not None and os.path.exists(tf.name):
            try:
                os.unlink(tf.name)
            except Exception:
                pass
