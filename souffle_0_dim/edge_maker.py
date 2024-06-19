import csv
import argparse
import shutil


def parse_command_line_args():
    parser = argparse.ArgumentParser(prog="Adjacency matrix to adjacency list maker",
                                     description="Convert adjacency matrix to adjacency list",
                                     epilog="Uses Python 3")
    parser.add_argument('-d', '--dir', nargs="?", default=None, help="Path to the dataset directory(optional)")
    parser.add_argument('-m', '--matrix', nargs="?", default=None, help="Path to the adjacency matrix (optional)")
    parser.add_argument('-o', '--output', nargs="?", default=None, help="Output filename (optional)")
    args = parser.parse_args()
    return args.dir, args.matrix, args.output

def get_delimiter(filepath):
    with open(filepath, 'r') as file:
        first_line = file.readline()
        if ',' in first_line:
            return ','
        elif '\t' in first_line:
            return '\t'
        else:
            raise ValueError("Could not detect delimiter")


def read_csv(filepath):
    data = []
    delimiter = get_delimiter(filepath)
    with open(filepath) as file:
        csv_file = csv.reader(file, delimiter=delimiter)
        for row in csv_file:
            row = list(map(float, row))
            data.append(row)

    return data

def write_csv(filepath, data):
    with open(filepath, "w") as file:
        csv_file = csv.writer(file, delimiter="\t")
        csv_file.writerows(data)
    return True


def convert_to_edge(data):
    updated_data = []
    for i in range(len(data)):
        for j in range(i, len(data[i])):
            row = [i+1, j+1, data[i][j]]
            updated_data.append(row)
    return updated_data




if __name__ == "__main__":
    dir_path, matrix_path, output_filename = parse_command_line_args()
    edge_file = "data/edge.facts"
    if not output_filename:
        output_filename = matrix_path.split(".csv")[0]+".facts"
    data = read_csv(matrix_path)
    converted_data = convert_to_edge(data)
    if write_csv(output_filename, converted_data):
        shutil.copyfile(output_filename, edge_file)
        print(f"Wrote {output_filename} and copied to {edge_file}")

# python edge_maker.py -m data/dataset_4_4.csv

