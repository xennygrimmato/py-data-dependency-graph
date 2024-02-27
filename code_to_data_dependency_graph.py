import ast


def get_deps(code: str) -> Tuple[Dict[str, int], Dict[str, Set[str]]]:
    body = ast.parse(code)
    _, statements = next(ast.iter_fields(body))

    # Line no. at which each identifier was first seen
    declaration_line_num_map: Dict[str, int] = {}
    ddg: Dict[str, Set[str]] = {}

    def update_decls(lhs_vars_input, num):
        lhs_var_nodes = []
        for var_node in lhs_vars_input:
            lhs_var_nodes.append(var_node)
            if var_node.id not in declaration_line_num_map:
                declaration_line_num_map[var_node.id] = num
                ddg[var_node.id] = set()
        return lhs_var_nodes

    # x1, x2, x3, ..., xN = 1, 2, 3, 4, 5, ..., N
    # is represented in the AST as:
    #   - R = ast.Assign is root
    #   - R.targets gives the LHS
    #   - R.values

    for seq_no, node in enumerate(statements):
        if isinstance(node, ast.Assign):
            identifier_names = node.targets
            lhs_vars = update_decls(identifier_names, seq_no)

            self_edge_occurrences_to_ignore = {x: 1 for x in identifier_names}

            # DFS in RHS
            depends_on = []
            for descendant in ast.walk(node):
                if descendant in self_edge_occurrences_to_ignore and self_edge_occurrences_to_ignore[descendant] > 0:
                    self_edge_occurrences_to_ignore[descendant] -= 1
                    continue
                if isinstance(descendant, ast.Name):
                    depends_on.append(descendant)

            for var in lhs_vars:
                for dependency in depends_on:
                    ddg[var.id].add(dependency.id)

    return declaration_line_num_map, ddg


class MethodLevelDDGs:
    def __init__(self, code):
        self.parsed_ast = ast.parse(code)

    def get_methods(self):
        fn_nodes = []

        class FnVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                fn_nodes.append(node)

        visitor = FnVisitor()
        visitor.visit(self.parsed_ast)
        return fn_nodes

    def recursive_ddg(self, fn_root_node):
        ddg = {}
        self_edge_set = set()

        class DDGVisitor(ast.NodeVisitor):
            def visit_Assign(self, node):
                identifiers = node.targets
                for identifier in identifiers:
                    ddg[identifier.id] = set()
                    self_edge_set.add(identifier.id)

                depends_on = []
                for descendant in ast.walk(node):
                    if isinstance(descendant, ast.Name):
                        depends_on.append(descendant)

                for var in identifiers:
                    for dependency in depends_on:
                        if var.id in self_edge_set:
                            self_edge_set.remove(var.id)
                            continue
                        ddg[var.id].add(dependency.id)

        visitor = DDGVisitor()
        visitor.visit(fn_root_node)
        return ddg


def fn_ddgs(code):
    method_level_ddgs = MethodLevelDDGs(code)
    methods = method_level_ddgs.get_methods()
    ddgs = {method.name: method_level_ddgs.recursive_ddg(method) for method in methods}
    return ddgs
