class ClickStreamRow:
    def __init__(self, line, header):
        cols = line.split(",")
        self.phrase = cols[0]
        self.product = cols[1]
        self.impr = int(cols[2])
        self.clicks = int(cols[3])
        self.add_to_cart = int(cols[4])
        self.col_by_name = {}
        col_names = header.split(",")
        for i in range(len(cols)):
            self.col_by_name[col_names[i]] = cols[i]

    def get(self, name):
        return self.col_by_name[name]
