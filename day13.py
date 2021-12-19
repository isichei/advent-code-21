from collections import namedtuple
import numpy as np

Point = namedtuple('Point', ['x', 'y'])
Fold = namedtuple('Fold', ['axis', 'value'])
points = []
folds = []

def fold_plot(plot: str, fold: Fold) -> str:
    if fold.axis == "y":
        plot = transpose(plot)
    
    matrix = plot_to_matrix(plot)
    start = fold.value+1
    end = len(matrix[0])
    for row in matrix:
        for i in range(start, end):
            if row[i] == "#":
                row[2*fold.value-i] = "#"

    new_matrix = []
    for row in matrix:
        new_matrix.append(row[:fold.value])
    
    plot = matrix_to_plot(new_matrix)
    if fold.axis == "y":
        plot = transpose(plot)

    
    return plot

def plot_to_matrix(plot: str) -> list[list[str]]:
    m = [[]]
    for p in plot:
        if p == "\n":
            m.append([])
        else:
            m[-1].append(p)
    return m

def matrix_to_plot(m: list[list[str]]) -> str:
    p = ""
    for l1 in m:
        for s in l1:
            p += s
        p += "\n"
    return p[:-1]

def transpose(plot: str) -> str:
    l = plot_to_matrix(plot)
    tl = list(map(list, zip(*l)))
    return matrix_to_plot(tl)

def count_dots(plot: str) -> int:
    counter = 0
    for p in plot:
        if p == "#":
            counter += 1
    return counter

def tests():
    data = "ab\ncd"
    m = plot_to_matrix(data)
    assert m == [["a", "b"], ["c", "d"]]

    data2 = matrix_to_plot(m)
    assert data == data2

    t = "ac\nbd"
    assert transpose(data) == t


if __name__ == "__main__":

    tests()

    # data = (
    #     "#.##..#..#.\n"
    #     "#...#......\n"
    #     "......#...#\n"
    #     "#...#......\n"
    #     ".#.#..#.###\n"
    #     "...........\n"
    #     "..........."
    # )

    # print(data)

    # new = fold_plot(data, Fold("x", 5))
    # print(new)

    # print(count_dots(new))
    with open("data/day13.txt") as f:
        for line in f:
            if "," in line:
                x, y = line.split(",", 1)
                points.append(Point(int(x), int(y)))
            elif "fold" in line:
                axis, value = line.replace("fold along ","").split("=")
                folds.append(Fold(axis, int(value)))

    max_y = max([p.y for p in points])+1
    max_x = max([p.x for p in points])+1

    paper_matrix = []
    for y in range(max_y):
        paper_matrix.append([])
        for x in range(max_x):
            paper_matrix[-1].append(".")

    for p in points:
        paper_matrix[p.y][p.x] = "#"


    paper = matrix_to_plot(paper_matrix)
    # folds = [folds[0]]
    for fold in folds:
        paper = fold_plot(paper, fold)
    
    print(count_dots(paper))
    print(paper)
    #     if fold.axis == "x":
    #         axis = 1
    #         paper1 = paper[:, :fold.value].copy()
    #         paper2 = paper[:, fold.value+1:].copy()
    #     else:
    #         axis = 0
    #         paper1 = paper[:fold.value, :].copy()
    #         paper2 = paper[fold.value+1:, :].copy()

    #     print(f"paper {paper.shape} fold along {fold.axis}={fold.value}. paper1: {paper1.shape} | paper2: {paper2.shape}")
    #     paper2 = np.flip(paper2, axis)
    #     if paper1.size[axis] == paper2.size[axis]:
    #         paper = paper1 + paper2
    #     else:
    #         paper = paper1 + np.r_

    
    #     print(np.count_nonzero(paper))