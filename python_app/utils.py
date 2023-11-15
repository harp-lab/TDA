import matplotlib.pyplot as plt
import random
import csv


def get_dataset(filename='dataset_4_4.csv', v=100, generate=False):
    if generate:
        return generate_large_dataset(v=v, filename=filename)
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in zip(*csv_reader):
            data.append(list(map(float, row)))
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
    max_xaxis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax[0].barh(y_pos, values, align='center')
    ax[0].invert_yaxis()
    ax[0].set_xlabel('Delta')
    ax[0].set_title('0 dimensional barcodes')
    ax[0].set_xlim([0, max_xaxis])
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


def draw_barcode_only(data, matrix):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    max_xaxis = sorted([i[1] for i in data], reverse=True)[0]
    y_pos = [i for i in range(len(data))]
    values = [pair[1] for pair in data]
    ax.barh(y_pos, values, height=0.3, align='center')
    ax.invert_yaxis()
    ax.set_xlabel('Delta')
    ax.set_title('0 dimensional barcodes: {} vertices, {} bars'.format(
        len(matrix[0]), len(data)
    ))
    ax.set_xlim([0, max_xaxis])
    plt.tight_layout()
    plt.show()
