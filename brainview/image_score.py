import os, csv
from image_similarity_measures.evaluate import evaluation
import pandas as pd
import cv2


def write_csv_results(filename, results, columns):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"\nDone writing {filename}")


def get_similarity_score(subjects, bars, cohorts, dataset_type, metrics, view_type):
    data = []
    for subject in subjects:
        subject_path = os.path.join("paper_exp", f"{view_type}_view", f"{dataset_type}", f"subject{subject}")
        for bar in bars:
            for i in range(len(cohorts)):
                for j in range(i + 1, len(cohorts)):
                    org_img_path = os.path.join(subject_path, f"{cohorts[i]}_{bar}.png")
                    pred_img_path = os.path.join(subject_path, f"{cohorts[j]}_{bar}.png")
                    output = evaluation(org_img_path=org_img_path,
                                        pred_img_path=pred_img_path,
                                        metrics=metrics)
                    scores = []
                    for metric in metrics:
                        scores.append(round(output[metric], 3))
                    row = [dataset_type, subject, bar, cohorts[i], cohorts[j]] + scores
                    print(row)
                    data.append(row)
    return data


def generate_scores_generic(subjects, cohorts, bars, columns, dataset_type, output_file, view_type):
    print(f"{dataset_type}")
    print("-" * 15)
    results = get_similarity_score(subjects, bars, cohorts, dataset_type, metrics, view_type)
    print("=" * 15)
    print("\n\n\n\n")
    write_csv_results(output_file, results, columns)


def generate_scores(random_subjects, real_subjects, cohorts, bars, columns, random_file, real_file, view_type):
    generate_scores_generic(random_subjects, cohorts, bars, columns, "random", random_file, view_type)
    generate_scores_generic(real_subjects, cohorts, bars, columns, "real", real_file, view_type)


def show_average_scores(file, type):
    df = pd.read_csv(file)

    # Extract the columns
    psnr = df['psnr']
    sre = df['sre']
    ssim = df['ssim']
    fsim = df['fsim']

    # Calculate the average values
    average_psnr = psnr.mean()
    average_sre = sre.mean()
    average_ssim = ssim.mean()
    average_fsim = fsim.mean()

    # Print the results
    print(f"Type: {type}")
    print(f'Average PSNR: {average_psnr}')
    print(f'Average SRE: {average_sre}')
    print(f'Average SSIM: {average_ssim}')
    print(f'Average FSIM: {average_fsim}')


def statistical_analysis(random_file, real_file):
    show_average_scores(random_file, "random")
    show_average_scores(real_file, "real")


def single_result():
    pass
    # random_output = evaluation(org_img_path="paper_exp/random/random_subject1/645_3.png",
    #            pred_img_path="paper_exp/random/random_subject1/1400_3.png",
    #            metrics=metrics)
    # print(random_output)
    # 'psnr': 40.00895752370358, 'rmse': 0.009990011341869831, 'sre': 63.35158893972552,
    # 'ssim': 0.9587604728399599, 'fsim': 0.7689721855936194,
    # 'issm': 0.0, 'uiq': 0.20901964676025936,
    # 'sam': 0.0

    # real_output = evaluation(org_img_path="paper_exp/real/subject4/645_3.png",
    #                          pred_img_path="paper_exp/real/subject4/1400_3.png",
    #                          metrics=metrics)
    # print(real_output)
    # 'psnr': 42.072560640005, 'rmse': 0.007877141237258911, 'sre': 64.17829244746001,
    # 'ssim': 0.9713571870264152, 'fsim': 0.8343905128832961,
    # 'issm': 0.0, 'uiq': 0.2372536459209604,
    # 'sam': 0.0

    # real_output = evaluation(org_img_path="paper_exp/real/subject4/645_3.png",
    #            pred_img_path="paper_exp/real/subject4/645_3.png",
    #            metrics=metrics)
    # print(real_output)
    # 'psnr': inf, 'rmse': 0.0, 'sre': inf,
    # 'ssim': 1.0, 'fsim': 1.0,
    # 'issm': 0.0, 'uiq': 0.29169130980658087,
    # 'sam': 0.0


def crop_and_merge():
    combined_image_file = "paper_exp/survey_1/1.png"
    left_image_file = "paper_exp/survey_1/1_r_1_645_mid.png"
    right_image_file = "paper_exp/survey_1/1_r_1_2500_mid.png"
    left_image = cv2.imread(left_image_file)
    right_image = cv2.imread(right_image_file)
    x_start = 130
    y_start = 140
    crop_width = 350
    crop_height = 400
    cropped_left_image = left_image[y_start:y_start + crop_height, x_start:x_start + crop_width]
    cropped_right_image = right_image[y_start:y_start + crop_height, x_start:x_start + crop_width]
    # Combine the images horizontally (side by side)
    combined_image = cv2.hconcat([cropped_left_image, cropped_right_image])
    # Save the cropped image
    cv2.imwrite(combined_image_file, combined_image)
    print(f"Saved: {combined_image_file}")


def get_png_files(directory):
    png_files = {}
    for file in os.listdir(directory):
        if file.endswith(".png") or file.endswith(".PNG"):
            if file.count("_") == 4:
                serial = file.split("_")[0]
                file_path = os.path.join(directory, file)
                if serial in png_files:
                    png_files[serial].append(file_path)
                else:
                    png_files[serial] = [file_path]
    return png_files


def crop_and_merge_all(directory):
    files = get_png_files(directory)
    merge_count = 0
    for serial, images in files.items():
        if len(images) != 2:
            print(f"Error in serial {serial}. It has {len(images)} images. It should have only 2 images.")
            continue
        merge_image_directory = os.path.join(directory, "merged")
        if not os.path.exists(merge_image_directory):
            os.mkdir(merge_image_directory)
        combined_image_file = os.path.join(merge_image_directory, f"{serial}.png")
        left_image_file = images[0]
        right_image_file = images[1]
        left_image = cv2.imread(left_image_file)
        right_image = cv2.imread(right_image_file)
        x_start = 130
        y_start = 140
        crop_width = 350
        crop_height = 400
        cropped_left_image = left_image[y_start:y_start + crop_height, x_start:x_start + crop_width]
        cropped_right_image = right_image[y_start:y_start + crop_height, x_start:x_start + crop_width]
        # Combine the images horizontally (side by side)
        combined_image = cv2.hconcat([cropped_left_image, cropped_right_image])
        # Save the cropped image
        cv2.imwrite(combined_image_file, combined_image)
        print(f"Exported: {combined_image_file}")
        merge_count += 1
    print(f"\nExported total {merge_count} images in {merge_image_directory} directory")


if __name__ == "__main__":
    metrics = ["psnr", "sre", "ssim", "fsim"]
    random_subjects = [1, 2, 3, 4]
    real_subjects = [4, 31, 55, 189]
    cohorts = [645, 1400, 2500]
    bars = ["3", "first", "mid", "last"]
    columns = ["type", "subject", "bar", "cohort_1", "cohort_2"] + metrics
    view_type = "single"
    random_results_filename = f"random_results_{view_type}.csv"
    real_results_filename = f"real_results_{view_type}.csv"

    generate_scores(random_subjects, real_subjects, cohorts, bars, columns,
                    random_results_filename, real_results_filename, view_type)
    statistical_analysis(random_results_filename, real_results_filename)
    # survey_directory = "paper_exp/survey"
    # crop_and_merge_all(survey_directory)
