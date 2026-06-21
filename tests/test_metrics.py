from core.metrics import analyze_python_metrics


def test_simple_metrics():
    code = '''
# module comment

def a():
    # do one
    x = 1
    return x

class C:
    pass
'''
    res = analyze_python_metrics(code)
    assert res['functions'] == 1
    assert res['classes'] == 1
    assert res['total_lines'] > 0
