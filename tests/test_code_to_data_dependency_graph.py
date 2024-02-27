import unittest

from code_to_data_dependency_graph import MethodLevelDDGs, get_deps


class TestGetDepsFunction(unittest.TestCase):

    def test_simple_assignment(self):
        code = "x = 1"
        decl_map, ddg = get_deps(code)
        self.assertEqual(decl_map, {'x': 0})
        self.assertEqual(ddg, {'x': set()})

    def test_multiple_assignments_single_statement(self):
        code = "x, y = 1, 2"
        decl_map, ddg = get_deps(code)
        self.assertEqual(decl_map, {'x': 0, 'y': 0})
        self.assertEqual(ddg, {'x': set(), 'y': set()})

    def test_assignment_with_function_call(self):
        code = "def f(a): return a\nx = f(1)"
        decl_map, ddg = get_deps(code)
        self.assertEqual(decl_map, {'f': 0, 'x': 1})
        self.assertTrue('f' in ddg['x'])

class TestMethodLevelDDGs(unittest.TestCase):

    def test_simple_method_dependency(self):
        code = """
def a(x):
    return x

def b(y):
    return a(y)
"""
        ml_ddgs = MethodLevelDDGs(code)
        ddgs = ml_ddgs.fn_ddgs(code)
        self.assertTrue('a' in ddgs['b'])

    def test_nested_function_definitions(self):
        code = """
def outer(x):
    def inner(y):
        return y
    return inner(x)
"""
        ml_ddgs = MethodLevelDDGs(code)
        ddgs = ml_ddgs.fn_ddgs(code)
        self.assertTrue('inner' in ddgs['_global_'])
        self.assertTrue('x' in ddgs['outer'])

    def test_inter_method_dependencies(self):
        code = """
def first():
    return 42

def second():
    return first()
"""
        ml_ddgs = MethodLevelDDGs(code)
        ddgs = ml_ddgs.fn_ddgs(code)
        self.assertTrue('first' in ddgs['second'])

if __name__ == '__main__':
    unittest.main()
