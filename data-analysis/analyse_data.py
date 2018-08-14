import argparse
import json
from enum import Enum
import matplotlib.pyplot as plt
from model import clickstream, trainingset
from mpl_toolkits.mplot3d import Axes3D


def show_click_stream_histogram(path, config):
    min_impression = config['filters']['min_impression']
    column_name = config['histogram']['column']
    with open(path) as fp:
        header = next(fp)  # get header
        grouped = {}
        for line in fp:
            row = clickstream.ClickStreamRow(line, header)
            if row.impr > min_impression:
                if row.phrase in grouped:
                    grouped_value = grouped[row.phrase]
                    grouped_value[0] += 1
                    grouped_value[1].append(int(row.get(column_name)))
                else:
                    grouped[row.phrase] = [1, [int(row.get(column_name))]]
        min_count = config['filters']['min_products_per_query']
        col_values = []
        for key, value in grouped.items():
            if value[0] > min_count:
                col_values.extend(value[1])
        plot_hist(col_values, config, column_name)


def plot_hist(values, config, name):
    plt.figure()
    bins = config['histogram']['num_of_bins']
    plt.title('Histogram of ' + name)
    plt.hist(values, bins, facecolor='green', alpha=0.75)
    plt.show()


def show_training_set_histogram(path, config):
    column_name = config['histogram']['column']
    with open(path) as fp:
        hist_values = []
        header = trainingset.normalize_header(next(fp))  # get header
        for line in fp:
            row = trainingset.TrainingSetRow(trainingset.normalize_line(line), header)
            hist_values.append(float(row.get(column_name)))
        plot_hist(hist_values, config, column_name)


def show_statistics(path):
    with open(path) as fp:
        header = next(fp)  # get header
        grouped = {}
        cnt = 0
        zero_clicks = 0
        for line in fp:
            row = clickstream.ClickStreamRow(line, header)
            if row.phrase in grouped:
                grouped[row.phrase] += 1
            else:
                grouped[row.phrase] = 1
            if row.clicks == 0:
                zero_clicks += 1
            cnt += 1
        print('Total (query, product) pairs={}'.format(cnt))
        unique_phrases = len(grouped)
        print('Unique queries={}'.format(unique_phrases))
        phrases_list = grouped.values()
        avg_products_per_query = sum(phrases_list) / float(unique_phrases)
        print('Average products per query={}'.format(avg_products_per_query))
        print('Max products per query={}'.format(max(phrases_list)))
        print('Min products per query={}'.format(min(phrases_list)))
        print('Number of products with zero clicks={}'.format(zero_clicks))


def create_queries_file(path, config):
    min_impression = config['filters']['min_impression']
    with open(path) as fp:
        header = next(fp)  # get header
        grouped = {}
        filtered_by_min_impression = 0
        for line in fp:
            row = clickstream.ClickStreamRow(line, header)
            if row.impr > min_impression:
                if row.phrase in grouped:
                    grouped[row.phrase] += 1
                    filtered_by_min_impression += 1
                else:
                    grouped[row.phrase] = 1
        min_count = config['filters']['min_products_per_query']
        print('Total pairs after min impression filter={}'.format(filtered_by_min_impression))
        print('Total queries after min impression filter={}'.format(len(grouped)))
        with open(config['queries']['file'], 'w') as phrases_file:
            cnt = 0
            for key, value in grouped.items():
                if value > min_count:
                    line = key
                    if config['queries']['add_count']:
                        line = line + "," + value
                    phrases_file.write(line + "\n")
                    cnt += 1
            print('Total queries after min product filter={}'.format(cnt))


def show_scatter_2d_plot(path, config):
    with open(path) as fp:
        header = trainingset.normalize_header(next(fp))
        x_key = config['scatter']['x_axis']
        y_key = config['scatter']['y_axis']
        y_data = []
        x_data = []
        for line in fp:
            row = trainingset.TrainingSetRow(trainingset.normalize_line(line), header)
            x_data.append(float(row.get(x_key)))
            y_data.append(float(row.get(y_key)))
        plt.plot(x_data, y_data, '.', label='observation')
        plt.xlabel(x_key)
        plt.ylabel(y_key)
        plt.legend()
        plt.show()


def show_scatter_3d_plot(path, config):
    with open(path) as fp:
        header = trainingset.normalize_header(next(fp))
        x_key = config['scatter']['x_axis']
        y_key = config['scatter']['y_axis']
        z_key = config['scatter']['z_axis']
        y_data = []
        x_data = []
        z_data = []
        for line in fp:
            row = trainingset.TrainingSetRow(trainingset.normalize_line(line), header)
            x_data.append(float(row.get(x_key)))
            y_data.append(float(row.get(y_key)))
            z_data.append(float(row.get(z_key)))

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x_data, y_data, z_data, label='observations')
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.set_zlabel(z_key)
        ax.legend()
        plt.show()


def main(opts):
    clickstream_path = 'data-example/clicks.csv'
    training_set_path = 'data-example/training_set.txt'
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        action = opts.action
        if action is Mode.statistic:
            show_statistics(clickstream_path)
        elif action is Mode.queries:
            create_queries_file(clickstream_path, data)
        elif action is Mode.histogram:
            hist_source = data['histogram']['source']
            if hist_source == 'click_stream':
                show_click_stream_histogram(clickstream_path, data)
            elif hist_source == 'training_set':
                show_training_set_histogram(training_set_path, data)
            else:
                print('Unsupported histogram source={}'.format(hist_source))
        elif action is Mode.scatter:
            scatted_plot_type = data['scatter']['type']
            if scatted_plot_type == '2d':
                show_scatter_2d_plot(training_set_path, data)
            elif scatted_plot_type == '3d':
                show_scatter_3d_plot(training_set_path, data)
            else:
                print('Unsupported scatter type={}'.format(scatted_plot_type))
        else:
            print('Unsupported action={}'.format(opts))


class Mode(Enum):
    statistic = 'statistic'
    queries = 'queries'
    histogram = 'histogram'
    scatter = 'scatter'

    def __str__(self):
        return self.value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=Mode, choices=list(Mode))
    main(parser.parse_args())
