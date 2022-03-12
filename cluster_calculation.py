from sklearn.cluster import OPTICS
import numpy as np
import json


def get_number_of_clusters(mds_data, min_points=10):
    clusters = OPTICS(min_samples=min_points).fit(mds_data)
    labels = clusters.labels_
    return len(np.unique(labels))


def get_number_of_clusters_from_datafile(datafile, min_points=10):
    with open(datafile, "r") as json_file:
        dataset = json.loads(json.loads(json_file.read()))
        return get_number_of_clusters(dataset, min_points)


if __name__ == "__main__":
    clusters = {}
    for i in range(1, 11):
        datafile_2500 = f"visualizor/dfc_2500_subjects_mds/subject_{i}.json"
        datafile_1400 = f"visualizor/dfc_1400_subjects_mds/subject_{i}.json"
        clusters[i] = [
            get_number_of_clusters_from_datafile(datafile_2500, min_points=15),
            get_number_of_clusters_from_datafile(datafile_1400, min_points=30)
        ]
    print(clusters)
