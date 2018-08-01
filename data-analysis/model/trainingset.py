HEADER_PAIRS_SPLITTER = '='


class TrainingSetRow:
    """
    Represent training set line following format:
    2 qid:0 0:0 1:4.1 #red jeans=1120
    rank | qid| features| query| product_id

    Header has following format:
    #0=on_sale,1=bm25_score
    """
    def __init__(self, line, header):
        line_data, comment = line.split("#")

        # query is str value
        # product id is str value
        self.query, self.product_id = comment.split(HEADER_PAIRS_SPLITTER)

        cols = line_data.strip().split(' ')
        # rank is int value
        self.rank = int(cols[0])
        # qid is int value
        self.qid = int(cols[1].split(':')[1])
        # parse features
        feature_values_to_num = {}
        for i in range(2, len(cols)):
            pair = cols[i]
            num, feature_value = pair.split(":")
            feature_values_to_num[num] = feature_value
        num_to_names_list = header.replace("#", "").split(",")
        # dict key is name value is feature value
        # header is used to resolve it
        self.features = {}
        for num_to_name in num_to_names_list:
            num, feature_name = num_to_name.split(HEADER_PAIRS_SPLITTER)
            self.features[feature_name] = feature_values_to_num[num]

    def get(self, name):
        if name == 'rank':
            return self.rank
        else:
            return self.features[name]

    def get_as_dict(self):
        result = {
            'qid': self.qid,
            'product_id': self.product_id,
            'query': self.query,
            'rank': self.rank
        }
        result.update(self.features)
        return result


def normalize_header(line):
    return line.rpartition("#")[2].strip().replace("\n", "")


def normalize_line(line):
    return line.replace("\n", "").strip()
