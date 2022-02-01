import json
import numpy as np
from utils import get_dataset
import barcodes_ripser
from distance_calculation import get_wasserstein_distance_gudhi
from mds_calculator import get_mds


def get_mds_matrix(subject_id):
    data_path = f'subjects_distance_matrix/subject_{subject_id}.json'
    dissimilarity_matrix = np.array(json.loads(open(data_path, "r").read()))
    mds_matrix = get_mds(dissimilarity_matrix)
    return json.dumps(mds_matrix.tolist())


def get_dissimilarity_matrix(data_dir, subject_number):
    dissimilarity_matrix = [[0 for j in range(86)] for i in range(86)]
    for i in range(1, 87):
        for j in range(1, i):
            filepath_1 = f'{data_dir}/normalize_dfc_2500_subject_{subject_number}_time_{i}.txt'
            adjacency_matrix_1 = get_dataset(filename=filepath_1, fmri=True)

            ripser_barcodes_1 = barcodes_ripser.get_0_dim_barcodes(
                adjacency_matrix_1,
                max_value=1.0)

            filepath_2 = f'{data_dir}/normalize_dfc_2500_subject_{subject_number}_time_{j}.txt'
            adjacency_matrix_2 = get_dataset(filename=filepath_2, fmri=True)

            ripser_barcodes_2 = barcodes_ripser.get_0_dim_barcodes(
                adjacency_matrix_2,
                max_value=1.0)
            distance = get_wasserstein_distance_gudhi(ripser_barcodes_1,
                                                      ripser_barcodes_2)
            distance = round(distance, 3)
            dissimilarity_matrix[i - 1][j - 1] = distance
            dissimilarity_matrix[j - 1][i - 1] = distance
    return dissimilarity_matrix


def generate_distance_matrix(data_dir, generated_json_directory):
    for subject_number in range(1, 317):
        generated_json = f'{generated_json_directory}/subject_{subject_number}.json'
        dissimilarity_matrix = get_dissimilarity_matrix(data_dir,
                                                        subject_number)
        with open(generated_json, "w") as f:
            json.dump(dissimilarity_matrix, f)
            print(f"JSON created for Subject {subject_number}")
    print("Done generating the JSON files")


def generate_mds(mds_directory, json_directory):
    for subject_number in range(1, 317):
        generated_mds = f'{mds_directory}/subject_{subject_number}.json'
        mds_matrix = get_mds_matrix(subject_number)
        with open(generated_mds, "w") as f:
            json.dump(mds_matrix, f)
            print(f"JSON created for Subject {subject_number}")
    print("Done generating the JSON files")


if __name__ == "__main__":
    data_directory = "full_data/dfc_2500_normal"
    json_directory = "subjects_distance_matrix"
    mds_directory = "subjects_mds"
    # generate_distance_matrix(data_directory, json_directory)
    generate_mds(mds_directory, json_directory)
