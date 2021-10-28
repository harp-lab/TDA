from utils import get_dataset, draw_barcode_and_matrix, draw_barcode_only
from barcodes import get_barcodes
import os, argparse


# Driver code

def demo():
    adjacency_matrix = get_dataset(filename="dataset_100_100.csv")
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_only(barcodes, adjacency_matrix)

    adjacency_matrix = get_dataset()
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_and_matrix(barcodes, adjacency_matrix)


def get_all_datasets():
    datasets = [test for test in os.listdir(".") if test.endswith(".csv")]
    datasets.sort()
    return datasets


def barcode_only(dataset):
    adjacency_matrix = get_dataset(filename=dataset)
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_only(barcodes, adjacency_matrix)


def barcode_and_matrix(dataset):
    adjacency_matrix = get_dataset(filename=dataset)
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_and_matrix(barcodes, adjacency_matrix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', help='List available tests', action='store_true')
    parser.add_argument("--all", '-a', help='Produce all demo', action='store_true')
    parser.add_argument('--data', '-d', help='Input a specific dataset (case sensitive, must ends with .csv)')
    parser.add_argument('--matrix', '-m', help='Attach adjacency matrix with barcodes', action='store_true')
    args = parser.parse_args()

    if args.all:
        demo()
        return

    if args.data:
        if not os.path.exists(f'{args.data}'):
            print(f'Dataset "{args.data}" not found')
        else:
            if args.matrix:
                barcode_and_matrix(args.data)
            else:
                barcode_only(args.data)
        return

    if args.list:
        print("Available dataset: ")
        print(*get_all_datasets(), sep='\n')
        return

    parser.print_help()


if __name__ == "__main__":
    main()
