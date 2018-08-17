
import json
import requests
import matplotlib.pyplot as plt


def do_aggregation_query(solr_url):
    params = {
        'q': '*: *',
        'rows': '0',
        'json.facet': '{view_count_0_to_10: {'
                      'type: query, '
                      'q: "productViewCount:[0 TO 10]", '
                      'facet: {clicks: {type: terms, field: clicked, limit: -1}}'
                      '}}'
    }
    response = requests.get(url=solr_url, params=params)
    if response.status_code != 200:
        print(response.content)
        response.raise_for_status()
    return response.json()


def get_solr_url(server, core):
    return 'http://' + server + '/solr/' + core + '/query'


if __name__ == '__main__':
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
        url = get_solr_url(config['indexing']['server'], config['indexing']['core_name'])
        batch_size = config['indexing']['batch_size']
        result = do_aggregation_query(url)
        print(result)
        # TODO(build bar plot)



