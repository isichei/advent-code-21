import math

MAX_VALUE = 10
reverse_directions = {
    "up": "down",
    "right": "left",
    "down": "up",
    "left": "right",
}
def is_min(i: int, j: int, data: list[list[int]]) -> bool:
    up = MAX_VALUE
    down = MAX_VALUE
    left = MAX_VALUE
    right = MAX_VALUE

    if i > 0:
        up = data[i-1][j]

    if i < (len(data)-1):
        down = data[i+1][j]
    
    if j > 0:
        left = data[i][j-1]

    if j < (len(data[0])-1):
        right = data[i][j+1]

    v = data[i][j]
    return v < up and v < down and v < left and v < right

def get_next_coord(i, j, direction):
    match direction:
        case "up":
            return (i-1, j)
        case "down":
            return (i+1, j)
        case "left":
            return (i, j-1)
        case "right":
            return (i, j+1)
        case _:
            raise ValueError(f"Invalid {direction=}")

def search(i:int, j:int, prev_direction:str, data: list[list[int]], basin_log: list[tuple[int,int]]):

    # Check if current pos valid basin
    if i < 0 or i >= len(data):
        return None
    if j < 0 or j >= len(data[0]):
        return None
    if (i, j) in basin_log:
        return None
    if data[i][j] == 9:
        return None

    # Current position is basin
    basin_log.add((i,j))

    # Search remaining basin
    for d, rev_d in reverse_directions.items():
        if rev_d != prev_direction:
            ni, nj = get_next_coord(i, j, d)
            # print(f"At {(i, j)}. Going {d} to {(ni, nj)}")
            search(ni, nj, d, data, basin_log)

if __name__ == "__main__":
    data = []
    with open("data/day9.txt") as f:
        for line in f:
            data.append([int(l) for l in line.strip()])

    max_i = len(data)
    max_j = len(data[0])

    mins = []
    for i in range(max_i):
        for j in range(max_j):
            if is_min(i, j, data):
                mins.append((i,j))

    basin_logs = []
    for i, j in mins:
        basin_logs.append(set())
        search(i, j, "start", data, basin_logs[-1])
    
    lens = sorted([len(log) for log in basin_logs])
    print(math.prod(lens[-3:]))
