from collections import namedtuple

Point = namedtuple("Point", "y x")


def neighbours(pos):
    y, x = pos
    return [
        Point(y, x+1),
        Point(y+1, x),
        Point(y, x-1),
        Point(y-1, x)
    ]


class Node:
    def __init__(self, pos, links):
        self.pos = pos
        self.links = links

    def __repr__(self):
        return f"{self.pos}: {self.links}"


def get_nodes(grid):
    nodes = dict()
    for pos in grid.keys():
        nbs = dict()
        for nb in neighbours(pos):
            if nb in grid:
                nbs[nb] = 1
        nodes[pos] = Node(pos, nbs)
    return nodes


def merge_hallways(nodes):
    remove_list = list()
    for pos, node in nodes.items():
        if len(node.links) == 2:
            remove_list.append(pos)
            nbs = list(node.links.keys())
            left = nbs.pop()
            right = nbs.pop()
            steps_to_left = node.links[left]
            steps_to_right = node.links[right]
            nodes[left].links[right] = steps_to_left + steps_to_right
            nodes[right].links[left] = steps_to_left + steps_to_right
            del nodes[left].links[pos]
            del nodes[right].links[pos]

    for pos in remove_list:
        del nodes[pos]
    return nodes


def walk(nodes, pos, end, count=0, visited=None):
    if visited is None:
        visited = list()

    if pos == end:
        return count

    visited.append(pos)
    node = nodes[pos]

    result = [0]
    nbs = [nb for nb in node.links if nb not in visited]

    for nb in nbs:
        result.append(
            walk(nodes, nb, end, count + node.links[nb], visited.copy())
        )
    return max(result)


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    height = len(lines)

    grid = dict()
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol in ".>v":
                grid[Point(y, x)] = "."
            if y == 0 and symbol == ".":
                start = Point(y, x)
            if y == height - 1 and symbol == ".":
                end = Point(y, x)

    return grid, start, end


if __name__ == "__main__":
    grid, start, end = data("input.txt")

    nodes = get_nodes(grid)
    nodes = merge_hallways(nodes)
    answer = walk(nodes, start, end)
    print(f"Answer 2: {answer}")
