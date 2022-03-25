import numpy as np


class summary_stats_class():

    def __init__(self, data):
        self.data = data
        self.min_data = min(data)
        self.max_data = max(data)
        self.mean_data = sum(data) / len(data)
        self.std_data = np.std(data)

    def get_summary_stats(self):
        return self.min_data, self.max_data, self.mean_data

    def min_max_scale(self):
        return [(i - self.min_data) / (self.max_data - self.min_data) for i in
                self.data]

    def zscore_scale(self):
        return [(i - self.mean_data) / self.std_data for i in self.data]


if __name__ == "__main__":
    ssc = summary_stats_class([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(ssc.get_summary_stats())
    print(ssc.min_max_scale())
    print(ssc.zscore_scale())
