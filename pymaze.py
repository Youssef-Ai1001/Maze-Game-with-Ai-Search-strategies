# ===> using DFS & BFS <===
import pygame                      # Used for GUI
from pygame.locals import *        #  For game development and handling events & Provides constants like QUIT and KEYDOWN
import random                      # For random maze generation 
import queue                       # Provides a Queue class for the BFS algorithm
from sys import argv               # Used to get command-line arguments
from Maze import Maze      # Maze Class


# The Game class handles the game initialization, drawing, player movement, and pathfinding.
# Initializes Pygame and sets up the display
class Game:
    # Initializes the game by setting up Pygame, creating the display window, 
    # and storing game parameters like difficulty, maze dimensions, and pathfinding (BFS Algo).
    def __init__(self, diff, dim, path):
        pygame.init()
        # Set Window Size
        self.size = (800, 600)
        # Create a display window with the specified Size
        self.screen = pygame.display.set_mode(self.size)
        # Title of Window
        pygame.display.set_caption("Maze Demo")
        # Game Icon 
        icon = pygame.image.load('conundrum.png')
        pygame.display.set_icon(icon)

        font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
        text = font.render("Loading...", 1, (255, 255, 255))
        rect = text.get_rect()
        rect.center = self.size[0] / 2, self.size[1] / 2
        self.screen.blit(text, rect)
        pygame.display.update(rect)

        self.diff = diff
        # Converts the dimensions of the maze from a string (eg "10x10") to a pair of integers
        self.dim = tuple(map(int, dim.split("x")))
        # Storing the Path
        self.path = path
        # Initializes a Maze object and calculate cell dimensions based on the screen size.
        self.maze_obj = Maze(*self.dim)
        self.cell_width = self.size[0] / self.maze_obj.cols
        self.cell_height = self.size[1] / self.maze_obj.rows

    def start(self):
        self.draw_maze()
        self.reset_player()
        self.loop()

    def reset_player(self):
        self.cx = self.cy = 0
        self.path_to_goal = self.find_path((0, 0), (self.maze_obj.cols - 1, self.maze_obj.rows - 1))
        self.curr_path_index = 0

    def draw_maze(self):
        self.screen.fill((102, 255, 102))
        # Draws the maze walls based on the maze dictionary.
        # loop on all rows in maze
        for y in range(self.maze_obj.rows):
            # loop on all columns in maze
            for x in range(self.maze_obj.cols):
                # If there is a south wall of the current cell
                if self.maze_obj.maze[(x, y)]['south']:  
                    # draw south wall
                    pygame.draw.line(self.screen, (255, 30, 30),
                                     (x * self.cell_width, (y + 1) * self.cell_height),
                                     ((x + 1) * self.cell_width, (y + 1) * self.cell_height))
                # If there is an east wall of the current cell
                if self.maze_obj.maze[(x, y)]['east']:  
                    # draw east wall
                    pygame.draw.line(self.screen, (255, 30, 30),
                                     ((x + 1) * self.cell_width, y * self.cell_height),
                                     ((x + 1) * self.cell_width, (y + 1) * self.cell_height))
        # Draw The Maze Border
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.size[0], self.size[1]), 1)
        # Refresh the screen to show the changes
        pygame.display.update()

    def loop(self):
        self.clock = pygame.time.Clock()
        # Set a variable to control the continuation of the loop
        self.keep_going = True

        # Main operation loop
        while self.keep_going:
            # Set the refresh rate to 10 fps ==> The speed of Player (dot)
            self.clock.tick(10)
            # Event processing
            for event in pygame.event.get():
                # to Quite the game press ESC key on keyboard
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.keep_going = False    # Excit the game

            # Verify that the end of the path has been reached
            if self.curr_path_index < len(self.path_to_goal):
                self.cx, self.cy = self.path_to_goal[self.curr_path_index]
                self.curr_path_index += 1

            # Draw the player in his current position
            self.draw_player()
            pygame.display.update()

# Drawing Player (Circle or Dot)
    def draw_player(self):
        self.screen.fill((255, 255, 255))
        self.draw_maze()
        # Color Of Circle
        pygame.draw.circle(self.screen, (0, 0, 255),
                           (int(self.cx * self.cell_width + self.cell_width / 2),
                            int(self.cy * self.cell_height + self.cell_height / 2)), 10)
        pygame.display.update() 

# Pathfinding: Implement a BFS algorithm in the find_path method to find a path from the start to end of the maze
    def find_path(self, start, end):
        q = queue.Queue()   # FIFO
        q.put((start, [start]))
        # Set for visited points
        visited = set()

        # loop continues until the queue is empty
        while not q.empty():
            # Take the first element of the queue (current point & current path)
            current_pos, path = q.get()
            if current_pos == end: # If the current point is the end point, return the path
                return path

            neighbors = self.get_neighbors(current_pos)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Add the neighbor to the queue with the updated path to include the new neighbor
                    q.put((neighbor, path + [neighbor]))
        return []

    def get_neighbors(self, pos):
        x, y = pos   # Extract the coordinates (x, y) from the entered location pos.
        neighbors = []
        # Check if there is a north wall and if it is possible to move to the north cell (can move north)
        if not self.maze_obj.maze[(x, y)]['north'] and y > 0:
            neighbors.append((x, y - 1))
        if not self.maze_obj.maze[(x, y)]['south'] and y < self.maze_obj.rows - 1:
            neighbors.append((x, y + 1))
        if not self.maze_obj.maze[(x, y)]['west'] and x > 0:
            neighbors.append((x - 1, y))
        if not self.maze_obj.maze[(x, y)]['east'] and x < self.maze_obj.cols - 1:
            neighbors.append((x + 1, y))
        return neighbors

# This condition checks whether this file is run as a main program and not as an imported library in another file.
if __name__ == "__main__":
    # Game Setting
    args = argv[1:]  # Take the arguments entered from the command line except for the file name.
    diff = 0
    dim = "30x40"
    path = 1
    for arg in args:
        if "--diff" in arg:
            diff = int(arg.split("=")[-1])
        elif "--dim" in arg:
            dim = arg.split("=")[-1]
        elif "--path" in arg:
            path = int(arg.split("=")[-1])

    g = Game(diff, dim, path)   # Creates an object of the Game class using user-entered or default values.
    g.start()
    pygame.quit()