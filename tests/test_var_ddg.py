import unittest
from io import StringIO
from unittest.mock import patch

from var_ddg import MyVisitor


class TestMyVisitor(unittest.TestCase):

    @patch("builtins.open", new_callable=lambda: lambda *args, **kwargs: StringIO("x = 1\ny = x + 2"))
    def test_simple_dependency(self, mock_open):
        visitor = MyVisitor("dummy_path")
        visitor.construct_ddg()
        ddg = visitor.get_function_level_ddg()
        self.assertIn('_global_', ddg)
        self.assertIn(('y', 'x'), ddg['_global_'])

    @patch("builtins.open", new_callable=lambda: lambda *args, **kwargs: StringIO("for i in range(5):\n    x = i"))
    def test_loop_dependency(self, mock_open):
        visitor = MyVisitor("dummy_path")
        visitor.construct_ddg()
        ddg = visitor.get_function_level_ddg()
        self.assertIn('_global_', ddg)
        self.assertIn(('x', 'i'), ddg['_global_'])

    @patch("builtins.open", new_callable=lambda: lambda *args, **kwargs: StringIO("if condition:\n    x = 42\nelse:\n    x = 0"))
    def test_conditional_dependency(self, mock_open):
        visitor = MyVisitor("dummy_path")
        visitor.construct_ddg()
        ddg = visitor.get_function_level_ddg()
        self.assertIn('_global_', ddg)
        self.assertIn(('x', 'condition'), ddg['_global_'])

    @patch("builtins.open", new_callable=lambda: lambda *args, **kwargs: StringIO("def foo():\n    x = 1\n    return x\ny = foo()"))
    def test_function_call_dependency(self, mock_open):
        visitor = MyVisitor("dummy_path")
        visitor.construct_ddg()
        ddg = visitor.get_function_level_ddg()
        self.assertIn('_global_', ddg)
        self.assertIn(('y', 'foo'), ddg['_global_'])

    @patch("builtins.open", new_callable=lambda: lambda *args, **kwargs: StringIO("x = 1\ny = x + 2\ndef foo():\n    z = y"))
    def test_construct_ddg(self, mock_open):
        visitor = MyVisitor("dummy_path")
        visitor.construct_ddg()
        ddg = visitor.get_function_level_ddg()
        self.assertIn('_global_', ddg)
        self.assertIn(('y', 'x'), ddg['_global_'])
        self.assertIn(('z', 'y'), ddg['foo'])

if __name__ == '__main__':
    unittest.main()
