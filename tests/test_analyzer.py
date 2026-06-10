from core.analyzer import CodeAnalyzer

def test_valid_python_code():
    assert CodeAnalyzer.analyze_code("a = 1\n") == []

def test_syntax_error_reported():
    res = CodeAnalyzer.analyze_code("def )")
    assert isinstance(res, list) and len(res) >= 1
