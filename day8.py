from typing import Tuple, List

def get_data(line: str) -> Tuple[List[str], List[str]]:
    left, right = line.split("|", 1)

    left = ["".join(sorted(l)) for l in left.strip().split()]
    right = ["".join(sorted(r)) for r in right.strip().split()]
    return left, right

def resolve_letters(letters: List[str]) -> dict:
    n = {}
    lens = [len(l) for l in letters]
    
    one = letters[lens.index(2)]
    n[one] = "1"
    seven = letters[lens.index(3)]
    n[seven] = "7"
    four = letters[lens.index(4)]
    n[four] = "4"
    eight = letters[lens.index(7)]
    n[eight] = "8"

    # split lens 5 and 6
    code5 = []
    code6 = []
    for code, l in zip(letters, lens):
        match l:
            case 5:
                code5.append(code)
            case 6:
                code6.append(code)
            case _:
                pass
    
    # Search 6s
    # 4, 1 - 9 = 0, 0
    # 4, 1 - 6 = 1, 1
    # 4, 1 - 0 = 1, 0
    for c in code6:
        match (
            len(set(four).difference(c)),
            len(set(one).difference(c))
        ):
            case (0,0):
                n[c] = "9"
            case (1,1):
                n[c] = "6"
                six = c
            case (1, 0):
                n[c] = "0"
            case _:
                raise ValueError(f"Unexpected 6s: {c}")
    
    # Search 5s
    # 1,6 - 3 = 0,2 
    # 1,6 - 5 = 1,1
    # 1,6 - 2 = 1,2
    for c in code5:
        match (
            len(set(one).difference(c)),
            len(set(six).difference(c))
        ):
            case (0, 2):
                n[c] = "3"
            case (1, 1):
                n[c] = "5"
            case (1, 2):
                n[c] = "2"
            case _:
                raise ValueError(f"Unexpected 5s: {c}")
    return n


if __name__ == "__main__":
    total = 0
    with open("data/day8.txt") as f:
        for line in f:
            l, r = get_data(line)
            both = l + r
            decoded = resolve_letters(both)
            total += int("".join([decoded[r_] for r_ in r]))

    print(f"{total=}")
