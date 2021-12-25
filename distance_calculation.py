import sys
import numpy as np
import networkx as nx
from scipy.stats import wasserstein_distance


def get_1_wasserstein_distance(pd_1, pd_2):
    return wasserstein_distance([ar[1] for ar in pd_1],
                                [ar[1] for ar in pd_2])


def get_wasserstein_distance(persis1, persis2, p=1):
    # compute the p-Wasserstein distance for 2 persistence diagrams by finding maximal matching,
    # then matching all un-matched vertices to the closest point on the diagonal, then adding up all L-infinity distances between matched vertices
    # first turn persistence diagrams into a bipartite graph, nodes are (birth,death) tuples of only H1 (loop) structures
    bg = nx.Graph()
    persis1nodes = [(pers[0], pers[1]) for pers in persis1]
    persis2nodes = [(pers[0], pers[1]) for pers in persis2]
    # print("nodes")
    # print(persis1nodes, persis2nodes)
    bg.add_nodes_from(persis1nodes, bipartite=0)
    bg.add_nodes_from(persis2nodes, bipartite=1)
    # add all edges w/ edge weight (l inf norm)
    edgelist = []
    for node1 in persis1nodes:
        for node2 in persis2nodes:
            edgelist.append((node1, node2,
                             np.linalg.norm(np.array(node1) - np.array(node2),
                                            ord=np.inf)))
    bg.add_weighted_edges_from(edgelist)
    if not nx.is_connected(bg):
        print('something went wrong, graph is not connected')
        sys.exit()
    maxmatch = nx.bipartite.maximum_matching(bg)
    # maxmatch = nx.hopcroft_karp_matching(bg)
    # print('done with max matching')
    # add in matching to diagonal if node wasn't matched
    for idx, node in enumerate(persis1nodes + persis2nodes):
        if node not in maxmatch:
            diagmatch = (0.5 * (node[0] + node[1]), 0.5 * (node[0] + node[1]))
            maxmatch[node] = diagmatch
            maxmatch[diagmatch] = node
            if idx < len(persis1nodes):
                bipart = 1
            else:
                bipart = 0
            bg.add_node(diagmatch, bipartite=bipart)
            bg.add_edge(node, diagmatch, weight=np.linalg.norm(
                np.array(node) - np.array(diagmatch), ord=np.inf))
    # now add up all distances from maxmatch and divide by 2 (matching dictionary includes each edge twice)
    dist = 0
    for node1, node2 in maxmatch.iteritems():
        dist += (bg.edge[node1][node2]['weight']) ** p
    dist = (dist / 2) / (len(maxmatch) / 2)
    return dist
