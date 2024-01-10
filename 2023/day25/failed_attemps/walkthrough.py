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

    graph = dict()

    for component in components:
        graph[component] = set()

    for key, connects in connections.items():
        for component in connects:
            graph[key].add(component)
            graph[component].add(key)

    return Graph(graph)


class Graph:
    def __init__(self, graph):
        self.nodes = set(graph.keys())
        self.edges = graph

    def wire_count(self, key):
        return len(self.edges[key] - self.nodes)

    def count_all(self):
        return sum(
            [self.wire_count(node) for node in self.edges]
        )


if __name__ == "__main__":
    graph = data("test.txt")
    org_nodes = graph.nodes.copy()

    while graph.count_all() != 3:
        print(graph.count_all())
        graph.nodes.remove(max(graph.nodes, key=graph.wire_count))

    answer = len(graph.nodes) * len(org_nodes - graph.nodes)
    print(f"Answer 1: {answer}")
