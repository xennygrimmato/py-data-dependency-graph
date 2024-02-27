import ast


class MyVisitor:
    def __init__(self, path: str):
        self.GLOBAL_FN = ast.FunctionDef(name='_global_')

        # FunctionDef -> set(x, y) such that x reads y
        self.fn_to_ddg_map = {self.GLOBAL_FN: set()}
        self.fn_to_self_edge_set_map = {self.GLOBAL_FN: set()}
        self.fn_stack = [self.GLOBAL_FN]
        self.visited = set()

        code = open(path).read()
        self.tree = ast.parse(code)

    def ast_visit(self, node, level=0):
        if node in self.visited:
            return
        self.visited.add(node)

        is_fn = False
        if isinstance(node, ast.FunctionDef):
            is_fn = True
            self.fn_stack.append(node)
            self.fn_to_ddg_map[node] = set()
            self.fn_to_self_edge_set_map[node] = set()

        if isinstance(node, ast.Assign):
            lhs_ids = []
            current_fn = self.fn_stack[-1]
            depends_on = []
            for identifier in node.targets:
                if isinstance(identifier, ast.Attribute):
                    lhs_ids.append(identifier.value)
                    self.fn_to_self_edge_set_map[current_fn].add(identifier.value.id)
                elif isinstance(identifier, ast.Subscript):
                    lhs_ids.append(identifier.value)
                    self.fn_to_self_edge_set_map[current_fn].add(identifier.value.id)
                elif isinstance(identifier, ast.Tuple):
                    for elt in identifier.elts:
                        lhs_ids.append(elt)
                        self.fn_to_self_edge_set_map[current_fn].add(elt.id)
                else:
                    lhs_ids.append(identifier)
                    self.fn_to_self_edge_set_map[current_fn].add(identifier.id)

            # This ast.walk() call in the loop causes the complexity to be O(n^2)
            for descendant in ast.walk(node.value):
                if isinstance(descendant, ast.Name):
                    depends_on.append(descendant)
            for var in lhs_ids:
                for dependency in depends_on:
                    if dependency.id in self.fn_to_self_edge_set_map[current_fn]:
                        self.fn_to_self_edge_set_map[current_fn].remove(dependency.id)
                        continue
                    self.fn_to_ddg_map[current_fn].add((var.id, dependency.id))

        # TODO(xennygrimmato): Add visited check for node
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.ast_visit(item, level=level+1)
            elif isinstance(value, ast.AST):
                self.ast_visit(value, level=level+1)
        if is_fn:
            self.fn_stack.pop()

    def construct_ddg(self) -> None:
        self.ast_visit(self.tree)

    def get_function_level_ddg(self):
        return {fn.name: value for fn, value in self.fn_to_ddg_map.items()}
    def get_function_level_ddg(self) -> Dict[ast.FunctionDef, Set[Tuple[str, str]]]:
        return {fn.name: value for fn, value in self.fn_to_ddg_map.items()}
