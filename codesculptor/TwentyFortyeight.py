"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    front = to_merge(non_zeros(line))
    
    return front + [0] * (len(line) - len(front))

def non_zeros(lst):
    """
    Returns a list with all non-zero elements of the original 
    list.
    """
    return [num for num in lst if num != 0]

def to_merge(lst):
    """
    Returns all non-zero elements as a new list after merging.
    """
    num_to_double = 0
    
    for idx in range(len(lst)):
        if lst[idx] != num_to_double:
            num_to_double = lst[idx]
        else:
            lst[idx-1] = num_to_double *2
            lst[idx] = 0
            num_to_double = 0
            
    return non_zeros(lst)

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        
        self._init_tiles = {UP: [(0, col) for col in range(grid_width)],
        DOWN: [(grid_height - 1, col) for col in range(grid_width)],
        LEFT: [(row, 0) for row in range(grid_height)],
        RIGHT: [(row, grid_width - 1) for row in range(grid_height)]}
        
        self._num_steps = {UP: grid_height,
        DOWN: grid_height,
        LEFT: grid_width,
        RIGHT: grid_width}
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = []
        count = 0
        while count < self._grid_height:
            self._grid.append([0] * self._grid_width)
            count += 1
                
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        print 'Print out values in grid'
        for row in range(self._grid_height):
            print self._grid[row]
        return ''

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        
        for ids in self._init_tiles[direction]:
            line = []
            for step in range(self._num_steps[direction]):
                row = ids[0] + step * OFFSETS[direction][0]
                col = ids[1] + step * OFFSETS[direction][1]
                line.append(self.get_tile(row, col))
            output = merge(line)
            if output != line:
                moved = True
                for step in range(self._num_steps[direction]):
                    row = ids[0] + step * OFFSETS[direction][0]
                    col = ids[1] + step * OFFSETS[direction][1]
                    self.set_tile(row, col, output[step])
        
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # compute a list that restores the indices of zero elements
        self._empty_idx = [row * self._grid_width + col for row in range(self._grid_height) for col in range(self._grid_width) 
            if self._grid[row][col] == 0]
        
        if self._empty_idx != []:
            idx = random.choice(self._empty_idx)
            row = idx // self._grid_width
            col = idx % self._grid_width
            if random.randrange(0, 10) == 9:
                self.set_tile(row, col, 4)
            else:
                self.set_tile(row, col, 2)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
