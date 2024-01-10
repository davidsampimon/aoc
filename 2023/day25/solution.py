#  from https://gitlab.com/0xdf/aoc2023/-/blob/main/day25/day25.py?ref_type=heads
import networkx as nx


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    graph = nx.Graph()
    for line in lines:
        left, right = line.split(": ")
        for node in right.split():
            graph.add_edge(left, node)
    return graph


if __name__ == "__main__":
    graph = data("input.txt")
    cut_value, partition = nx.stoer_wagner(graph)

    answer = len(partition[0]) * len(partition[1])
    print(f"Answer 1: {answer}")
