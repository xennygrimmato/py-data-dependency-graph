import code_to_data_dependency_graph as code2ddg


def test(path):
    code = open(path).read()
    print(code)
    decls, graph = code2ddg.get_deps(code)
    print("var: line_number map =>")
    print(decls)

    print("variable data dependence =>")
    print(graph)


if __name__ == '__main__':
    test("snippets/sample_2.py")
