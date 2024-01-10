import heapq
from collections import deque


class Position:
    def __init__(self, coord):
        self.y = coord[0]
        self.x = coord[1]

    @property
    def neighbors(self):
        y = self.y
        x = self.x
        # north, east, south, west
        return [
            Position((y-1, x)),
            Position((y, x+1)),
            Position((y+1, x)),
            Position((y, x-1))
        ]
    
    def __repr__(self):
        return f"{self.y} x {self.x}"


class Maze:
    def __init__(self, total_rows):
        self.map = total_rows
        self.grid_y = len(total_rows)
        self.grid_x = len(total_rows[0])

    def find_neighbors(self, pos):
        possible_neighbors = []
        for neighbor in pos.neighbors:
            if self._check_move(pos, neighbor):
                possible_neighbors.append(neighbor)
        return possible_neighbors
    
    def _contains(self, pos):
        if 0 <= pos.y < self.grid_y:
            if 0 <= pos.x < self.grid_x:
                return True
        return False
    
    def _check_move(self, from_pos, to_pos):
        if self._contains(to_pos):
            from_height = self.map[from_pos.y][from_pos.x]
            to_height = self.map[to_pos.y][to_pos.x]
            if from_height == "S":
                from_height = "a"
            if to_height == "E":
                to_height = "z"
            return ord(to_height) <= (ord(from_height) + 1)
        return False
    
    def find_character(self, character):
        results = []
        for y in range(0, self.grid_y):
            for x in range(0, self.grid_x):
                if self.map[y][x] == character:
                    results.append(Position((y, x)))
        if len(results) == 1:
            return results[0]
        return results

class Explorer:
    def __init__(self, maze, start_pos):
        self.map = maze
        self.start = start_pos
        self.distances = [[]]
        self._init_distances()
        self.exploration_queue = deque()
        self.exploration_queue.append(start_pos)

    def _init_distances(self):
        self.distances = [
            [-1 for x in range(self.map.grid_x)] for y in range(self.map.grid_y)
            ]
        self.distances[self.start.y][self.start.x] = 0
    
    @property
    def is_exploring(self):
        return len(self.exploration_queue) > 0

    def exploring(self):
        if len(self.exploration_queue) == 0:
            return "Nothing left to explore!"
        return self.exploration_queue.popleft()


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    maze = Maze(total_lines)
    start_pos = maze.find_character("S")
    end_pos = maze.find_character("E")

    # Puzzle 1
    explorer = Explorer(maze, start_pos)
    while explorer.is_exploring:
        pos = explorer.exploring()
        steps = explorer.distances[pos.y][pos.x]
        options = explorer.map.find_neighbors(pos)
        for option in options:
            if explorer.distances[option.y][option.x] == -1:
                explorer.distances[option.y][option.x] = steps + 1
                explorer.exploration_queue.append(option)
    
    answer = explorer.distances[end_pos.y][end_pos.x]
    print(answer)

    ## Puzzle 2
    list_a = maze.find_character("a")
    results = []

    for start_pos in list_a:
        explorer = Explorer(maze, start_pos)
        while explorer.is_exploring:
            pos = explorer.exploring()
            steps = explorer.distances[pos.y][pos.x]
            options = explorer.map.find_neighbors(pos)
            for option in options:
                if explorer.distances[option.y][option.x] == -1:
                    explorer.distances[option.y][option.x] = steps + 1
                    explorer.exploration_queue.append(option)
        if explorer.distances[end_pos.y][end_pos.x] > -1:
            heapq.heappush(results, explorer.distances[end_pos.y][end_pos.x])
    print(heapq.heappop(results))



