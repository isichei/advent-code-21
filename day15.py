from collections import deque
from typing import Counter
from attr import Factory, define, field, fields
from collections import deque, namedtuple
from itertools import combinations_with_replacement, count, permutations, combinations
import sys
from copy import deepcopy
import numpy as np
import heapq
from time import perf_counter

# f(n) = g(n) + h(n)
# n is next node
# g cost of start to n
# h is heuristic

Pos = namedtuple("Pos", "x,y")
TARGET_POS = Pos(9, 9)

@define(order=False)
class Node:
    x: int
    y: int
    total_risk: int = field(eq=False) 
    prev_pos: Pos = field(default=None, eq=False)

    def __lt__(self, other) -> bool:
        return self.total_risk < other.total_risk

    def __repr__(self) -> str:
        return f"Node[{(self.x, self.y)} | f={self.total_risk}]"

    def get_neighbours(self) -> list[Pos]:
        out = []
        # down, up, left, right
        for d in [Pos(0,1), Pos(0,-1), Pos(-1,0), Pos(1,0)]:
            p = Pos(self.x + d.x, self.y + d.y)
            if (p.x <= TARGET_POS.x and p.x >= 0 and p.y <= TARGET_POS.y and p.y >=0):
                out.append(p)
        return out
    
    def get_pos(self) -> Pos:
        return Pos(self.x, self.y)


def print_route(route_map: list[list[int]], route: deque):
        map_str = []
        for row in route_map:
            map_str.append([f" {r} " for r in row])
        
        for n in route:
            map_str[n.y][n.x] = "(" + map_str[n.y][n.x][1] + ")"
        
        for row in map_str:
            print(" ".join(row))
 

if __name__ == "__main__":
    start_time = perf_counter()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        data_fp = "data/day15-test.txt" 
    else:
        data_fp = "data/day15.txt" 
    with open(data_fp) as f:
        route_map = []
        for line in f:
            route_map.append([int(x) for x in line.strip()])

    np_route_mapmap = np.array(route_map)
    initial_map = np_route_mapmap.copy()
    cave_map_p2 = initial_map.copy()

    for row in range(1, 5):
        new_values = (initial_map + row - 1) % 9 + 1
        cave_map_p2 = np.append(cave_map_p2, new_values, axis=0)

    initial_map = cave_map_p2.copy()
    for column in range(1, 5):
        new_values = (initial_map + column - 1) % 9 + 1
        cave_map_p2 = np.append(cave_map_p2, new_values, axis=1)
    
    np_route_mapmap = cave_map_p2
    max_y, max_x = np_route_mapmap.shape

    TARGET_POS = Pos(max_x-1, max_y-1)

    open_nodes = []
    closed_nodes = {}

    current_pos = Pos(0,0) # x,y

    current_node = Node(x=0, y=0, total_risk=0)
    open_nodes.append(current_node)

    while current_node.get_pos() != TARGET_POS:
        current_node = heapq.heappop(open_nodes)

        if (current_node.x, current_node.y) in closed_nodes: continue

        for neighbour in current_node.get_neighbours():
            risk = np_route_mapmap[current_node.y, current_node.x]
            total_risk = risk + current_node.total_risk
            n = Node(neighbour.x, neighbour.y, total_risk=total_risk, prev_pos=current_node.get_pos())
            heapq.heappush(open_nodes, n)
        
        # Add the current node to closed
        closed_nodes[(current_node.x, current_node.y)] = current_node

    print(f"Time: {perf_counter()-start_time}")
    print(len(closed_nodes))
    print(len(open_nodes))
    print(current_node)

    route = deque()
    route.append(current_node.get_pos())
    total_risk = 0
    while current_node.prev_pos is not None:
        total_risk += np_route_mapmap[current_node.y, current_node.x]
        route.append(current_node.prev_pos)
        current_node = closed_nodes[(route[-1].x, route[-1].y)]
    print(f"{total_risk=}")

    # print_route(route_map, route)

    