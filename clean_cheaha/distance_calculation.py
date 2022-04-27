import json
import gudhi
import gudhi.wasserstein
import numpy as np
from utils import get_dataset
from mds_calculation import get_mds


def get_wasserstein_distance_gudhi(dgm_1, dgm_2):
    return gudhi.wasserstein.wasserstein_distance(dgm_1, dgm_2,
                                                  order=1., internal_p=2.)


def get_mds_matrix(subject_id, json_directory):
    data_path = f'{json_directory}/subject_{subject_id}.json'
    dissimilarity_matrix = np.array(json.loads(open(data_path, "r").read()))
    mds_matrix = get_mds(dissimilarity_matrix)
    return json.dumps(mds_matrix.tolist())


def get_dissimilarity_matrix(data_dir, subject_number, timeslots,
                             normalize_file_prefix):
    dissimilarity_matrix = np.array([[0 for j in range(timeslots)] for i in
                                     range(timeslots)])
    barcodes = {}
    for i in range(1, timeslots + 1):
        time_1 = f"time_{i}"
        if time_1 not in barcodes:
            filepath_1 = f'{data_dir}/{normalize_file_prefix}{subject_number}_time_{i}.txt'
            adjacency_matrix_1 = get_dataset(filename=filepath_1, fmri=True)
            rips_complex_1 = gudhi.RipsComplex(distance_matrix=adjacency_matrix_1)
            pd_1 = rips_complex_1.create_simplex_tree(max_dimension=1).persistence()[1:]
            barcodes_1 = np.array([pair[1] for pair in pd_1])
            barcodes[time_1] = barcodes_1
        else:
            barcodes_1 = barcodes[time_1]
        for j in range(1, i):
            time_2 = f"time_{j}"
            if time_2 not in barcodes:
                filepath_2 = f'{data_dir}/{normalize_file_prefix}{subject_number}_time_{j}.txt'
                adjacency_matrix_2 = get_dataset(filename=filepath_2, fmri=True)
                rips_complex_2 = gudhi.RipsComplex(distance_matrix=adjacency_matrix_2)
                pd_2 = rips_complex_2.create_simplex_tree(max_dimension=1).persistence()[1:]
                barcodes_2 = np.array([pair[1] for pair in pd_2])
                barcodes[time_2] = barcodes_2
            else:
                barcodes_2 = barcodes[time_2]
            distance = get_wasserstein_distance_gudhi(barcodes_1,
                                                      barcodes_2)
            distance = round(distance, 3)
            dissimilarity_matrix[i - 1][j - 1] = distance
            dissimilarity_matrix[j - 1][i - 1] = distance
    return dissimilarity_matrix


def generate_distance_matrix(data_dir, generated_json_directory,
                             total_subjects, total_timeslots,
                             normalize_file_prefix, start_subject=None,
                             end_subject=None):
    if start_subject == None:
        start_subject = 1
        end_subject = total_subjects
    for subject_number in range(start_subject, end_subject + 1):
        print(f"Generating distance matrix for Subject {subject_number}")
        generated_json = f'{generated_json_directory}/subject_{subject_number}.json'
        dissimilarity_matrix = get_dissimilarity_matrix(data_dir,
                                                        subject_number,
                                                        total_timeslots,
                                                        normalize_file_prefix)
        with open(generated_json, "w") as f:
            json.dump(dissimilarity_matrix.tolist(), f)
            print(
                f"Wasserstein distance JSON created for Subject {subject_number}")
    print("Done generating the Wasserstein distance matrix JSON files")


def generate_mds(mds_directory, json_directory, total_subjects,
                 start_subject=None,
                 end_subject=None
                 ):
    if start_subject == None:
        start_subject = 1
        end_subject = total_subjects
    for subject_number in range(start_subject, end_subject + 1):
        generated_mds = f'{mds_directory}/subject_{subject_number}.json'
        mds_matrix = get_mds_matrix(subject_number, json_directory)
        with open(generated_mds, "w") as f:
            json.dump(mds_matrix, f)
            print(f"MDS JSON created for Subject {subject_number}")
    print("Done generating the MDS JSON files")


if __name__ == "__main__":
    # data_directory = "full_data/dfc_2500_normal"
    # json_directory = "dfc_2500_subjects_distance_matrix"
    # mds_directory = "dfc_2500_subjects_mds"
    # normalize_file_prefix = 'normalize_dfc_2500_subject_'
    # total_subjects = 10
    # total_timeslots = 754

    # DFC 645
    # data_directory = "full_data/dfc_645_normal_partial"
    # json_directory = "dfc_645_subjects_distance_matrix"
    # mds_directory = "dfc_645_subjects_mds"
    # normalize_file_prefix = 'normalize_dfc_645_subject_'
    # total_subjects = 1
    # total_timeslots = 2
    #
    # generate_distance_matrix(data_directory, json_directory,
    #                          total_subjects, total_timeslots,
    #                          normalize_file_prefix)
    # generate_mds(mds_directory, json_directory, total_subjects)

    # DFC 1400
    # data_directory = "../dfc_1400_normal"
    # json_directory = "dfc_1400_subjects_distance_matrix"
    # mds_directory = "dfc_1400_subjects_mds"
    # normalize_file_prefix = 'normalize_dfc_1400_subject_'
    # total_subjects = 306
    # start_subject = 11
    # end_subject = 231
    # total_timeslots = 336

    # DFC 645
    # data_directory = "../dfc_645_normal_update"
    # json_directory = "dfc_645_subjects_distance_matrix"
    # mds_directory = "dfc_645_subjects_mds"
    # normalize_file_prefix = 'normalize_dfc_645_subject_'
    # total_subjects = 316
    # start_subject = 1
    # end_subject = 316
    # total_timeslots = 754
    data_directory = "../fmri_data"
    json_directory = "dfc_2500_1_subjects_distance_matrix"
    mds_directory = "dfc_2500_1_subjects_mds"
    normalize_file_prefix = 'normalize_dfc_2500_subject_'
    total_subjects = 1
    start_subject = 1
    end_subject = 1
    total_timeslots = 86

    generate_distance_matrix(data_directory, json_directory,
                             total_subjects, total_timeslots,
                             normalize_file_prefix, start_subject, end_subject)
    generate_mds(mds_directory, json_directory, total_subjects, start_subject,
                 end_subject)
