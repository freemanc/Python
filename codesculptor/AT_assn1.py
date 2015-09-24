"""
Three Functions related to in-degree computation
"""

# Define 3 digraph-constants for testing purpose
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 
5: set([2]), 6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3, 7]), 3: set([7]), 4: set([1]), 
5: set([2]), 6: set([]), 7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
    Function outputs a complete digraph, where the number of nodes is the input
    """
    output = {}
    if num_nodes > 0:
        for node in range(num_nodes):
            in_neighbor = set(range(num_nodes))
            in_neighbor.remove(node)
            output[node] = in_neighbor
    return output

def compute_in_degrees(digraph):
    """
    Computes the in-degrees of each node for the given digraph
    """
    output = {}
    for node, out_neighbors in digraph.items():
        output[node] = output.get(node, 0)
        for nbr in out_neighbors:
            output[nbr] = output.get(nbr, 0) + 1
    return output

def in_degree_distribution(digraph):
    """
    Computes the unnormalized in-degree distribution of the given digraph
    """
    output = {}
    in_degree = compute_in_degrees(digraph)
    for in_degree in in_degree.values():
        output[in_degree] = output.get(in_degree, 0) + 1
    return output