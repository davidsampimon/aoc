import random, copy



def data(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()
    
    components = set()
    connections = dict()
    graph = dict()
    for line in lines:
        key, connects_l = line.split(":")
        connects = connects_l.split()
        connections[key] = connects
        components.add(key)
        components.update(connects)
   
    graph = dict()

    for component in components:
        graph[component] = set()

    for key, connects in connections.items():
        for component in connects:
            graph[key].add(component)
            graph[component].add(key)

    return {key: list(value) for key, value in graph.items()}


def choose_random_key(graph):
    v1 = random.choice(list(graph.keys()))
    v2 = random.choice(list(graph[v1]))
    return v1, v2

def karger(graph):
    length = []
    while len(graph) > 2:
        v1, v2 = choose_random_key(graph)
        graph[v1].extend(graph[v2])
        for x in graph[v2]:
            graph[x].remove(v2)
            graph[x].append(v1) 
        while v1 in graph[v1]:
            graph[v1].remove(v1)
        del graph[v2]
    for key in graph.keys():
        length.append(len(graph[key]))
    return length[0]

def operation(n):
    i = 0
    count = 10000   
    while i < n:
        data = copy.deepcopy(G)
        min_cut = karger(data)
        if min_cut < count:
            count = min_cut
        i = i + 1
    return count


# print(operation(100))


if __name__ == "__main__":
    graph = data("input.txt")
    min_cut = 10
    while min_cut != 3:
        contracted_graph = copy.deepcopy(graph)
        min_cut = karger(contracted_graph)
    print(min_cut)
    side = sum(len(edges) for edges in contracted_graph.values())
    answer = side * (len(graph) - side)
    print(answer)

