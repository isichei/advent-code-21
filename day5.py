from typing import Generator, List, Tuple
import attr

@attr.s(auto_attribs=True, frozen=True)
class Coordinate:
    x: int = attr.ib()
    y: int = attr.ib()

    @classmethod
    def from_raw_input(cls, input: str):
        """
        Expects str in format x, y
        """
        x_str, y_str = input.split(",")
        x = int(x_str.strip())
        y = int(y_str.strip())

        c = Coordinate(x, y)
        return c


@attr.s(auto_attribs=True)
class Vent:
    start: Coordinate = attr.ib()
    end: Coordinate = attr.ib()
    vent_type: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        if self.start.x != self.end.x and self.start.y != self.end.y:
            self.vent_type = "diaginal"
        elif self.start.x == self.end.x:
            self.vent_type = "vertical"
        elif self.start.y == self.end.y:
            self.vent_type = "horizontal"
        else:
            self.vent_type = "unknown"

    @classmethod
    def from_raw_input(cls, input: str):
        """
        Expects format "x1,y1 -> x2,y2"
        """
        start_coord, end_coord = input.split("->")
        start = Coordinate.from_raw_input(start_coord.strip())
        end = Coordinate.from_raw_input(end_coord.strip())
        return cls(start, end)

    def horizontal_walk(self):
        step = -1 if self.start.x > self.end.x else 1
        for i in range(self.start.x, self.end.x + step, step):
            yield i
    
    def vertical_walk(self):
        step = -1 if self.start.y > self.end.y else 1
        for i in range(self.start.y, self.end.y + step, step):
            yield i


def get_min_max_coords(vents: List[Vent]) -> Tuple[int, int, int, int]:
    """
    returns min_x, max_x, min_y, max_y
    """
    min_x, max_x, min_y, max_y = (0, 0, 0, 0)
    for v in vents:
        min_x = min(v.start.x, v.end.x, min_x)
        max_x = max(v.start.x, v.end.x, max_x)
        min_y = min(v.start.y, v.end.y, min_y)
        max_y = max(v.start.y, v.end.y, max_y)

    max_x += 1
    max_y += 1
    return (min_x, max_x, min_y, max_y)


if __name__ == "__main__":
    vents = []
    min_x, max_x, min_y, max_y = (0, 0, 0, 0)

    with open("data/day5.txt") as f:
        for line in f:
            vents.append(Vent.from_raw_input(line))            

    # vh_vents = [v for v in vents if v.vent_type != "diaginal"]
    vh_vents = vents
    
    # init grid
    min_x, max_x, min_y, max_y = get_min_max_coords(vh_vents)
    grid = []
    for y in range(max_y):
        grid.append([])
        for x in range(max_x):
            grid[y].append(0)

    for vent_number, v in enumerate(vh_vents):
        match v.vent_type:
            case "diaginal":
                for x, y in zip(v.horizontal_walk(), v.vertical_walk()):
                    grid[y][x] += 1
            case "horizontal":
                for x in v.horizontal_walk():
                    grid[v.start.y][x] += 1
            case "vertical":
                for y in v.vertical_walk():
                    grid[y][v.start.x] += 1
            case _:
                raise ValueError(f"UNKOWN TYPE, {vent_number}: {v}")

    total = 0
    for y in range(max_y):
        for x in range(max_x):
            if grid[y][x] > 1:
                total += 1
    print(f"{total=}")
    # for g in grid:
    #     print(g)

