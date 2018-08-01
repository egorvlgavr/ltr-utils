import json
import requests
from model import trainingset


def get_solr_url(server, core):
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


if __name__ == "__main__":
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
        url = get_solr_url(config['indexing']['server'], config['indexing']['core_name'])
        batch_size = config['indexing']['batch_size']
        with open('data-example/training_set.txt') as training_set_file:
            header = trainingset.normalize_header(next(training_set_file))
            docs_batch = []
            indexed = 0
            batch_num = 0
            for line in training_set_file:
                row = trainingset.TrainingSetRow(trainingset.normalize_line(line), header)
                docs_batch.append(row.get_as_dict())
                indexed += 1
                if len(docs_batch) >= batch_size:
                    index_docs(docs_batch, url)
                    docs_batch.clear()
                    batch_num += 1
                    print('Batch #{}. Total indexed {} docs.'.format(batch_num, indexed))
            if len(docs_batch) > 0:
                index_docs(docs_batch, url)
            print('Full run indexed {} documents.'.format(indexed))
