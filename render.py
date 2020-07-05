from sys import argv

from var_ddg import MyVisitor
from graphviz import Digraph


dot = Digraph(comment='DDG')


def get_ddg(path):
    obj = MyVisitor(path)
    obj.construct_ddg()
    graphs = obj.get_function_level_ddg()
    return graphs


def render_graph(edges, method_name):
    dot.edges(edges)
    dot.save('{0}.dot'.format(method_name))
    dot.render('{0}.gv'.format(method_name), view=True)


# e.g. "snippets/sample_3.py"
path = argv[1]
sample_3_graph = get_ddg(path)
for method_name in sample_3_graph:
    edges = list(sample_3_graph[method_name])
    render_graph(edges, method_name)
