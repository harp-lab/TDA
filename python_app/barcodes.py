def get_unique_distances(matrix):
    return list(sorted(set([j for row in matrix for j in row])))


def get_number_of_components(matrix, min_distance):
    v = len(matrix[0])
    group = 0
    seen = set()
    for i in range(v):
        if i not in seen:
            visited = [False for _ in range(v)]
            start_node = i
            q = [start_node]
            visited[start_node] = True
            while len(q) != 0:
                current = q.pop(0)
                seen.add(current)
                for node in range(v):
                    if visited[node] is False and matrix[current][node] <= min_distance:
                        q.append(node)
                        visited[node] = True
            group += 1
    return group


def get_barcodes(matrix, max_val=None):
    unique_distances = get_unique_distances(matrix)
    barcodes = list()
    number_of_components = None
    for distance in unique_distances:
        components = get_number_of_components(matrix, distance)
        if components == 1:
            barcodes.append([0, distance])
            break
        if number_of_components is None:
            number_of_components = components
            continue
        if components < number_of_components:
            for i in range(number_of_components - components):
                barcodes.append([0, distance])
            number_of_components = components
    remaining_bars = len(matrix[0]) - len(barcodes)
    if max_val is None:
        max_val = max(unique_distances)
    for i in range(remaining_bars):
        barcodes.append([0, max_val])
    barcodes = sorted(barcodes, key=lambda x: x[1], reverse=True)
    return barcodes
