class TreeSplit:
    def __init__(self, feature, threshold):
        self.feature = feature
        self.threshold = float(threshold)

    def __eq__(self, o) -> bool:
        return (self.__class__ == o.__class__
                and self.feature == o.feature
                and self.threshold == o.threshold)

    def __hash__(self) -> int:
        return hash((self.feature, self.threshold))

    def __str__(self) -> str:
        return str(self.feature) + ',' + str(self.threshold)

    def __lt__(self, o) -> bool:
        return (self.feature, self.threshold) < (o.feature, o.threshold)


class SplitStatistic:
    def __init__(self) -> None:
        self.models = set()
        self.num_of_use = 0
        self.gini_index = -1

    def count_usage(self, model_num) -> None:
        self.models.add(model_num)
        self.num_of_use += 1

    def to_row(self) -> str:
        return ','.join([str(len(self.models)),
                         str(self.num_of_use),
                         '{0:.6f}'.format(self.gini_index)])

    def set_gini_index(self, gini_index) -> None:
        self.gini_index = gini_index


