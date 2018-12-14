import json
import requests
from model import trainingset, clickstream


def get_solr_url(conf):
    server = conf['indexing']['server']
    core = conf['indexing']['core_name']
    return 'http://' + server + '/solr/' + core + '/update'


def index_docs(docs, solr_url):
    params = {
        "commitWithin": 5000,
        "overwrite": "true",
        "wt": "json"
    }
    response = requests.post(url=solr_url, params=params, json=docs)
    if response.status_code != 200:
        print(response.content)
        response.raise_for_status()


def read_click_data_dict(path):
    with open(path) as fp:
        print("Building click data dictionary Started.")
        cs_header = clickstream.normalise_cs_line(next(fp))  # get header
        result = {}
        for cs_line in fp:
            try:
                cs_row = clickstream.ClickStreamRow.new_v2_row(clickstream.normalise_cs_line(cs_line), cs_header)
                result[cs_row.get_qd_pair()] = cs_row.get_clicks_data_as_dict()
            except ValueError:
                print("Skip incorrect line.")
        print("Building click data dictionary finished.")
        print('Total dict size {}'.format(len(result)))
        return result


if __name__ == "__main__":
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
        url = get_solr_url(config)
        batch_size = config['indexing']['batch_size']
        click_stream_file_path = config['file']['click_stream']
        training_set_file_path = config['file']['training_set']

        with open(training_set_file_path) as training_set_file:
            click_data_dict = read_click_data_dict(click_stream_file_path)
            header = trainingset.normalize_header(next(training_set_file))
            docs_batch = []
            indexed = 0
            batch_num = 0
            for line in training_set_file:
                row = trainingset.TrainingSetRow(trainingset.normalize_line(line), header)
                doc_for_index = row.get_as_dict()
                qd_key = row.get_qd_pair()
                if qd_key in click_data_dict:
                    doc_for_index.update(click_data_dict[qd_key])
                else:
                    print('Not joined by key for={}'.format(qd_key))
                    continue
                docs_batch.append(doc_for_index)
                indexed += 1
                if len(docs_batch) >= batch_size:
                    index_docs(docs_batch, url)
                    docs_batch.clear()
                    batch_num += 1
                    print('Batch #{}. Total indexed {} docs.'.format(batch_num, indexed))
            if len(docs_batch) > 0:
                index_docs(docs_batch, url)
            print('Full run indexed {} documents.'.format(indexed))