tile_types = {
    'X': {'passable': True,  'cost': 1},
    '.': {'passable': True,  'cost': 1},
    'W': {'passable': False, 'cost': None},
    'M': {'passable': True,  'cost': 2},
    'B': {'passable': True,  'cost': 3},
    'S': {'passable': True,  'cost': 1},
    
}

def handle_teleports(tile):
    if tile.isdigit():
        return {'passable': True, 'cost': 1}
    return tile_types[tile]