from node_class import Node
from tile_rules import tile_types
from tile_rules import handle_teleports

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
    
    directions = [(0, 1), (0, -1),(1, 0),(-1, 0)]#reverse order 

    neighbours = []
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
            tile = matrix[new_row][new_col]
            if handle_teleports(tile)['passable']:
                neighbours.append((new_col, new_row))
    return neighbours

def expand_node(current_node, matrix, fringe, expanded_positions, teleports):
    # If current node is a teleport entrance, only add exit as neighbour
    if current_node.position in teleports:
        exit_position = teleports[current_node.position]
        if exit_position not in expanded_positions:
            col, row = exit_position
            tile = matrix[row][col]
            child_node = Node(
                position=exit_position,
                tile_type=tile,
                parent=current_node,
                path_cost=current_node.path_cost  # 0 cost to teleport
            )
            fringe.append(child_node)
        return

    # Otherwise expand normally
    neighbours = get_neighbours(matrix, current_node.position)

    for position in neighbours:
        col, row = position
        # CRITICAL: We only check if it's been expanded. 
        # Checking if it's in the fringe prevents DFS from finding deeper paths.
        if position not in expanded_positions:
            tile = matrix[row][col]
            child_node = Node(
                position=position,
                tile_type=tile,
                parent=current_node,
                path_cost=current_node.path_cost + handle_teleports(tile)['cost']
            )
            fringe.append(child_node)
            
def reconstruct_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append(node.position)
        node = node.parent
    return list(reversed(path))

def runDFS(matrix, start_position, goal_position, teleports):
    fringe = [] 
    expanded_positions = set()

    print("DFS Search Initiated")
    print("Expanded: ", end="")
    
    start_node = create_start_node(matrix, start_position)
    fringe.append(start_node)

    while fringe:
        current_node = fringe.pop() # LIFO
        if current_node.position in expanded_positions:
            continue

        print(f"{current_node.position}", end="")
        
        if current_node.position == goal_position: 
            path = reconstruct_path(current_node)
            print("")
            print(f"Path Found: {path}")
            print(f"Taking this path will cost: {current_node.path_cost} Willpower")
            return path 

      
        expanded_positions.add(current_node.position)
        expand_node(current_node, matrix, fringe, expanded_positions, teleports)
        
    print("\nNO PATH FOUND!")
    return None