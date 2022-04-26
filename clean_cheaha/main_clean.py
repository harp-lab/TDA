import math
import time

from utils import get_dataset
import gudhi
import gudhi.wasserstein
import numpy as np


def calculate_wasserstein():
    start = time.time()
    filepath_1 = "../fmri_data/normalize_dfc_2500_subject_1_time_10.txt"
    filepath_2 = "../fmri_data/normalize_dfc_2500_subject_1_time_20.txt"
    adjacency_matrix_1 = get_dataset(filename=filepath_1, fmri=True)
    adjacency_matrix_2 = get_dataset(filename=filepath_2, fmri=True)

    rips_complex_1 = gudhi.RipsComplex(distance_matrix=adjacency_matrix_1)
    pd_1 = rips_complex_1.create_simplex_tree(max_dimension=1).persistence()[1:]
    barcodes_1 = np.array([pair[1] for pair in pd_1])

    rips_complex_2 = gudhi.RipsComplex(distance_matrix=adjacency_matrix_2)
    pd_2 = rips_complex_2.create_simplex_tree(max_dimension=1).persistence()[1:]
    barcodes_2 = np.array([pair[1] for pair in pd_2])

    dist_1_2 = gudhi.wasserstein.wasserstein_distance(barcodes_1, barcodes_2,
                                                      order=1., internal_p=2.)
    print(dist_1_2)
    print(time.time() - start)

calculate_wasserstein()