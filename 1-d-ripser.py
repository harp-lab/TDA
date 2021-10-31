import numpy as np
from ripser import ripser
from persim import plot_diagrams
from utils import get_dataset


def default_example():
    data = np.random.random((100, 2))
    diagrams = ripser(data)['dgms']
    print(len(diagrams[0]))
    # plot_diagrams(diagrams, show=True)


def get_ph():
    matrix = np.array(get_dataset("dataset_100_100.csv"))
    diagrams = ripser(matrix, distance_matrix=True)['dgms']
    print(len(diagrams[0]))


def draw_bar():
    nsamples = 20
    xmin, xmax = 0, 150
    samples = np.random.random_sample((nsamples, 2)) * (xmax - xmin) + xmin
    print(samples)


if __name__ == "__main__":
    # default_example()
    # get_ph()
    draw_bar()
