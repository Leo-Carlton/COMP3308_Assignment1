import sys
from map_parser import create_map_matrix
from BFS import runBFS
from DFS import runDFS
from UCS import runUCS
from Greedy import runGreedy
from Astar import runAstar
from HillClimb import runHC

def main(strategy, filename):
    ## Make the map first
    map_layout, start_position, goal_position, teleports = create_map_matrix(filename)

    ## add all strategies
    if strategy == "B":
        runBFS(map_layout, start_position, goal_position, teleports)
    elif strategy == "D":
        runDFS(map_layout, start_position, goal_position, teleports)
    elif strategy == "U":
        runUCS(map_layout, start_position, goal_position, teleports)
    elif strategy == "G":
        runGreedy(map_layout, start_position, goal_position, teleports)
    elif strategy == "A":
        runAstar(map_layout, start_position, goal_position, teleports)
    else:
        runHC(map_layout, start_position, goal_position, teleports)
    return

if __name__ == '__main__':   
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        strategy = 'B'
        filename = 'example1.txt'
    else:
        strategy = sys.argv[1]
        filename = sys.argv[2]
    main(strategy, filename)
