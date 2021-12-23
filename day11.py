from collections import deque, namedtuple
import attr

Coord = namedtuple("Coord", ["i","j"])

@attr.s(auto_attribs=True, frozen=True)
class Octopus:
    energy: int = attr.ib()
    total_flashes: int = attr.ib(default=0)
    _has_flashed: bool = attr.ib(init=False, default=False)

    def reset(self):
        self._has_flashed = False

    def increase_energy(self) -> bool:
        """Returns true if flashed"""
        flash = False
        if not self._has_flashed:
            self.energy += 1
            if self.energy > 9:
                self.energy = 0
                self._has_flashed = True
                flash = True
        return flash

def get_square_coords(c: Coord, i_thres, j_thres) -> list[Coord]:
    square = []
    for i in [c.i-1, c.i, c.i+1]:
        for j in [c.j-1, c.j, c.j+1]:
            ignores = [
                (c.i == i and c.j == j), # center coord
                i - 1 < 0 or i >= i_thres, # i oob
                j - 1 < 0 or j >= j_thres, # j oob
            ]
            if not any(ignores):
                square.append(Coord(i, j))

    return square
     

if __name__ == "__main__":
    matrix = []
    stack = deque()
    with open("data/day11.txt") as f:
        for line in f:
            matrix.append([])
            for l in line.strip():
                matrix[-1].append(Octopus(int(l)))
    
    i_thres = len(matrix)
    j_thres = len(matrix[0])
    # Step1 increase
    for i in range(i_thres):
        for j in range(j_thres):
            matrix[i][j].reset()

    for i in range(i_thres):
        for j in range(j_thres):
            if matrix[i][j].increase_energy():
                stack.append(Coord(i, j))
    
    # Step 2 increase neighbours
    while stack:
        coords = get_square_coords(stack.pop())
        for c in coords:
            matrix[c.i][c.j].increase_energy()
    