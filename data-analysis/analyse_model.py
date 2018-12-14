import abc
import json

import requests

from model.treesplit import TreeSplit, SplitStatistic


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


def get_data_provider(conf):
    provider_conf = conf['model']['data_provider']
    if provider_conf == 'solr':
        return SolrDataProvider(config)
    else:
        raise ValueError('Unsupported type of data provider', provider_conf)


class ImportanceCalculator:
    @staticmethod
    def calculate_gini_index(rank_aggr, total):
        gini_index = 1
        for aggr in rank_aggr.values():
            gini_index -= (aggr / total) ** 2
        return gini_index

    def __init__(self, data_provider) -> None:
        self.data_provider = data_provider
        self.total_products, rank_aggr = self.data_provider.tree_aggregation()
        self.tree_gini_index = ImportanceCalculator.calculate_gini_index(rank_aggr, self.total_products)
        print('Tree GINI importance: {0:.5f}'.format(self.tree_gini_index))

    def calculate_importance(self, split):
        print('Importance for split: {}'.format(str(split)))
        left_total, left_aggr, right_total, right_aggr = self.data_provider.split_aggregation(split)
        partition_left = left_total / self.total_products
        partition_right = right_total / self.total_products
        gini_left = ImportanceCalculator.calculate_gini_index(left_aggr, left_total)
        gini_right = ImportanceCalculator.calculate_gini_index(right_aggr, right_total)
        print('P_l:{0:.5f} | GINI_l:{1:.5f} | P_r:{2:.5f} | GINI_r:{3:.5f}'
              .format(partition_left, gini_left, partition_right, gini_right))
        return self.tree_gini_index - partition_left * gini_left - partition_right * gini_right


class DataProvider(abc.ABC):
    @abc.abstractmethod
    def tree_aggregation(self):
        pass

    @abc.abstractmethod
    def split_aggregation(self, split):
        pass


class SolrDataProvider(DataProvider):
    @staticmethod
    def get_solr_url(config):
        server = config['indexing']['server']
        core = config['indexing']['core_name']
        return 'http://' + server + '/solr/' + core + '/query'

    @staticmethod
    def get_buckets_dict(buckets):
        buckets_dict = {}
        for bucket in buckets:
            buckets_dict[bucket['val']] = bucket['count']
        return buckets_dict

    def __init__(self, config) -> None:
        self.solr_url = SolrDataProvider.get_solr_url(config)

    def search(self, params):
        response = requests.get(url=self.solr_url, params=params)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def tree_aggregation(self):
        params = {
            'q': '*:*',
            'rows': '0',
            'json.facet': '{ranks: {type: terms,field: rank,sort: {index: asc}}}'
        }
        rsp = self.search(params)
        num_found = rsp['response']['numFound']
        buckets_dict = SolrDataProvider.get_buckets_dict(rsp['facets']['ranks']['buckets'])
        return num_found, buckets_dict

    def split_aggregation(self, split):
        left_query = '{}_feature:[* TO {}]'.format(split.feature, split.threshold)
        right_query = '{}_feature:{{{} TO *]'.format(split.feature, split.threshold)
        json_facet = '{left_split:{type: query, q: \"' + left_query \
                     + '\", facet: {ranks: {type: terms, field: rank,sort: {index: asc} }}},' \
                     + 'right_split:{type: query,q: \"' + right_query \
                     + '\",facet: {ranks: {type: terms,field: rank,sort: {index: asc}}}}}'
        params = {
            'q': '*:*',
            'rows': '0',
            'json.facet': json_facet
        }
        rsp = self.search(params)
        left_total = rsp['facets']['left_split']['count']
        right_total = rsp['facets']['right_split']['count']
        left_dict = SolrDataProvider.get_buckets_dict(rsp['facets']['left_split']['ranks']['buckets'])
        right_dict = SolrDataProvider.get_buckets_dict(rsp['facets']['right_split']['ranks']['buckets'])
        return left_total, left_dict, right_total, right_dict


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
