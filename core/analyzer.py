import ast


class CodeAnalyzer:
    @staticmethod
    def analyze_code(code):
        try:
            ast.parse(code)
            return []
        except SyntaxError as e:
            return [str(e)]