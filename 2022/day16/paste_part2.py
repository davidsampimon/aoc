## solution copied from https://github.com/hyper-neutrino/advent-of-code
from collections import deque


def parse_input(input_file):
    valves = {}
    tunnels = {}

    for line in open(input_file):
        line = line.strip()
        valve = line.split()[1]
        flow = int(line.split(";")[0].split("=")[1])
        targets = line.split("to ")[1].split(" ", 1)[1].split(", ")
        valves[valve] = flow
        tunnels[valve] = targets
    
    return valves, tunnels


class Explorer:
    def __init__(self, valves, tunnels):
        self.distances, self.nonempty = self.set_distance_nonempty(
            valves,
            tunnels
        )
        self.indices = self.set_indices(self.nonempty)

    def set_indices(self, nonempty):
        indices = {}

        for index, element in enumerate(nonempty):
            indices[element] = index
        
        return indices

    def set_distance_nonempty(self, valves, tunnels):
        dists = {}
        nonempty = []

        for valve in valves:
            if valve != "AA" and not valves[valve]:
                continue
            
            if valve != "AA":
                nonempty.append(valve)

            dists[valve] = {valve: 0, "AA": 0}
            visited = {valve}
            
            queue = deque([(0, valve)])
            
            while queue:
                distance, position = queue.popleft()
                for neighbor in tunnels[position]:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    if valves[neighbor]:
                        dists[valve][neighbor] = distance + 1
                    queue.append((distance + 1, neighbor))

            del dists[valve][valve]
            if valve != "AA":
                del dists[valve]["AA"]

        return dists, nonempty


    def dfs(self, time, valve, bitmask):
        cache = {}
        if (time, valve, bitmask) in cache:
            return cache[(time, valve, bitmask)]
        
        maxval = 0
        for neighbor in self.distances[valve]:
            bit = 1 << self.indices[neighbor]
            if bitmask & bit:
                continue
            remtime = time - self.distances[valve][neighbor] - 1
            if remtime <= 0:
                continue
            maxval = max(maxval, self.dfs(remtime, neighbor, bitmask | bit) + valves[neighbor] * remtime)
            
        cache[(time, valve, bitmask)] = maxval
        return maxval


if __name__ == "__main__":
    valves, tunnels = parse_input("test.txt")
    explorer = Explorer(valves, tunnels)
    
    bitmask = (1 << len(explorer.nonempty)) - 1
    max_flow = 0
    for i in range((bitmask + 1) // 2):
        max_flow = max(
            max_flow,
            explorer.dfs(26, "AA", i) + explorer.dfs(26, "AA", bitmask ^ i)
        )
    print(max_flow)

