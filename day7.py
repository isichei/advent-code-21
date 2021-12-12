import numpy as np

def sum_ints(x: int) -> int:
    return int(x*(x+1)*0.5)

if __name__ == "__main__":
    with open("data/day7.txt") as f:
        raw_text = f.read()
        positions = np.array([int(x) for x in raw_text.split(",")])

    min_position = None
    min_value = (positions**2).sum()**2 # give a large value
    v_sum_ints = np.vectorize(sum_ints)
    max_pos = positions.max()
    for i, pos in enumerate(range(max_pos)):
        diff_array = abs(positions-pos)
        new_min = (v_sum_ints(diff_array)).sum()
        if new_min < min_value:
            min_position = i
            min_value = new_min

    print(f"{min_position=}, {min_value=}")
