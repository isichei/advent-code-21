from dataclasses import dataclass

MAX_CAVE_VISITS = 1

@dataclass
class Node:
    name: str
    i: int = -1

def get_next_node(node: Node, edges: dict[str, list[str]]) -> Node | None:
    node.i += 1
    try:
        return Node(edges[node.name][node.i])
    except IndexError:
        return None

def get_data() -> dict[str, list[str]]:
    edges: dict[str, list[str]] = {}
    with open("data/day12.txt") as f:
        for line in f:
            start, end = line.strip().split("-", 1)
            if start in edges:
                edges[start].append(end)
            else:
                edges[start] = [end]
            
            if start == "start" or end == "end":
                continue

            if end in edges:
                edges[end].append(start)
            else:
                edges[end] = [start]
    return edges


def is_lower(s: str) -> bool:
    return s.lower() == s

# Add next node to the path
if __name__ == "__main__":
    edges = get_data()
    print(edges)
    edges["end"] = []
    path = []
    total_paths = 0

    path.append(Node("start"))

    while path:
        # print(" -> ".join([n.name for n in path]))
        next_node = get_next_node(path[-1], edges)
    
        # If next node is None then no more paths exist from current node
        if next_node is None:
            path.pop()
        
        # If next node is an "end" then note it and continue searching
        elif next_node.name == "end":
            path_str = " -> ".join([n.name for n in path] + ["end"])
            # print(f"Found path: {path_str}")
            total_paths += 1

        # Check if this is a node that can be revisited
        elif is_lower(next_node.name) and sum([n.name == next_node.name for n in path]) >= MAX_CAVE_VISITS:
            pass

        # latest cave is legal add it to path
        else:
            path.append(next_node)

    print(f"{total_paths=}")
