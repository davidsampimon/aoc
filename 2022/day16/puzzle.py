import time
import heapq

TOTAL_TIME = 30

class Valve:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.is_open = False
        self.step_map = {}

    @property
    def is_closed(self):
        return not self.is_open
    
    def open(self):
        self.is_open = True

    def set_flow(self, flow):
        self.flow = flow

    def set_child(self, child):
        self.children.append(child)

    def set_step_map(self, step_map):
        self.step_map = step_map

    def __repr__(self):
        return f"(Valve {self.name}, open={self.is_open}, flow={self.flow})"

    def __eq__(self, other):
        return str(self.name) == other

class Explorer:
    def __init__(self, data):
        self.data = data
        self.grid = self._grid_init()
        self._set_step_maps()

    def _grid_init(self):
        grid_dict = {}
        for valve in self.data:
            grid_dict[valve.name] = -1
        return grid_dict
        
    def _set_step_maps(self):
        for valve in self.data:
            self.grid = self._grid_init()
            self.calc_steps(valve)
            valve.set_step_map(self.grid)

    def calc_steps(self, valve, steps=0):
        if self.grid[valve.name] == -1:
            self.grid[valve.name] = steps
        for child in valve.children:
            if self.grid[child.name] < 0 or self.grid[child.name] > steps + 1:
                self.grid[child.name] = steps + 1
                self.calc_steps(child, steps+1)       

    def get_valve(self, valve_name):
        index = self.data.index(valve_name)
        return self.data[index]
    
    def valve_reset(self):
        for valve in self.data:
            valve.is_open = False
    
    def scores(self, grid, n, minutes):
        results = []
        for valve in self.data:
            steps = grid[valve.name]
            reduced_factor = TOTAL_TIME - (minutes + steps + 1)
            score = valve.flow * reduced_factor * valve.is_closed
            if score > 0:
                results.append((score, valve.name))
        return heapq.nlargest(n, results)
    
    def move(self, from_valve, valve, minutes):
        steps = from_valve.step_map[valve.name]
        minutes += steps
        minutes += 1
        return (minutes, valve.flow)

    def try_out(self, top_n, depth_n, route=(0, ["AA"]), minutes=0):
        if depth_n == 0:
            return route

        self.valve_reset()
        for valve_name in route[1]:
            visited_valve = self.get_valve(valve_name)
            visited_valve.open()
        
        from_valve = self.get_valve(route[1][-1])
        best_valves = self.scores(from_valve.step_map, top_n, minutes)
        if not best_valves:
            return route
        
        results = []
        for valve in best_valves:
            to_valve = self.get_valve(valve[1])
            path = (route[0] + valve[0], route[1] + [valve[1]])
            time_expired = self.move(from_valve, to_valve, minutes)[0]
            results.append(self.try_out(top_n, depth_n - 1, path, time_expired))
        return results

def parse_input(data):
    results = []
    with open(data, "r") as f:
        for line in f:
            line_list = line.strip().split()
            name = line_list[1]
            flow = parse_flow(line_list[4])
            children = [x.strip(",") for x in line_list[9:]]
            results = add_valve(name, results)
            results = add_flow(name, flow, results)
            for child in children:
                results = add_valve(child, results)
                results = add_child(name, child, results)
    return results            
            
def add_valve(name, valve_list):
    if name not in valve_list:
        valve_list.append(Valve(name))
    return valve_list

def add_flow(name, flow, valve_list):
    index = valve_list.index(name)
    valve_list[index].set_flow(flow)
    return valve_list

def add_child(name, child, valve_list):
    index = valve_list.index(name)
    child_index = valve_list.index(child)
    valve_list[index].set_child(valve_list[child_index])
    return valve_list

def parse_flow(flow_data):
    flow = flow_data.replace("rate=", "")
    flow = flow.replace(";", "")
    return (int(flow))

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

if __name__ == "__main__":

    # puzzle 1
    start_time = time.time()

    valve_list = parse_input("input.txt")
    explorer = Explorer(valve_list)
    print(f"Valves: {len(explorer.data)}")
    route_tree = explorer.try_out(15, 8)
    flat_results = flatten(route_tree)
    results = heapq.nlargest(1, flat_results)
    print(results[0])

    end_time = time.time()
    res = end_time - start_time
    print('Execution time:', res, 'seconds')
