from enum import Enum, auto

class Direction(Enum):
    INCREASED = auto()
    DECREASED = auto()
    SAME = auto()

if __name__ == "__main__":
    with open("data/day1.text") as f:
        sonar = [int(x) for x in f.read().split()]

    # True is increased
    window_len = 3
    directions = [Direction.SAME]
    for i in range(len(sonar)-window_len):
        diff = sonar[i+window_len] - sonar[i]
        if diff == 0:
            directions.append(Direction.SAME)
        elif diff > 0:
            directions.append(Direction.INCREASED)
        elif diff < 0:
            directions.append(Direction.DECREASED)
        else:
            raise ValueError("Duh!!!")

    stats = {}
    for d in Direction:
        stats[d.name] = sum([1 if direction == d else 0 for direction in directions])
    print(stats)
