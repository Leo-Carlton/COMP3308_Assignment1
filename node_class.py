class Node:
    def __init__(self, position, tile_type, parent=None, path_cost=0):
        self.position = position      # (x, y) tuple
        self.tile_type = tile_type    # 'normal', 'mud', 'boulder', 'teleport', etc.
        self.parent = parent          # parent Node, for path reconstruction
        self.path_cost = path_cost    # cumulative Willpower cost from start
