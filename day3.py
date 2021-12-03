from typing import List, Tuple


def get_bit_count(array: List[str], pos, oxygen=False) -> Tuple[str, int]:
    """
    Checks in what pos in binary had the most or least
    depending on oxygen flag 1s or 0s. Returning a tuple with
    string "1" or "0" and count of said string as an int
    """
    stats = {"1": 0, "0": 0}
    for a in array:
        stats[a[pos]] += 1
    if oxygen:
        bit = "1" if stats["1"] >= stats["0"] else "0"
        count = stats[bit]
    else:
        bit = "0" if stats["0"] <= stats["1"] else "1"
        count = stats[bit]
    return (bit, count)

def get_sample(array: List[str], pos: int, bit_value: str, number: int) -> List[str]:
    i = 0
    arr_len = len(array)
    new_array = []
    while len(new_array) < number and i < arr_len:
        if array[i][pos] == bit_value:
            new_array.append(array[i])
        i += 1
    return new_array

def part1():
    with open("data/day3.txt") as f:
        binaries = f.readlines()

    bin_converter = {"1": 1, "0": -1}
    binaries = [b.strip() for b in binaries]
    bin_len = len(binaries[0])
    gamma: List[bool] = [0]*bin_len
    max_value = int("1"*bin_len, 2)

    for binary in binaries:
        for i, b in enumerate(binary):
            gamma[i] += bin_converter[b]
    
    final_gamma_str = "".join(["1" if g > 0 else "0" for g in gamma])
    final_epsilon_str = "".join(["1" if g == "0" else "0" for g in final_gamma_str])
    print(final_gamma_str)
    print(final_epsilon_str)

    print("Part 1 ans: ", int(final_gamma_str, 2)*int(final_epsilon_str,2))


def part2():
    with open("data/day3.txt") as f:
        binaries = f.readlines()

    metrics = {"oxygen": None, "co2": None}
    for m in metrics:
        oxygen = m == "oxygen"
        sample = {"new": [], "current": [b.strip() for b in binaries]}
        pos = 0
        # Do bit criteria search
        while len(sample["new"]) > 1 or pos == 0:
            bit_value, sample_num = get_bit_count(sample["current"], pos, oxygen=oxygen)
            sample["new"] = get_sample(sample["current"], pos, bit_value, sample_num)
            
            # Iterate loop
            sample["current"] = [x for x in sample["new"]] # cba to copy
            pos += 1

        metrics[m] = "".join(sample["new"][0])
    print("Part 2, ans: ", int(metrics['oxygen'], 2) * int(metrics['co2'], 2))

if __name__ == "__main__":
    part1()
    part2()
