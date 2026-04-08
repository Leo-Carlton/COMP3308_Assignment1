from node_class import Node
from collections import deque
from tile_rules import tile_types


def create_start_node(matrix, node_start_location):
    col, row = node_start_location 
    start_node = Node(
        position=node_start_location,
        tile_type=matrix[row][col],
        parent=None,
        path_cost=0
    )
    return start_node


def get_neighbours(matrix, position):
    col, row = position 
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
    neighbours = []
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            tile = matrix[new_row][new_col]
            if tile_types[tile]['passable']:
                neighbours.append((new_col, new_row))  # (col, row)
    return neighbours


def expand_node(current_node, matrix, fringe, expanded):
    expanded.append(current_node)
    neighbours = get_neighbours(matrix, current_node.position)
    for position in neighbours:
        col, row = position 
        if position not in [n.position for n in expanded]:
            tile = matrix[row][col]
            child_node = Node(
                position=position,
                tile_type=tile,
                parent=current_node,
                path_cost=current_node.path_cost + tile_types[tile]['cost']
            )
            fringe.append(child_node)


def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node.position)
        node = node.parent
    return list(reversed(path))


def runBFS(matrix, start_position, goal_position):
    fringe = deque()
    expanded = []

    print("BFS Search Initiated")
    print("Expanded:", end="")
    start_node = create_start_node(matrix, start_position)
    fringe.append(start_node)

    while fringe:
        current_node = fringe.popleft()

        if current_node.position == goal_position:
            path = reconstruct_path(current_node)
            print("")
            print(f"Path Found: {path}")
            print(f"Taking this path will cost: {current_node.path_cost} Willpower")
            return path

        expand_node(current_node, matrix, fringe, expanded)
        print(f"{current_node.position}", end="")

    print("No path found")
    return None