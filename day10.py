from collections import deque

bracket_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

bracket_pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

bracket_close_score = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

def valid_close(char, expected_close) -> bool:
    return char == expected_close

def parse_line(line: str) -> tuple[str, deque]:
    stack = deque()
    stack.append(line[0])
    error_char = None
    for i, x in enumerate(line[1:]):
        if x in bracket_pairs:
            stack.append(x)
        elif valid_close(x, bracket_pairs[stack[-1]]):
            stack.pop()
        else:
            error_char = x
            break
    return error_char, stack

def unpack_stack_and_score(stack: deque) -> int:
    total = 0
    while stack:
        open_bracket = stack.pop()
        total *= 5
        total += bracket_close_score[open_bracket]
    return total

if __name__ == "__main__":
    with open("data/day10.txt") as f:
        lines = [l.strip() for l in f.readlines()]

    errors = []
    stacks = []
    for line in lines:
        e, s = parse_line(line)
        errors.append(e)
        stacks.append(s)
    
    # Part 1
    total = 0
    total_error_lines = 0
    for e in errors:
        if e:
            total += bracket_scores[e]
            total_error_lines += 1
    print(f"Part 1: {total} | {total_error_lines=}")

    # Part 2
    stack_scores = []
    for e, s in zip(errors, stacks):
        if not e:
            stack_scores.append(unpack_stack_and_score(s))

    sorted_scores = sorted(stack_scores)
    mid_score = sorted_scores[int(len(sorted_scores)/2)]

    print(f"Part 2: {mid_score=}")
