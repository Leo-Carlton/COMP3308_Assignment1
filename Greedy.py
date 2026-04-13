from node_class import Node
import heapq
from tile_rules import handle_teleports

def create_start_node(matrix, node_start_location):
    col, row = node_start_location
    return Node(
        position=node_start_location,
        tile_type=matrix[row][col],
        parent=None,
        path_cost=0
    )

def heuristic(position, goal, teleports):
    if position in teleports:
        position = teleports[position]  # use exit position for heuristic
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

def get_neighbours(matrix, position):
    col, row = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  ## Left Right Up Down
    neighbours = []
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            tile = matrix[new_row][new_col]
            if handle_teleports(tile)['passable']:
                neighbours.append((new_col, new_row))
    return neighbours

def expand_node(current_node, matrix, fringe, expanded, teleports, goal_position, counter):
    expanded.append(current_node)

    expanded_positions = [n.position for n in expanded]
    fringe_positions = [n.position for _, _, _, _, n in fringe]

    # If current node is a teleport entrance, only add the exit as neighbour
    if current_node.position in teleports:
        exit_position = teleports[current_node.position]
        if exit_position not in expanded_positions and exit_position not in fringe_positions:
            col, row = exit_position
            tile = matrix[row][col]
            # 0 Willpower to teleport to exit
            new_cost = current_node.path_cost
            h = heuristic(exit_position, goal_position, teleports)
            counter += 1
            child_node = Node(
                position=exit_position,
                tile_type=tile,
                parent=current_node,
                path_cost=new_cost
            )
            heapq.heappush(fringe, (h, exit_position[0], exit_position[1], counter, child_node))
        return counter

    # Otherwise expand normally
    neighbours = get_neighbours(matrix, current_node.position)

    for position in neighbours:
        col, row = position
        tile = matrix[row][col]

        if position in expanded_positions or position in fringe_positions:
            continue

        new_cost = current_node.path_cost + handle_teleports(tile)['cost']
        h = heuristic(position, goal_position, teleports)
        counter += 1
        child_node = Node(
            position=position,
            tile_type=tile,
            parent=current_node,
            path_cost=new_cost
        )
        heapq.heappush(fringe, (h, position[0], position[1], counter, child_node))

    return counter

def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node.position)
        node = node.parent
    return list(reversed(path))

def runGreedy(matrix, start_position, goal_position, teleports):
    fringe = []
    expanded = []
    counter = 0

    print("Greedy Search Initiated")
    print("Expanded:", end="")
    start_node = create_start_node(matrix, start_position)
    h = heuristic(start_position, goal_position, teleports)
    heapq.heappush(fringe, (h, start_position[0], start_position[1], counter, start_node))

    while fringe:
        _, _, _, _, current_node = heapq.heappop(fringe)

        print(f"{current_node.position}", end="")
        counter = expand_node(current_node, matrix, fringe, expanded, teleports, goal_position, counter)

        if current_node.position == goal_position:
            path = reconstruct_path(current_node)
            print("")
            print(f"Path Found: {path}")
            print(f"Taking this path will cost: {current_node.path_cost} Willpower")
            return path

    print("No path found")
    return None

