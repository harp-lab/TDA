import json

data = json.load(open("clusters_kmeans/clusters.json"))
total_matches = 0
total_subjects = 0
matches = []
mis_matches = []
total_distances = -0
for subject in data:
    dfc_2500, dfc_1400 = data[subject]
    if dfc_2500 == dfc_1400:
        total_matches += 1
        matches.append(subject)
    else:
        current_distance = abs(dfc_1400 - dfc_2500)
        total_distances += current_distance
        mis_matches.append(subject)
    total_subjects += 1

mean_distance = total_distances / total_subjects
print("Clustering Method: KMeans")
print("Best cluster selection using Silhouette Score in 2-15 range")
print(f"Total subjects: {total_subjects}")
print(f"Total matches: {total_matches}")
print(f"Total match percentage: {(total_matches / total_subjects) * 100:.2f}")
print(f"Mean mismatch distance: {mean_distance:.2f}")
# print(f"Matched cluster subjects: {matches}")
# print(f"Mismatched cluster subjects: {mis_matches}")
