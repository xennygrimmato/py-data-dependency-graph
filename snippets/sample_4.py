import ast


def get_deps(code):
    body = ast.parse(code)
    _, statements = next(ast.iter_fields(body))
