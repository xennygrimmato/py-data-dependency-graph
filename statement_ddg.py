from astor import tree_walk, code_to_ast


class AssignWalker(tree_walk.TreeWalk):
    def __init__(self):
        tree_walk.TreeWalk.__init__(self)
        self.fn_stack = []

    def pre_Assign(self):
        print("Assign", self.cur_node.__dict__)

    def pre_FunctionDef(self):
        self.fn_stack.append(self.cur_node)
        print("After pushing ...", self.fn_stack)

    def post_FunctionDef(self):
        self.fn_stack.pop()
        print("After popping ...", self.fn_stack)


ast = code_to_ast.parse_file("snippets/sample_3.py")
obj = AssignWalker()
obj.walk(ast)
