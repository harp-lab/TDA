import numpy as np
import matplotlib.pyplot as plt


def get_dataset():
    return np.array([[0, 2], [2, 2], [1, 0], [1.5, -3.0]])


def get_axis(points, padding=2):
    x_values = points[:, 0]
    y_values = points[:, 1]
    min_x = min(x_values) - padding
    max_x = max(x_values) + padding
    min_y = min(y_values) - padding
    max_y = max(y_values) + padding
    return [min_x, max_x, min_y, max_y]


def get_neighbor_graph(points, eps):
    # nodes as index : 0, 1, 2, ..., points.length
    number_of_points = points.shape[0]
    nodes = [i for i in range(number_of_points)]
    edges = []
    # arrays to store distances between two points
    distances = []
    # distance diameter
    for i in range(number_of_points):
        for j in range(i + 1, number_of_points):
            point_1 = points[i]
            point_2 = points[j]
            distance = np.linalg.norm(point_1 - point_2)
            if distance <= eps:
                distances.append([len(edges), distance])
                edges.append({i, j})
    return nodes, edges, distances


def get_lower_neighbors(nodes, edges, node):
    return {
        i for i in nodes if {i, node} in edges and node > i
    }


def get_simplices(nodes, edges, k):
    simplices = []
    # insert 0-simplices: nodes
    for i in nodes:
        simplices.append({i})
    # insert 1-simplices: edges
    for edge in edges:
        simplices.append(edge)
    # insert n-simplices
    for i in range(k):
        # Skip 0-simplices
        for simplex in [x for x in simplices if len(x) == i + 2]:
            lower_neighbors = []
            for z in simplex:
                lower_neighbors.append(get_lower_neighbors(nodes, edges, z))
            neighbors = set.intersection(*lower_neighbors)
            for neighbor in neighbors:
                simplices.append(set.union(simplex, {neighbor}))
        return simplices


def draw_simplices(simplices, points):
    plt.clf()
    axis = get_axis(points)
    plt.axis(axis)

    # Plot the points in the graph
    plt.scatter(points[:, 0], points[:, 1])

    # Add labels to the points
    for i in range(points.shape[0]):
        label = "{} ({}, {})".format(i, points[i][0], points[i][1])
        plt.annotate(label, (points[i][0] + 0.1, points[i][1] - 0.1))

    # Draw the edges
    for edge in filter(lambda x: len(x) == 2, simplices):
        edge_points = [points[i] for i in edge]
        line = plt.Polygon(edge_points, closed=False, fill=None,
                           edgecolor='r')
        plt.gca().add_line(line)

    # Draw the triangle
    for triangle in filter(lambda x: len(x) == 3, simplices):
        triangle_points = [points[i] for i in triangle]
        line = plt.Polygon(triangle_points, closed=True, fill=True, color='b',
                           alpha=0.2)
        plt.gca().add_line(line)

    plt.show()


def reduce_matrix(matrix):
    # Returns [reduced_matrix, rank, nullity]
    if np.size(matrix) == 0:
        return [matrix, 0, 0]
    m = matrix.shape[0]
    n = matrix.shape[1]

    def _reduce(x):
        # We recurse through the diagonal entries.
        # We move a 1 to the diagonal entry, then
        # knock out any other 1s in the same  col/row.
        # The rank is the number of nonzero pivots,
        # so when we run out of nonzero diagonal entries, we will
        # know the rank.
        nonzero = False
        # Searching for a nonzero entry then moving it to the diagonal.
        for i in range(x, m):
            for j in range(x, n):
                if matrix[i, j] == 1:
                    matrix[[x, i], :] = matrix[[i, x], :]
                    matrix[:, [x, j]] = matrix[:, [j, x]]
                    nonzero = True
                    break
            if nonzero:
                break
        # Knocking out other nonzero entries.
        if nonzero:
            for i in range(x + 1, m):
                if matrix[i, x] == 1:
                    matrix[i, :] = np.logical_xor(matrix[x, :], matrix[i, :])
            for i in range(x + 1, n):
                if matrix[x, i] == 1:
                    matrix[:, i] = np.logical_xor(matrix[:, x], matrix[:, i])
            # Proceeding to next diagonal entry.
            return _reduce(x + 1)
        else:
            # Run out of nonzero entries so done.
            return x

    rank = _reduce(0)
    return [matrix, rank, n - rank]


def get_n_simplices(simplices, n):
    chains = []
    for simplex in simplices:
        if len(simplex) == n + 1:
            chains.append(simplex)
    if len(chains) == 0:
        chains = [0]
    return chains


def is_face(face, simplex):
    if simplex == 0 or set(face) < set(simplex):
        return 1
    return 0


def get_boundary_matrix(n_chain, p_chain):
    boundary_matrix = np.zeros((len(n_chain), len(p_chain)))
    for i, n_simplex in enumerate(n_chain):
        for j, p_simplex in enumerate(p_chain):
            boundary_matrix[i, j] = is_face(p_simplex, n_simplex)
    return boundary_matrix.T


def get_betti_number(simplices):
    maximum_dimension = len(max(simplices, key=len))
    betti = np.zeros(maximum_dimension)



if __name__ == "__main__":
    point_cloud = get_dataset()
    # for i in np.arange(1, 3.5, 0.2):
    i = 3.1
    epsilon = round(i, 2)
    node_list, edge_set, distance_list = get_neighbor_graph(point_cloud,
                                                            epsilon)
    rips_simplices = get_simplices(node_list, edge_set, 3)
    # print("Epsilon: ", epsilon)
    # print("Edges: ", edge_set)
    # print("Simplices: ", rips_simplices)
    # print("")
    print(rips_simplices)
    c_0 = get_n_simplices(rips_simplices, 0)
    c_1 = get_n_simplices(rips_simplices, 1)
    c_2 = get_n_simplices(rips_simplices, 2)
    b_1 = get_boundary_matrix(c_1, c_0)
    snf_1 = reduce_matrix(b_1)
    print(snf_1)
    b_2 = get_boundary_matrix(c_2, c_1)
    snf_2 = reduce_matrix(b_2)
    print(snf_2)
