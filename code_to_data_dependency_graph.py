import ast


def get_deps(code):
    body = ast.parse(code)
    _, statements = next(ast.iter_fields(body))

    # Line no. at which each identifier was first seen
    declaration_line_num_map = {}
    ddg = {}

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

    # full_graph = {
    #     assign.targets[0].id: [
    #         d.id for d in ast.walk(assign) if isinstance(d, ast.Name)
    #     ]
    #     for assign in statements
    # }
    # # full_graph also contains `range` and `i`. Keep only top levels var
    # restricted = {}
    # for var in full_graph:
    #     restricted[var] = [d for d in full_graph[var] if d in full_graph and d != var]
    # return restricted

    return declaration_line_num_map, ddg
