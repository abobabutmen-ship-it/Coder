def format_result(returncode, stdout, stderr, language=None):
    """Normalize analyzer output into standard schema.

    Returns:
      {"success": bool,
       "issues": [ {"message": str, "line": int|None, "rule": str|None} , ...],
       "raw": str|None,
       "returncode": int|None,
       "language": str|None }
    """
    raw_parts = []
    if stdout:
        raw_parts.append(stdout)
    if stderr:
        raw_parts.append(stderr)
    raw = "\n".join(raw_parts) if raw_parts else None

    issues = []
    if raw:
        for line in raw.splitlines():
            s = line.strip()
            if not s:
                continue
            # best-effort parsing: attempt to extract "file:line: msg" or plain msg
            parts = s.split(":", 2)
            if len(parts) == 3:
                # file:line: message
                _, ln, msg = parts
                try:
                    ln_i = int(ln)
                except Exception:
                    ln_i = None
                issues.append({"message": msg.strip(), "line": ln_i, "rule": None})
            else:
                issues.append({"message": s, "line": None, "rule": None})

    success = (returncode == 0) if returncode is not None else (len(issues) == 0)

    return {"success": success, "issues": issues, "raw": raw, "returncode": returncode, "language": language}
