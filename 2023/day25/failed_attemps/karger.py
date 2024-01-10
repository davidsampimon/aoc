from random import randint

def karger_min_cut(graph):
    while len(graph) > 2:
        v1, v2 = select_random_edge(graph)
        merge_vertices(graph, v1, v2)
        remove_self_loops(graph, v1)
    return len(list(graph.values())[0])

def select_random_edge(graph):
    v1 = list(graph.keys())[randint(0, len(graph) - 1)]
    v2 = graph[v1][randint(0, len(graph[v1]) - 1)]
    return v1, v2

def merge_vertices(graph, v1, v2):
    graph[v1].extend(graph[v2])
    for vertex in graph[v2]:
        if vertex in graph:
            if v2 in graph[vertex]:
                graph[vertex].remove(v2)
        graph[vertex].append(v1)
    del graph[v2]

def remove_self_loops(graph, vertex):
    graph[vertex] = [v for v in graph[vertex] if v != vertex]


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
            tmp[key].add(component)
            tmp[component].add(key)
    
    graph = {key: list(value) for key, value in tmp.items()}
    return graph

if __name__ == "__main__":
    graph = data("test.txt")
    
    results = list()
    count = 0
    while count < 1000:
        c_graph = graph.copy()
        cut = karger_min_cut(c_graph)
        if cut == 3:
            results.append(
                c_graph.copy()
            )
        count += 1
    pass