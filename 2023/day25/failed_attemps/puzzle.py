import random


class Edge:
    def __init__(source, dest):
        self.source = source
        self.destination = dest

    def __repr__(self):
        return f"{self.source} to {self.destination}"


class Graph:
    def __init__(self, graph):
        self.graph = graph

    def get(self, vertice):
        if vertice in self._map:
            return self.get(self._map[vertice])
        else:
            return vertice, self.graph[vertice]

    def merge(self, source, sink):
        source, source_edges = self.contracted_graph(source)
        sink, sink_edges = self.contracted_graph(sink)
        self.contracted_graph[source].update(sink_edges)
        if source in self.contracted_graph[source]:
            self.contracted_graph[source].remove(source)
        if sink in self.contracted_graph[source]:
            self.contracted_graph[source].remove(source)
        self.contracted_graph[source].remove(sink)
        del self.contracted_graph[sink]
        self._map[sink] = source
    
    def karger(self):
        """
        Karger's min cut algorithm. From
        https://www.geeksforgeeks.org/introduction-and-implementation-of-kargers-algorithm-for-minimum-cut/
        """
        # 1)  Initialize contracted graph CG as copy of original graph
        self.contracted_graph = graph.graph.copy()
        # 2)  While there are more than 2 vertices.
        while len(self.contracted_graph) > 2:
            #    a) Pick a random edge (u, v) in the contracted graph.
            source = random.choice(list(self.contracted_graph))
            sink = random.choice(list(self.contracted_graph))
            if source == sink:
                continue
            #    b) Merge (or contract) u and v into a single vertex (update 
            #        the contracted graph)
            self.merge(source, sink)
            #    c) Remove self-loops
            
        # 3) Return cut represented by two vertices.
        return self.contracted_graph



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
    
    return components, connections


if __name__ == "__main__":
    components, connections = data("test.txt")
    assert len(components) == 15
    all_connections = dict()

    for component in components:
        all_connections[component] = set()

    for key, connects in connections.items():
        for component in connects:
            all_connections[key].add(component)
            all_connections[component].add(key)

    graph = Graph(all_connections)
    cuts = graph.karger()
    pass
