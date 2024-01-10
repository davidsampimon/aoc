class RopeEnd():
    def __init__(self, name, start_pos=(0, 0), child=None):
        self.name = str(name)
        self.position = start_pos
        self.history = [start_pos]
        self.child = child

    def __repr__(self):
        return self.name

    def _new_pos(self, pos):
        self.position = pos
        self.history.append(pos)
        if self.child:
            self.child.track_parent(pos)

    @property
    def unique_positions(self):
        return len(set(self.history))

    def move_right(self):
        y, x = self.position
        self._new_pos((y, x+1))
        
    def move_left(self):
        y, x = self.position
        self._new_pos((y, x-1))

    def move_up(self):
        y, x = self.position
        self._new_pos((y+1, x))
    
    def move_down(self):
        y, x = self.position
        self._new_pos((y-1, x))
    
    def track_parent(self, pos):
        y_diff = pos[0] - self.position[0]
        x_diff = pos[1] - self.position[1]
        if abs(y_diff) > 1 and abs(x_diff) > 1:
            new_y = (pos[0] + self.position[0])//2
            new_x = (pos[1] + self.position[1])//2
            self._new_pos((new_y, new_x))
        elif abs(y_diff) > 1:
            new_y = (pos[0] + self.position[0])//2
            new_x = pos[1]
            self._new_pos((new_y, new_x))
        elif abs(x_diff) > 1:
            new_x = (pos[1] + self.position[1])//2
            new_y = pos[0]
            self._new_pos((new_y, new_x))

def draw(knots_dict):
    print(f"0: {knots_dict[0].position}. 1: {knots_dict[1].position}. 2: {knots_dict[2].position}. 3: {knots_dict[3].position}. 4: {knots_dict[4].position}")
    print(f"5: {knots_dict[5].position}. 6: {knots_dict[6].position}. 7: {knots_dict[7].position}. 8: {knots_dict[8].position}. 9: {knots_dict[9].position}.")
    draw_dict = {}
    keys = knot_dict.keys()
    max_y = 0
    min_y = 0
    max_x = 0
    min_x = 0
    for key in keys:
        coord = knot_dict[key].position
        max_y = max(max_y, coord[0])
        min_y = min(min_y, coord[0])
        max_x = max(max_x, coord[1])
        min_x = min(min_x, coord[1])
        draw_dict[coord] = key
    
    offset_y = min_y
    offset_x = min_x
    grid_y = max_y - offset_y
    grid_x = max_x - offset_x
    for y in reversed(range(0, grid_y + 1)):
        for x in range(0, grid_x + 1):
            try:
                print(draw_dict[(y + offset_y, x + offset_x)], end="")
            except:
                print(".", end="")
        print()

 
if __name__ == "__main__":
    knot_dict = {}
    knots = 10
    draw_lines = 40
    
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    for num in range(knots-1, -1, -1):
        if num == knots-1:
            knot_dict[num] = RopeEnd(num)
        else:
            knot_dict[num] = RopeEnd(num, child=knot_dict[num+1])

    for index, row in enumerate(total_lines):
        if index < draw_lines:
            print(f"#########Line: {index}############")
            draw(knot_dict)
        cmd, total = row.split()
        total = int(total)
        match cmd:
            case "R":
                for _ in range(0, total):
                    knot_dict[0].move_right()
            case "L":
                for _ in range(0, total):
                    knot_dict[0].move_left()
            case "D":
                for _ in range(0, total):
                    knot_dict[0].move_down()
            case "U":
                for _ in range(0, total):
                    knot_dict[0].move_up()
    print("Answer puzzle2")
    print(knot_dict[knots-1].unique_positions)
