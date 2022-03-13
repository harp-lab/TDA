import json
from sklearn.cluster import OPTICS
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score


def get_labels_highest_score(dataset):
    max_score = -99999
    labels = None
    for i in range(2, 16):
        cluster = KMeans(n_clusters=i, random_state=10)
        cluster_labels = cluster.fit_predict(dataset)
        score = silhouette_score(dataset, cluster_labels)
        if score > max_score:
            max_score = score
            labels = cluster_labels
    return labels


def get_cluster_labels(dataset, min_points=15):
    # clusters = OPTICS(min_samples=min_points).fit(dataset)
    clusters = OPTICS(cluster_method='dbscan', eps=1).fit(dataset)
    return clusters.labels_


def get_dataset(datafile):
    with open(datafile, "r") as json_file:
        return np.array(json.loads(json.loads(json_file.read())))


def show_clusters(labels, unique_labels, dataset, title, index):
    ax = plt.subplot(1, 2, index)
    for i in unique_labels:
        x = dataset[labels == i, 0]
        y = dataset[labels == i, 1]
        label = f"cluster {i + 1}"
        if i == -1:
            label = "noise"
        ax.scatter(x, y, label=label)
        ax.legend()
    ax.set_title(title)
    plt.tight_layout()


if __name__ == "__main__":
    cluster_info = {}
    min_points_2500 = 15
    min_points_1400 = 30
    for i in range(1, 11):
        datafile_2500 = f"visualizor/dfc_2500_subjects_mds/subject_{i}.json"
        datafile_1400 = f"visualizor/dfc_1400_subjects_mds/subject_{i}.json"
        dataset_2500 = get_dataset(datafile_2500)
        dataset_1400 = get_dataset(datafile_1400)
        # labels_2500 = get_cluster_labels(dataset_2500, min_points_2500)
        labels_2500 = get_labels_highest_score(dataset_2500)
        unique_labels_2500 = np.unique(labels_2500)
        # labels_1400 = get_cluster_labels(dataset_1400, min_points_1400)
        labels_1400 = get_labels_highest_score(dataset_1400)
        unique_labels_1400 = np.unique(labels_1400)
        n_clusters_2500 = len([i for i in unique_labels_2500 if i != -1])
        n_clusters_1400 = len([i for i in unique_labels_1400 if i != -1])
        cluster_info[i] = [
            n_clusters_2500, n_clusters_1400
        ]
        title = f'DFC2500 subject {i}: {n_clusters_2500} clusters'
        show_clusters(labels_2500, unique_labels_2500, dataset_2500, title, 1)
        title = f'DFC1400 subject {i}: {n_clusters_1400} clusters'
        show_clusters(labels_1400, unique_labels_1400, dataset_1400, title, 2)
        plt.show()
    print(cluster_info)
