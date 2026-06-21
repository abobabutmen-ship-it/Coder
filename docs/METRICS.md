# Metrics documentation

This document describes the simple metrics and security scanning features added in the
feat/metrics-and-analysis branch.

Commands
--------

- python -m core.cli metrics metrics --lang py --code "def f():\n  pass"
  - Runs lightweight metrics on provided code.

- python -m core.cli metrics scan --code "def f():\n  pass"
  - Runs a security scan (bandit) if bandit is installed; otherwise returns a helpful message.

Metrics computed (Python):
- loc: non-blank non-comment lines
- total_lines: total lines
- functions: number of function definitions
- classes: number of class definitions
- comment_ratio: fraction of lines that are comments
- avg_function_length: average function length in non-blank lines

Security scan:
- Wrapper around the bandit CLI (if available). Output normalized to the project's schema.

Adding more metrics
-------------------
- You can extend core/metrics.py with additional analyzers (cyclomatic complexity, duplication,
  Halstead metrics) using tools like radon or custom AST walks.

