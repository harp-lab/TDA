import dionysus as d
from utils import get_dataset, get_simplices

# # simplices = [
# #     ([0], 0),
# #     ([1], 0),
# #     ([2], 0),
# #     ([3], 0),
# #     ([4], 0),
# #     ([5], 0),
# #     ([0, 1], 1.2), ([0, 2], 5), ([0, 4], 1.2),
# #     ([1, 4], 2),
# #     ([2, 3], 0.5), ([2, 4], 3.3),
# #     ([4, 5], 2.5)
# # ]
#
# simplices = [([0], 0), ([0, 1], 1.2), ([0, 2], 4.5), ([0, 3], 5.0),
#              ([0, 4], 1.2), ([0, 5], 3.7), ([1], 0), ([1, 2], 5.3),
#              ([1, 3], 5.8), ([1, 4], 2.0), ([1, 5], 4.5), ([2], 0),
#              ([2, 3], 0.5), ([2, 4], 3.3), ([2, 5], 5.8), ([3], 0),
#              ([3, 4], 3.3), ([3, 5], 6.3), ([4], 0), ([4, 5], 2.5), ([5], 0)]

matrix = get_dataset("dataset_20_20.csv")
simplices = get_simplices(matrix)

f = d.Filtration()

for vertices, distance in simplices:
    f.append(d.Simplex(vertices, distance))

f.sort()

m = d.homology_persistence(f)
dgms = d.init_diagrams(m, f)
#
# for i, dgm in enumerate(dgms):
#     if i == 1:
#         for pt in dgm:
#             print(i, pt.birth, pt.death)


for i, dgm in enumerate(dgms):
    # if i == 1:
    for pt in dgm:
        print(i, pt.birth, pt.death)
