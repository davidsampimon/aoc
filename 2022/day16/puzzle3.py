import time
import heapq
from copy import deepcopy

from day18.puzzle import flatten, parse_input

TOTAL_TIME = 26


class Player:
    def __init__(self, name, start_pos):
        self.name = name
        self.pos = start_pos
        self.task_end = 0
    
    def busy(self, minute):
        return self.task_end > minute

    def __repr__(self):
        return f"{self.name}@{self.pos}"


class Explorer:
    def __init__(self, data, players):
        self.data = data
        self.grid = self._grid_init()
        self._set_step_maps()
        self.players = players
        self._set_pos()
        self.all_paths = set()

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

    def _set_pos(self):
        for player in self.players:
            player.pos = self.get_valve(player.pos)

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
    
    def _paths(self, route, p1_best, p2_best):
        paths = []
        for p1_score in p1_best:
            for p2_score in p2_best:
                if p1_score == p2_score:
                    score = p1_score[0] + 0
                else:
                    score = p1_score[0] + p2_score[0]
                paths.append(
                    (
                        route[0] + score,
                        route[1] + [(p1_score[1], p2_score[1])]
                    )
                )
        tuple_paths = [(path[0], tuple(path[1])) for path in paths]
        return tuple_paths

    def update_pos(self, players, path, minutes):
        p1_to = self.get_valve(path[1][-1][0])
        p2_to = self.get_valve(path[1][-1][1])
        if p1_to != players[0].pos:
            players[0].task_end = self.move(
                players[0].pos,
                p1_to,
                minutes
            )[0]
            players[0].pos = p1_to
                
        if p2_to != players[1].pos:
            players[1].task_end = self.move(
                players[1].pos,
                p1_to,
                minutes
            )[0]
            players[1].pos = p2_to

    def discover(
        self,
        players,
        top_n, 
        depth_n, 
        route=(0, [("AA", "AA")]), 
        minutes=0,
    ):
        if depth_n == 0 or minutes >= TOTAL_TIME:
            return route


        self.valve_reset()
        for valve_tuple in route[1]:
            for valve_name in valve_tuple:
                visited_valve = self.get_valve(valve_name)
                visited_valve.open()
        
        results = []
        if players[0].busy(minutes) and players[1].busy(minutes):
            return self.discover(players, top_n, depth_n-1, route, minutes+1)

        if not players[0].busy(minutes):
            p1_best = self.scores(players[0].pos.step_map, top_n, minutes)
        else:
            p1_best = [(0, players[0].pos.name)]

        if not players[1].busy(minutes):
            p2_best = self.scores(players[1].pos.step_map, top_n, minutes)
        else:
            p2_best = [(0, players[1].pos.name)]
                
        if p1_best == [] and p2_best == []:
            return route
        
        paths = self._paths(route, p1_best, p2_best)
        breakpoint()
        for path in paths:
            if path[1][-1][0] == path[1][-1][1]:
                continue
            self.all_paths.add(path)
            self.update_pos(players, path, minutes)
            self.discover(players, top_n, depth_n-1, path, minutes+1)
            
        return results


if __name__ == "__main__":
    valve_list = parse_input("test.txt")
    human = Player("Alex", "AA")
    elephant = Player("Dumbo", "AA")

    # puzzle 2
    start_time = time.time()
    explorer = Explorer(valve_list, (human, elephant))
    breakpoint()
    print(f"Valves: {len(explorer.data)}")
    route_tree = explorer.discover(explorer.players, 10, 30)
    breakpoint()
    flat_results = flatten(route_tree)
    results = heapq.nlargest(1, flat_results)
    print(results[0])

    end_time = time.time()
    res = end_time - start_time
    print('Execution time:', res, 'seconds')
