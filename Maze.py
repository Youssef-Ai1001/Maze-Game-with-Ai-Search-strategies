import random  # For random maze generation
#  Maze class with methods to initialize and generate the maze using Depth-First Search
class Maze:
    def __init__(self, rows, cols):
        # (Rows and Columns) are Dimensions of the maze
        self.rows = rows                  
        self.cols = cols
        # A dictionary representing the maze Dimensions or structure 
        # to create the initial maze with all walls
        self.maze = self.initialize_maze(rows, cols) 
        # Generates the maze starting from the top-left (0 , 0) corner using DFS 
        self.generate((0, 0))  

#  create a dictionary representing the maze.
#  Each cell has information about its four walls (north, south, east, west) being open (True) or closed (False).
    def initialize_maze(self, rows, cols):  
        # (x , y)    Dimensions for the Cell ==>  x from 0 to cols - 1   & y from 0 to rows - 1
        # This mean that each cell has the four Walls
        maze = {(x, y): {'north': True, 'south': True, 'east': True, 'west': True}
                for x in range(cols) for y in range(rows)}
        return maze 

# Maze Generation using DFS
    def generate(self, start):
        # Keep tracking the path (unvisited Cell)
        stack = [start]  # start is the primary cell (first cell)
        # Keep tracking  visited cells 
        visited = {start}
  # All Possible moves (R)      (D)     (L)      (U)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # This loop stop when there are no cells in stack
        while stack:
            # select a current unvisited  From Stack (the top one)
            current = stack[-1]
            # Calc all possible neighbor to the current Cell Using the specific directions
            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in directions]
            # Checks for unvisited neighbors still within the border of the maze
            unvisited_neighbors = [n for n in neighbors if n in self.maze and n not in visited]

            if unvisited_neighbors:
                # Choose a random cell from unvisited_neighbors
                next_cell = random.choice(unvisited_neighbors)
                self.remove_wall(current, next_cell)
                # Add next_cell (visited) to the Visited Stack
                visited.add(next_cell)
                stack.append(next_cell)
            else:
                # If there are no unvisited neighbors ==> Removes the current cell from the stack (moves back in the path)
                stack.pop()
# معناه هيعدي للخليه الي جمبه ازاله الجدار 
    def remove_wall(self, current, next_cell):
        # Calc the difference between the current cell and next cell
        dx = next_cell[0] - current[0]    # احداثي العمود  
        dy = next_cell[1] - current[1]    # احداثي الصف
        # If the next cell is located to the right of the current cell  
        if dx == 1:
            self.maze[current]['east'] = False        # Remove the east Wall from the current cell
            self.maze[next_cell]['west'] = False      # Remove the west Wall from the next cell
        # If the next cell is located to the left of the current cell  
        elif dx == -1:
            self.maze[current]['west'] = False
            self.maze[next_cell]['east'] = False
        # If the next cell is located to the down of the current cell  
        elif dy == 1:
            self.maze[current]['south'] = False
            self.maze[next_cell]['north'] = False
        # If the next cell is located to the up of the current cell  
        elif dy == -1:
            self.maze[current]['north'] = False
            self.maze[next_cell]['south'] = False
