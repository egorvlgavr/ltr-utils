import json

from model.treesplit import TreeSplit, SplitStatistic
from util.importance import get_data_provider, ImportanceCalculator


def get_unique_model_splits(model):
    model_class = model['class']
    if model_class != 'org.apache.solr.ltr.model.MultipleAdditiveTreesModel':
        raise ValueError('Unsupported type of model', model_class)
    print('Start model traversing')
    splits_dict = {}
    for index, tree in enumerate(model['params']['trees']):
        parse_tree_node(splits_dict, tree['root'], index)
    print('Model traversing finished. Total splits:{}'.format(len(splits_dict)))
    return splits_dict


def parse_tree_node(aggregator, tree_node, tree_num):
    if 'feature' in tree_node:
        feature = tree_node['feature']
        threshold = tree_node['threshold']
        split = TreeSplit(feature, threshold)
        if split in aggregator:
            aggregator[split].count_usage(tree_num)
        else:
            statistic = SplitStatistic()
            statistic.count_usage(tree_num)
            aggregator[split] = statistic
        parse_tree_node(aggregator, tree_node['left'], tree_num)
        parse_tree_node(aggregator, tree_node['right'], tree_num)


def add_importance_to_statistic(splits_dict, conf):
    data_provider = get_data_provider(conf)
    calculator = ImportanceCalculator(data_provider)
    for split in splits_dict.keys():
        split_gini_index = calculator.calculate_importance(split)
        splits_dict[split].set_gini_index(split_gini_index)


def print_report(config, model, splits_dict):
    with open(config['model']['report_file'], 'w') as report_file:
        print_head(report_file, model, config, splits_dict)
        for split in sorted(splits_dict):
            report_file.write(str(split) + ',' + splits_dict[split].to_row() + '\n')


def print_head(report_file, model, config, splits_dict):
    report_file.write('# Model: {}'.format(model['name']) + '\n')
    report_file.write('# Model path: {}'.format(config['file']['ltr_model']) + '\n')
    report_file.write('# Model trees: {}'.format(len(model['params']['trees'])) + '\n')
    unique_features = set(split.feature for split in splits_dict.keys())
    report_file.write('# All used features: {}'.format(unique_features) + '\n')
    report_file.write('Feature,Threshold,Used in models,Num of usage,Split gini index' + '\n')


if __name__ == '__main__':
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
        model_file_path = config['file']['ltr_model']
        with open(model_file_path) as model_file:
            ltr_model = json.load(model_file)
            splits = get_unique_model_splits(ltr_model)
            add_importance_to_statistic(splits, config)
            print_report(config, ltr_model, splits)
