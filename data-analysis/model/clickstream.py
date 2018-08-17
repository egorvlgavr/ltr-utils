from model import qdpair


def safely_parse_int(value):
    if value == '':
        return 0
    else:
        return int(value)

# TODO(test)
class ClickStreamRow:
    """
    "Search_Term","PPID_Clicked","Total_Times_Clicked","Total_Times_AddToBag","Total_Times_Checked_Out","Total_Search_Count"
    """
    def __init__(self, line, header, order=(0, 1, 5, 2, 3, 4)):
        cols = line.split(",")
        self.phrase = cols[order[0]]
        self.product = cols[order[1]]
        self.impr = safely_parse_int(cols[order[2]])
        self.clicks = safely_parse_int(cols[order[3]])
        self.add_to_cart = safely_parse_int(cols[order[4]])
        self.checked_out = safely_parse_int(cols[order[5]])
        self.col_by_name = {}
        col_names = header.split(",")
        for i in range(len(cols)):
            self.col_by_name[col_names[i]] = cols[i]

    # TODO(test V2)
    @staticmethod
    def new_v2_row(line, header):
        """
        Search_Term,PPID_Clicked,Total_Search_Count,Total_Times_Clicked,Total_Times_AddToBag,Total_Times_Checked_Out
        """
        return ClickStreamRow(line, header, (0, 1, 2, 3, 4, 5))

    def get(self, name):
        return self.col_by_name[name]

    def get_qd_pair(self):
        return qdpair.QueryDocumentPair(self.phrase, self.product)

    def get_clicks_data_as_dict(self):
        return {
            'search_count': self.impr,
            'clicked': self.clicks,
            'add_to_bag': self.add_to_cart,
            'checked_out': self.checked_out
        }


def normalise_cs_line(line):
    return line.replace("\n", "").replace('"','')
