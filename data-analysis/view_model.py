import json

from pathlib import Path
from graphviz import Digraph
from model.treesplit import TreeSplit
from util.importance import get_data_provider, ImportanceCalculator


def parse_tree_node(graph, path, tree_node, calculator, previous_node=None, edge_type=None):
    is_root = is_root_node(previous_node, edge_type)
    if 'feature' in tree_node:
        feature = tree_node['feature']
        threshold = tree_node['threshold']
        split = TreeSplit(feature, threshold)
        node_path = path + '/' + str(split)
        gini = calculator.calculate_importance(split)
        node_label = str(split) + '\n' + 'GINI:' + '{0:.5f}'.format(gini)
        graph.node(node_path, node_label)
        if not is_root:
            graph.edge(previous_node, node_path, label=edge_type)
        parse_tree_node(graph, node_path, tree_node['left'], calculator ,node_path, 'left')
        parse_tree_node(graph, node_path, tree_node['right'], calculator, node_path, 'right')
    else:
        value = tree_node['value']
        node_path = path + '/' + 'value,' + value
        node_label = str(value)
        graph.node(node_path, node_label)
        if not is_root:
            graph.edge(previous_node, node_path, label=edge_type)


def is_root_node(previous_node, edge_type):
    return (previous_node is None) and (edge_type is None)


def get_tree_to_show(conf, ensemble):
    required_tree_num = int(conf['model']['view']['tree_num'])
    if required_tree_num > len(ensemble):
        raise ValueError("Tree to show number greater that ensemble contains.")
    return required_tree_num


if __name__ == '__main__':
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
        model_file_path = config['file']['ltr_model']
        with open(model_file_path) as model_file:
            model_file_name = Path(model_file_path).name
            ltr_model = json.load(model_file)
            trees_ensemble = ltr_model['params']['trees']
            tree_to_show = get_tree_to_show(config, ltr_model)
            for index, tree in enumerate(trees_ensemble):
                if index == tree_to_show:
                    tree_graph_name = model_file_name.replace('.json', '') + "_model_" + str(index)
                    g = Digraph(tree_graph_name, filename=tree_graph_name + '.gv')
                    g.attr('node', shape='box')
                    data_provider = get_data_provider(config)
                    calculator = ImportanceCalculator(data_provider)
                    parse_tree_node(g, 'root', tree['root'], calculator)
                    g.view()
