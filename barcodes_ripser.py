import math
import numpy as np
from ripser import ripser


def get_n_dim_barcodes(matrix, n):
    barcodes = []
    matrix = np.array(matrix)
    diagrams = ripser(matrix, distance_matrix=True)['dgms']
    if len(diagrams) > n:
        pd = sorted(diagrams[n], key=lambda x: x[1])
        prev_value = 0
        for bar in pd:
            if bar[1] == math.inf:
                barcodes.append([bar[0], prev_value])
            else:
                value = round(bar[1], 2)
                barcodes.append([bar[0], value])
                prev_value = value
    return barcodes
