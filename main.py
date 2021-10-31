from utils import get_dataset, draw_barcode_and_matrix, draw_barcode_only, \
    get_adjacency_for_triangle
from barcodes import get_n_dim_barcodes
from barcodes_manual import get_0_dim_barcodes
import os
import argparse


# Driver code

def demo():
    adjacency_matrix = get_dataset(filename="dataset_100_100.csv")
    barcodes = get_n_dim_barcodes(adjacency_matrix, 0)
    draw_barcode_only(barcodes, adjacency_matrix)

    adjacency_matrix = get_dataset()
    barcodes = get_n_dim_barcodes(adjacency_matrix, 0)
    draw_barcode_and_matrix(barcodes, adjacency_matrix)


def get_all_datasets():
    datasets = [test for test in os.listdir(".") if test.endswith(".csv")]
    datasets.sort()
    return datasets


def plot_barcode(dataset, show_matrix=False,
                 lower_matrix=False, upper_matrix=False):
    if lower_matrix is True:
        adjacency_matrix = get_adjacency_for_triangle(dataset)
    elif upper_matrix is True:
        adjacency_matrix = get_adjacency_for_triangle(dataset, lower=False)
    else:
        adjacency_matrix = get_dataset(filename=dataset)

    barcodes = get_0_dim_barcodes(adjacency_matrix)
    # print(barcodes)
    # print(len(barcodes))
    #
    # barcodes = get_n_dim_barcodes(adjacency_matrix, 0)
    # print(barcodes)
    # print(len(barcodes))
    #
    # barcodes = get_n_dim_barcodes(adjacency_matrix, 1)
    # print(barcodes)
    # print(len(barcodes))

    if show_matrix:
        draw_barcode_and_matrix(barcodes, adjacency_matrix)
    else:
        draw_barcode_only(barcodes, adjacency_matrix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', help='List available tests',
                        action='store_true')
    parser.add_argument("--all", '-a', help='Produce all demo',
                        action='store_true')
    parser.add_argument('--data', '-d',
                        help='Input a specific dataset ' \
                             '(case sensitive, must ends with .csv)')
    parser.add_argument('--lower', '-lo',
                        help='CSV contains lower triangular distance matrix',
                        action='store_true')
    parser.add_argument('--upper', '-up',
                        help='CSV contains upper triangular distance matrix ' \
                             ' (MATLAB output from the function pdist)',
                        action='store_true')
    parser.add_argument('--matrix', '-m',
                        help='Attach adjacency matrix with barcodes',
                        action='store_true')
    args = parser.parse_args()

    if args.all:
        demo()
        return

    if args.data:
        if not os.path.exists(f'{args.data}'):
            print(f'Dataset "{args.data}" not found')
        else:
            if args.matrix:
                plot_barcode(args.data, show_matrix=True,
                             lower_matrix=args.lower, upper_matrix=args.upper)
            else:
                plot_barcode(args.data, show_matrix=False,
                             lower_matrix=args.lower, upper_matrix=args.upper)
        return

    if args.list:
        print("Available dataset: ")
        print(*get_all_datasets(), sep='\n')
        return

    parser.print_help()


if __name__ == "__main__":
    main()
