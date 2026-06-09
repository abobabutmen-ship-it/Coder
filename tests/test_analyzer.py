import unittest
from core.analyzer import CodeAnalyzer

class TestCodeAnalyzer(unittest.TestCase):
    def test_valid_code(self):
        code = "def add(a, b):\n    return a + b"
        self.assertEqual(CodeAnalyzer.analyze_code(code), [])

    def test_invalid_code(self):
        code = "def add(a, b)\n    return a + b"
        self.assertTrue(len(CodeAnalyzer.analyze_code(code)) > 0)

if __name__ == "__main__":
    unittest.main()