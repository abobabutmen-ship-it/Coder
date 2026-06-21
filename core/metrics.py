"""
core/metrics.py

Simple code metrics for Python (and fallbacks for other languages).
Provides: LOC (non-blank, non-comment), total_lines, functions, classes,
comment_ratio, avg_function_length.
"""
import ast
from typing import Dict


def analyze_python_metrics(code: str) -> Dict:
    lines = code.splitlines()
    total_lines = len(lines)
    non_blank = [l for l in lines if l.strip()]
    loc = len([l for l in non_blank if not l.strip().startswith('#')])
    comments = len([l for l in lines if l.strip().startswith('#')])

    try:
        tree = ast.parse(code)
    except Exception:
        return {
            "language": "py",
            "loc": loc,
            "total_lines": total_lines,
            "functions": 0,
            "classes": 0,
            "comment_ratio": round(comments / total_lines, 3) if total_lines else 0.0,
            "avg_function_length": 0.0,
        }

    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    func_lengths = []
    for f in funcs:
        try:
            start = f.lineno - 1
            # end_lineno available in Python 3.8+ for ast nodes
            end = getattr(f, 'end_lineno', None)
            if end:
                func_lines = lines[start:end]
            else:
                func_lines = lines[start: start + 1]
            func_lengths.append(len([l for l in func_lines if l.strip() and not l.strip().startswith('#')]))
        except Exception:
            continue

    avg_func_len = round(sum(func_lengths) / len(func_lengths), 2) if func_lengths else 0.0

    return {
        "language": "py",
        "loc": loc,
        "total_lines": total_lines,
        "functions": len(funcs),
        "classes": len(classes),
        "comment_ratio": round(comments / total_lines, 3) if total_lines else 0.0,
        "avg_function_length": avg_func_len,
    }


def analyze_code_metrics(lang: str, code: str) -> Dict:
    lang = lang.lower()
    if lang == 'py':
        return analyze_python_metrics(code)
    # Basic heuristics for other languages
    lines = code.splitlines()
    total_lines = len(lines)
    loc = len([l for l in lines if l.strip()])
    return {"language": lang, "loc": loc, "total_lines": total_lines}
