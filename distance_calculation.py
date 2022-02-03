import sys
import numpy as np
from scipy.stats import wasserstein_distance
import gudhi.wasserstein
import numpy as np


def get_wasserstein_distance_gudhi(dgm_1, dgm_2):
    dgm_1 = np.array(dgm_1)
    dgm_2 = np.array(dgm_2)
    return gudhi.wasserstein.wasserstein_distance(dgm_1, dgm_2,
                                                  order=1., internal_p=2.)


def get_1_wasserstein_distance_gudhi():
    dgm1 = np.array([[2.7, 3.7], [9.6, 14.], [34.2, 34.974]])
    dgm2 = np.array([[2.8, 4.45], [9.5, 14.1]])

    message = "Wasserstein distance value = " + '%.2f' % gudhi.wasserstein.wasserstein_distance(
        dgm1, dgm2, order=1., internal_p=2.)
    print(message)
    # 1.45

    dgm1 = np.array([[0, 0.5], [0, 1.2], [0, 1.2], [0, 2.5], [0, 3.3]])
    dgm2 = np.array([[0, 0.5], [0, 1.2], [0, 2.0], [0, 2.5], [0, 5.0]])

    message = "Wasserstein distance value = " + '%.2f' % gudhi.wasserstein.wasserstein_distance(
        dgm1, dgm2, order=1., internal_p=2.)
    print(message)
    # 2.5


def get_1_wasserstein_distance(pd_1, pd_2):
    return wasserstein_distance([ar[1] for ar in pd_1],
                                [ar[1] for ar in pd_2])