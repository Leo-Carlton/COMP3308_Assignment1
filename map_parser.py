def create_map_matrix(filename):
    with open(filename, 'r') as f: 
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    cols, rows = map(int, lines[0].split('x'))
    start_col, start_row = map(int, lines[1].split('-'))
    
    matrix = []
    goal_position = None
    teleports = {}
    entrances = {}
    exits = {}

    for i in range(rows):
        row = list(lines[2 + i])
        for j, tile in enumerate(row):
            if tile == 'X':
                goal_position = (j, i)
            elif tile.isdigit():
                num = int(tile)
                if num % 2 == 1:
                    entrances[num] = (j, i)
                else:
                    exits[num] = (j, i)
        matrix.append(row)

    # link entrances to exits after full scan
    for entrance_num, entrance_pos in entrances.items():
        exit_num = entrance_num + 1
        if exit_num in exits:
            teleports[entrance_pos] = exits[exit_num]

    matrix[start_row][start_col] = 'S'
    return matrix, (start_col, start_row), goal_position, teleports