import csv as c


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, compartment, endstored, startcompartment):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Initialize path
    path = []

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:

            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            # Choke point 1

            if compartment == 1:  # Makes the path go passed the choke points if necessary
                if startcompartment in (2, 3, 4, 5, '2c', '8b'):
                    path = chokepoint(maze, (7, 2), endstored, path)

            if compartment in (2, 3, 4, 5, '2c', '8b'):
                if startcompartment == 1:
                    path = chokepoint(maze, (7, 2), endstored, path)

            # Choke point 2

            if compartment == '2c':
                if start == (8, 11):
                    path = chokepoint(maze, (4, 7), endstored, path)
                elif startcompartment in (3, 5, '8b'):
                    path = chokepoint(maze, (3, 7), endstored, path)

            if compartment == 3:
                if startcompartment == '2c':
                    path = chokepoint(maze, (3, 7), endstored, path)

                # Choke point 3

            if compartment in (2, 3, 4, '1b', '2b'):
                if startcompartment in (6, 7, 8, '6b', '7b', '8c', '8d'):
                    path = chokepoint(maze, (9, 14), endstored, path)

            if compartment == '8c':
                if startcompartment in (1, 2, 3, 4, 5, '1b', '2b', '2c'):
                    path = chokepoint(maze, (9, 14), endstored, path)

            if compartment in ('6b', '7b'):
                if startcompartment in (1, 2, 3, 4, 5, '1b', '2b', '2c'):
                    path = doublechokepoint(maze, (9, 14), (10, 10), path, endstored)

            if compartment == 7:
                if startcompartment in (1, 2, 3, 4, 5, '1b', '2b', '2c'):
                    path = doublechokepoint(maze, (9, 14), (11, 10), path, endstored)

            if compartment in (8, '8d'):
                if startcompartment in (1, 2, 3, 4, '1b', '2b', '2c'):
                    path = chokepoint(maze, (9, 14), endstored, path)

            if compartment == 8:
                if start in ((7, 14), (6, 14), (5, 14), (4, 14), (3, 14), (2, 14), (6, 15), (5, 15), (4, 15), (3, 15),
                             (2, 15), (5, 16), (4, 16), (3, 16), (2, 16), (4, 17), (3, 17), (2, 17), (3, 18), (2, 18),
                             (2, 19)):
                    path = chokepoint(maze, (9, 14), endstored, path)

            if compartment == 1:
                if startcompartment in (6, 7, 8, '6b', '7b', '8c', '8d'):
                    path = doublechokepoint(maze, (9, 14), (7, 2), path, endstored)

            if compartment == '2c':
                if startcompartment in (6, 7, 8, '6b', '7b', '8c', '8d'):
                    path = doublechokepoint(maze, (9, 14), (3, 7), path, endstored)

            if compartment == 6:
                if startcompartment in (1, 2, 3, 4, 5, '1b', '2b', '2c'):
                    path = doublechokepoint(maze, (9, 14), (11, 2), path, endstored)

            # Choke point 4

            if compartment == 6:
                if startcompartment in (7, 8, '8b', '8c', '8d'):
                    path = chokepoint(maze, (11, 2), endstored, path)

            if compartment == 6:
                if startcompartment == '7b':
                    path = chokepoint(maze, (10, 2), endstored, path)

            if compartment in (7, '8c'):
                if startcompartment == 6:
                    path = chokepoint(maze, (11, 2), endstored, path)

            # Choke point 5

            if compartment == 7:
                if startcompartment in (8, '8b', '8d'):
                    path = chokepoint(maze, (11, 10), endstored, path)

            if compartment == 8:
                if startcompartment in (6, 7, '6b', '7b'):
                    path = chokepoint(maze, (11, 11), endstored, path)

            if compartment == '8b':
                if startcompartment == 6:
                    path = chokepoint(maze, (11, 10), endstored, path)
                if startcompartment in ('6b', '7b'):
                    path = chokepoint(maze, (10, 10), endstored, path)

            return path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            # print(child.position)
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def chokepoint(maze, start, end, path):
    """First sets the end of the first run through astar() as start and sets end (which was endstored) as end
    maze = grid without the path
    path = all coordinates of the current path from initial start to choke point"""
    path1 = astar(maze, start, end, 0, 0, 0)
    path = path1 + path
    return path


def doublechokepoint(maze, start, end, path, endstored):
    """First sets the end of the first run through astar() as start and sets the next choke point as end, lastly sets
    that end as start and sets the endstored (which is the initial end) as end"""
    path1 = astar(maze, start, end, 0, endstored, 0)
    path = path1 + path
    path2 = astar(maze, end, endstored, 0, 0, 0)
    path = path2 + path
    return path


def matrix_reader():
    """Opens the matrix and sets it in a two-dimensional list, also known as the grid"""
    with open(r"maps/mapmatrix04v3.txt", "r") as map:
        reader = c.reader(map)
        matrix = list()
        for row in reader:
            new_row = list()
            for x in row:
                new_row.append(int(x))
            matrix.append(list(new_row))
    better = [e for e in matrix if e]

    return better


def dmain(start, end):
    """Runs once enter is pressed (from application.py)"""
    compartment = int()
    startcompartment = int()
    maze = matrix_reader()
    endfirst = end

    # Determines in which compartment you start and end
    for i in range(0, 2):  # Upper Left
        for j in range(0, 8):
            if end == (j, i):
                compartment = 1
            if start == (j, i):
                startcompartment = 1

    if end == (8, 0) or end == (8, 1):  #  Under Upper Left
        compartment = '1b'
    if end == (8, 0) or end == (8, 1):
        startcompartment = '1b'

    for i in range(2, 7):  # Right of Upper Left
        for j in range(0, 8):
            if end == (j, i):
                compartment = 2
            if start == (j, i):
                startcompartment = 2

    for i in range(2, 7):  # Under Right of Upper Left
        for j in range(8, 9):
            if end == (j, i):
                compartment = '2b'
            if start == (j, i):
                startcompartment = '2b'

    for i in range(5, 7):  # Right of Upper Left
        for j in range(0, 4):
            if end == (j, i):
                compartment = '2c'
            if start == (j, i):
                startcompartment = '2c'

    for i in range(7, 11):  # Upper Mid
        for j in range(0, 3):
            if end == (j, i):
                compartment = 3
            if start == (j, i):
                startcompartment = 3

    for i in range(7, 11):  # Under Upper Mid
        for j in range(3, 9):
            if end == (j, i):
                compartment = 4
            if start == (j, i):
                startcompartment = 4

    for i in range(11, 20):  # Upper Right
        for j in range(0, 10):
            if end == (j, i):
                compartment = 5
            if start == (j, i):
                startcompartment = 5

    for i in range(0, 2):  # Lower Left
        for j in range(11, 22):
            if end == (j, i):
                compartment = 6
            if start == (j, i):
                startcompartment = 6

    if end == (10, 0) or end == (10, 1):  # Above Lower Left
        compartment = '6b'
    if start == (10, 0) or start == (10, 1):
        startcompartment = '6b'

    for i in range(2, 10):  # Lower Mid
        for j in range(11, 22):
            if end == (j, i):
                compartment = 7
            if start == (j, i):
                startcompartment = 7

    for i in range(2, 10):  # Above Lower Mid
        if end[1] == i and end[0] == 10:
            compartment = '7b'
        if start[1] == i and start[0] == 10:
            startcompartment = '7b'

    for i in range(13, 20):  # Lower Right
        for j in range(11, 22):
            if end == (j, i):
                compartment = 8
            if start == (j, i):
                startcompartment = 8

    for i in range(16, 20):  # Upper Right within Lower Right
        for j in range(10, 13):
            if end == (j, i):
                compartment = '8b'
            if start == (j, i):
                startcompartment = '8b'

    if end == (12, 16):
        compartment = 8
    if start == (12, 16):
        startcompartment = 8

    for i in range(10, 13):  # Upper Right within Lower Right
        for j in range(10, 12):
            if end == (j, i):
                compartment = '8c'
            if start == (j, i):
                startcompartment = '8c'

    for i in range(13, 16):  # Lower Right
        for j in range(10, 11):
            if end == (j, i):
                compartment = '8d'
            if start == (j, i):
                startcompartment = '8d'

    # Checks if it has to pass a choke point or not for all routes
    # Choke point 1
    if compartment == 1:
        if startcompartment in (2, 3, 4, 5, '2c', '8b'):
            endfirst = (7, 2) # Choke point 1

    if compartment in (2, 3, 4, 5, '2c', '8b'):
        if startcompartment == 1:
            endfirst = (7, 2)

    # Choke point 2
    if compartment == '2c':
        if start == (8, 11):
            endfirst = (4, 7)  # Special choke point 3
        elif startcompartment in (3, 5, '8b'):
            endfirst = (3, 7)  # Choke point 2

    if compartment == 3:
        if startcompartment == '2c':
            endfirst = (3, 7)

    # Choke point 3
    if compartment in (1, 2, 3, 4, '1b', '2b', '2c'):
        if startcompartment in (6, 7, 8, '6b', '7b', '8c', '8d'):
            endfirst = (9, 14)  # Choke point 3

    if compartment in (6, 7, '6b', '7b', '8c'):
        if startcompartment in (1, 2, 3, 4, 5, '1b', '2b', '2c'):
            endfirst = (9, 14)

    if compartment in (8, '8d'):
        if startcompartment in (1, 2, 3, 4, '1b', '2b', '2c'):
            endfirst = (9, 14)

    if compartment == 8:
        if start in ((7, 14), (6, 14), (5, 14), (4, 14), (3, 14), (2, 14), (6, 15), (5, 15), (4, 15), (3, 15), (2, 15),
                     (5, 16), (4, 16), (3, 16), (2, 16), (4, 17), (3, 17), (2, 17), (3, 18), (2, 18), (2, 19)):
            endfirst = (9, 14)

    # Choke point 4
    if compartment == 6:
        if startcompartment in (7, 8, '8b', '8c', '8d'):
            endfirst = (11, 2)  # Choke point 4

    if compartment == 6:
        if startcompartment == '7b':
            endfirst = (10, 2)  # Special choke point 1

    if compartment in (7, '8c'):
        if startcompartment == 6:
            endfirst = (11, 2)

    # Choke point 5
    if compartment == 7:
        if startcompartment in (8, '8b', '8d'):
            endfirst = (11, 10)  # Choke point 5

    if compartment == 8:
        if startcompartment in (6, 7, '6b', '7b'):
            endfirst = (11, 11)

    if compartment == '8b':
        if startcompartment == 6:
            endfirst = (11, 10)
        if startcompartment in ('6b', '7b'):
            endfirst = (10, 10)  # Special choke point 2

    path = astar(maze, start, endfirst, compartment, end, startcompartment)

    return path

#if __name__ == '__main__':
#    main()