def create_map_matrix(filename):
    with open(filename, 'r') as f: 
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    cols, rows = map(int, lines[0].split('x'))
    start_col, start_row = map(int, lines[1].split('-'))
    
    matrix = []
    goal_position = None
    for i in range(rows):
        row = list(lines[2 + i])
        for j, tile in enumerate(row):
            if tile == 'X':
                goal_position = (j, i) 
        matrix.append(row)

    matrix[start_row][start_col] = 'S'
    return matrix, (start_col, start_row), goal_position  