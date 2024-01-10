

def data(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    
    components = set()
    connections = dict()

    for line in lines:
        key, connects_l = line.split(":")
        connects = connects_l.split()
        connections[key] = connects
        components.add(key)
        components.update(connects)
    
    tmp = dict()

    for component in components:
        tmp[component] = set()

    for key, connects in connections.items():
        for component in connects:
            tmp[key].add((component, 1))
            tmp[component].add((key, 1))
    
    
    graph = {key: list(value) for key, value in tmp.items()}
    return graph



def stoer_wagner(G, cut_value = float("inf")):
    """
    Returns the weighted minimum edge cut using the Stoer-Wagner algorithm.
    Determine the minimum edge cut of a connected graph using the Stoer-Wagner algorithm.
    In weighted cases, all weights must be nonnegative.

    Parameters:
    G (dict): A dictionary representing the graph. The keys are the nodes and the values are lists of tuples representing the edges and their weights.

    Returns:
    cut_value (integer or float): The sum of weights of edges in a minimum cut.
    partition (pair of node lists): A partitioning of the nodes that defines a minimum cut.

    Raises:
    ValueError: If the graph has less than two nodes, is not connected or has a negative-weighted edge.

    Examples:
    >>> G = {'x': [('a', 3), ('b', 1)], 'a': [('x', 3), ('c', 3)], 'b': [('x', 1), ('c', 5), ('d', 4)], 'c': [('a', 3), ('b', 5), ('y', 2)], 'd': [('b', 4), ('e', 2)], 'e': [('d', 2), ('y', 3)], 'y': [('c', 2), ('e', 3)]}
    >>> cut_value, partition = stoer_wagner(G)
    >>> cut_value
    4
    >>> partition
    (['x', 'a', 'c'], ['b', 'd', 'e', 'y'])
    """
    nodes = list(G.keys())
    n = len(nodes)
    if n == 2:
        return G, cut_value
    if n < 2:
        raise ValueError("Graph must have at least two nodes.")
    for node in nodes:
        if len(G[node]) == 0:
            raise ValueError("Graph must be connected.")
        for edge in G[node]:
            if edge[1] < 0:
                raise ValueError("Graph must have non-negative edge weights.")
    partition = ([nodes[0]], nodes[1:])
    for i in range(n - 1):
        A = partition[0]
        B = partition[1]
        d = {node: 0 for node in nodes}
        for node in B:
            for edge in G[node]:
                if edge[0] in A:
                    d[node] += edge[1]
        u = B[0]
        for node in B:
            if d[node] > d[u]:
                u = node
        cut_value = min(cut_value, d[u])
        A.append(u)
        B.remove(u)
        for node in B:
            for edge in G[node]:
                if edge[0] == u:
                    edge_weight = edge[1]
                    G[node].remove(edge)
                    G[A[-1]].append((node, edge_weight))
                    G[node].append((A[-1], edge_weight))
    return stoer_wagner(partition, cut_value)



if __name__ == "__main__":
    graph = data("input.txt")
    partition, cut = stoer_wagner(graph)
    breakpoint()
    pass