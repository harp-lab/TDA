import os
import argparse
import json
import numpy as np

from utils import get_dataset, get_adjacency_for_triangle, draw_bars
from mds_calculation import get_mds, plot_mds
import barcodes_ripser

# Driver code


def demo():
    subject_number = 1
    data_path = f'dfc_2500_subjects_distance_matrix/subject_{subject_number}.json'

    dissimilarity_matrix = np.array(json.loads(open(data_path, "r").read()))
    mds = get_mds(dissimilarity_matrix)
    plot_mds(mds, subject_number)

    # dissimarity_matrix = np.array(di)

    # print("Manual barcodes: ")
    # manual_barcodes = get_0_dim_barcodes(adjacency_matrix)
    # print(manual_barcodes == ripser_barcodes)
    # print("=" * 24)

    # adjacency_matrix_0 = get_adjacency_for_triangle("g0.csv")
    # barcodes_0 = get_0_dim_barcodes(adjacency_matrix_0)
    # barcodes_0 = barcodes_0[::-1]
    #
    # adjacency_matrix_1 = get_adjacency_for_triangle("g1.csv")
    # barcodes_1 = get_0_dim_barcodes(adjacency_matrix_1)
    # barcodes_1 = barcodes_1[::-1]
    #
    # adjacency_matrix_2 = get_adjacency_for_triangle("g2.csv")
    # barcodes_2 = get_0_dim_barcodes(adjacency_matrix_2)
    # barcodes_2 = barcodes_2[::-1]
    #
    # print(barcodes_0)
    # print(barcodes_2)
    #
    # # was_dis_0_1 = get_1_wasserstein_distance(barcodes_0, barcodes_1)
    # was_dis_0_2 = get_1_wasserstein_distance(barcodes_0, barcodes_2)
    # # was_dis_1_2 = get_1_wasserstein_distance(barcodes_1, barcodes_2)
    # # #
    # # print(was_dis_0_1, was_dis_0_2, was_dis_1_2)
    # print(was_dis_0_2)
    # # print(len(barcodes))
    # # for i, pair in enumerate(barcodes):
    # #     print(i, pair)
    # # draw_bars(barcodes, adjacency_matrix)


def get_all_datasets():
    datasets = [test for test in os.listdir(".") if test.endswith(".csv")]
    datasets.sort()
    return datasets


def plot_barcode(dataset, dimension=0,
                 lower_matrix=False, upper_matrix=False):
    if lower_matrix is True:
        adjacency_matrix = get_adjacency_for_triangle(dataset)
    elif upper_matrix is True:
        adjacency_matrix = get_adjacency_for_triangle(dataset, lower=False)
    else:
        adjacency_matrix = get_dataset(filename=dataset)
    if dimension == 0:
        barcodes = barcodes_ripser.get_0_dim_barcodes(adjacency_matrix)
        barcodes = barcodes[::-1]
        print(
            "Barcodes generated using Graph algorithm (connected components)")
    else:
        barcodes = barcodes_ripser.get_n_dim_barcodes(matrix=adjacency_matrix,
                                                      n=dimension)
        print("Barcodes generated using Ripser library")
    print(len(barcodes))
    for i, pair in enumerate(barcodes):
        print(i, pair)
    draw_bars(barcodes, adjacency_matrix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', help='List available tests',
                        action='store_true')
    parser.add_argument("--all", '-a', help='Produce all demo',
                        action='store_true')
    parser.add_argument('--data', '-d',
                        help='Input a specific dataset '
                             '(case sensitive, must ends with .csv)')
    parser.add_argument('--dim', '-di',
                        help='Input a dimension '
                             '(0-n)')
    parser.add_argument('--lower', '-lo',
                        help='CSV contains lower triangular distance matrix',
                        action='store_true')
    parser.add_argument('--upper', '-up',
                        help='CSV contains upper triangular distance matrix '
                             ' (MATLAB output from the function pdist)',
                        action='store_true')
    args = parser.parse_args()

    if args.all:
        demo()
        return

    if args.data:
        if not os.path.exists(f'{args.data}'):
            print(f'Dataset "{args.data}" not found')
        else:
            if args.dim:
                plot_barcode(args.data, dimension=int(args.dim),
                             lower_matrix=args.lower, upper_matrix=args.upper)
            else:
                plot_barcode(args.data, dimension=0,
                             lower_matrix=args.lower, upper_matrix=args.upper)
        return

    if args.list:
        print("Available dataset: ")
        print(*get_all_datasets(), sep='\n')
        return

    parser.print_help()
    demo()
    return


if __name__ == "__main__":
    main()