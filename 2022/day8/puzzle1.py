class Grid:
    def __init__(self, grid_list):
        self.y = len(grid_list)
        self.x = len(grid_list[0])
        self.grid = grid_list
        self.tree = 0

    @property
    def visible_trees(self):
        count = 0
        for y in range(0, self.y):
            for x in range(0, self.x):
                if self.is_visible(y, x):
                    count +=1
        return count

    @property
    def highest_score(self):
        high_score = 0
        for y in range(0, self.y):
            for x in range(0, self.x):
                high_score = max(self.scenic_score(y, x), high_score)
        return high_score

    def is_visible(self, y, x):
        self.tree = self.grid[y][x]
        if self._visible_north(y, x):
            return True
        if self._visible_south(y, x):
            return True
        if self._visible_east(y, x):
            return True
        if self._visible_west(y, x):
            return True
        return False

    def _visible_north(self, y, x):
        for num in range(y-1, -1, -1):
            if self.grid[num][x] >= self.tree:
                return False
        return True
    
    def _visible_south(self, y, x):
        for num in range(y+1, self.y):
            if self.grid[num][x] >= self.tree:
                return False
        return True
    
    def _visible_west(self, y, x):
        for num in range(x-1, -1, -1):
            if self.grid[y][num] >= self.tree:
                return False
        return True

    def _visible_east(self, y, x):
        for num in range(x+1, self.x):
            if self.grid[y][num] >= self.tree:
                return False
        return True

    def scenic_score(self, y, x):
        self.tree = self.grid[y][x]
        north = self._viewing_north(y, x)
        south = self._viewing_south(y, x)
        east = self._viewing_east(y, x)
        west = self._viewing_west(y, x)
        return north * south * east * west


    def _viewing_north(self, y, x):
        for num in range(y-1, -1, -1):
            if self.grid[num][x] >= self.tree:
                return y - num
        return y
    
    def _viewing_south(self, y, x):
        for num in range(y+1, self.y):
            if self.grid[num][x] >= self.tree:
                return num - y
        return self.y - y - 1
    
    def _viewing_west(self, y, x):
        for num in range(x-1, -1, -1):
            if self.grid[y][num] >= self.tree:
                return x - num
        return x

    def _viewing_east(self, y, x):
        for num in range(x+1, self.x):
            if self.grid[y][num] >= self.tree:
                return num - x
        return self.x - x - 1
    
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    grid = Grid(total_lines)
    print(grid.visible_trees)
    print(grid.highest_score)
