import matplotlib.pyplot as plt
import random
import csv
import numpy as np


def get_adjacency_for_triangle(triangular_matrix, lower=True):
    matrix = []
    data = get_dataset(triangular_matrix)
    if lower:
        data = data[::-1]
    size = len(data) + 1
    for i in range(len(data)):
        row = data[i]
        temp = []
        for j in range(size - len(row) - 1):
            temp.append(matrix[j][i])
        temp.append(0)
        for value in row:
            temp.append(value)
        matrix.append(temp)
    i = size - 1
    temp = []
    for j in range(size - 1):
        temp.append(matrix[j][i])
    temp.append(0)
    matrix.append(temp)
    with open("mod.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(matrix)
    return matrix


def get_simplices(matrix):
    simplices = []
    for i in range(len(matrix)):
        simplices.append(([i], 0))
        for j in range(i + 1, len(matrix[0])):
            simplices.append(([i, j], matrix[i][j]))
    return simplices


def get_dataset(filename='dataset_4_4.csv', v=100, generate=False, fmri=False):
    if generate:
        return generate_large_dataset(v=v, filename=filename)
    data = []
    if fmri:
        with open(filename) as fmri_file:
            fmri_reader = csv.reader(fmri_file, delimiter='\t')
            for line in fmri_reader:
                values = []
                for c in line:
                    if c.strip() != "":
                        val = float(c.strip())
                        if np.isnan(val):
                            val = 0
                        values.append(val)
                data.append(values)
        return data
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            values = [float(c.strip()) for c in line if c.strip() != ""]
            data.append(values)
    return data


def generate_large_dataset(v=100, filename='large_dataset.csv'):
    ar = []
    for i in range(v):
        temp = []
        for j in range(v):
            if i == j:
                temp.append(0)
            elif j < i:
                temp.append(ar[j][i])
            else:
                temp.append(round(random.random(), 2))
        ar.append(temp)
    with open(filename, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(ar)
    return ar


def draw_barcode_and_matrix(data, matrix):
    plt.rcdefaults()
    fig, ax = plt.subplots(2)
    max_x_axis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax[0].barh(y_pos, values, align='center')
    ax[0].invert_yaxis()
    ax[0].set_xlabel('Delta')
    ax[0].set_title('0 dimensional barcodes')
    ax[0].set_xlim([0, max_x_axis])
    ax[0].bar_label(ax[0].containers[0])
    ax[1].set_title('Adjacency matrix')
    matrix = [["{:.2f}".format(j) for j in ar] for ar in matrix]
    ax[1].table(cellText=matrix,
                cellLoc='center',
                rowLoc='center',
                colLoc='center',
                loc='center')
    ax[1].axis('off')
    plt.tight_layout()
    plt.show()


def draw_barcode_only(data, matrix, show_value=False):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    max_x_axis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax.barh(y_pos, values, height=0.3, align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Delta')
    ax.set_title('0 dimensional barcodes: {} vertices, {} bars'.format(
        len(matrix[0]), len(data)
    ))
    if show_value:
        ax.bar_label(ax.containers[0])
    ax.set_xlim([0, max_x_axis])
    plt.tight_layout()
    plt.show()


def draw_bars(barcodes, matrix, show_value=False):
    bar_counts = len(barcodes)
    barcodes = np.array(barcodes)
    barcodes.sort(axis=1)
    means = np.mean(barcodes, axis=1)
    half_range = barcodes[:, 1] - means
    _, caps, _ = plt.errorbar(means, np.arange(bar_counts) + 1,
                              xerr=half_range,
                              ls='',
                              elinewidth=3)  # capsize=2 for boundary on bar
    for cap in caps:
        cap.set_markeredgewidth(3)
    plt.ylim(0, bar_counts + 1)
    plt.show()
