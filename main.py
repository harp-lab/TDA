from utils import get_dataset, draw_barcode_and_matrix, draw_barcode_only
from barcodes import get_barcodes

# Driver code
if __name__ == '__main__':
    adjacency_matrix = get_dataset(filename="dataset_100_100.csv")
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_only(barcodes, adjacency_matrix)

    adjacency_matrix = get_dataset()
    barcodes = get_barcodes(adjacency_matrix)
    draw_barcode_and_matrix(barcodes, adjacency_matrix)
