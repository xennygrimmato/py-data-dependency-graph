import code_to_data_dependency_graph as code2ddg


def test(path):
    code = open(path).read()
    print(code)
    decls, graph = code2ddg.get_deps(code)
    print("var: line_number map =>")
    print(decls)

    print("variable data dependence =>")
    print(graph)


def test_recursive(path):
    code = open(path).read()
    print(code)
    graphs = code2ddg.fn_ddgs(code)

    print("variable data dependence by method name =>")
    print(graphs)


if __name__ == '__main__':
    path = "snippets/sample_3.py"
    test_recursive(path)
