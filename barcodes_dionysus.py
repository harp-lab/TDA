import math
import dionysus as d
from utils import get_simplices


def get_n_dim_barcodes(matrix, n):
    barcodes = []
    simplices = get_simplices(matrix)
    ph_filter = d.Filtration()
    for vertices, distance in simplices:
        ph_filter.append(d.Simplex(vertices, distance))
    ph_filter.sort()
    boundary_matrix = d.homology_persistence(ph_filter)
    diagrams = d.init_diagrams(boundary_matrix, ph_filter)
    # d.plot.plot_bars(diagrams[n], show=True)
    if len(diagrams) > n:
        pd = sorted(diagrams[n], key=lambda x: x.death)
        prev_value = 0
        for bar in pd:
            if bar.death == math.inf:
                barcodes.append([bar.birth, prev_value])
            else:
                value = round(bar.death, 2)
                barcodes.append([bar.birth, value])
                prev_value = value
    return barcodes
