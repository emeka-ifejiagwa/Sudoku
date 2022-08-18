from __future__ import annotations
import numpy as np
from random import choice

class Generator():
    """
    The Generator class generates and validates Sudoku boards
    There is no guarantee for uniqueness of the generated sudoku board
    np.int8 is used because the numbers in the boards are always small (0 - 9)
    This generator was used to test the solver

    Staticmethods
    -------------
    print_board(board: list[list]|np.ndarray((9,9), np.int8)) -> None
        prints the generated board in a stylized manner
    
    Methods
    -------
    generate(self) -> np.ndarray((9,9), np.int8)
        generates a sudoku board
    populate(self, grid: np.ndarray((9,9), np.int8) -> bool
        populates an empty game board
    next_empty_cell(self, grid: np.ndarray((9,9), np.int8), row_by_row = False) -> tuple
        finds the next empty cell in the game board
    is_valid(self, grid: np.ndarray((9,9), np.int8), val: int, position: tuple) -> bool
        checks if the intended move (insertion) is a valid one
    __in_box(self, grid: np.ndarray((9,9), np.int8), val: int, position: tuple) -> bool:
        checks if a number is in the 3 * 3 sub grid
    clear_blocks(self, grid: np.ndarray((9,9), np.int8), num_to_clear: int) -> None
        clears a random number of boxes
    """
    def generate(self) -> np.ndarray((9,9), np.int8):
        """
        Generates a Sudoku board

        Returns
        -------
        a numpy array with shape (9,9) ie a 9 by 9 array
        """
        grid = np.zeros((9,9), dtype=np.int8)
        # once fully populated, clear some cells
        grid[np.random.randint(0, 9), np.random.randint(0, 9)] = np.random.randint(1, 10)
        if self.populate(grid):
            # the more the empty cells, the more likely that there would be duplicate solutions
            # tweaking this number affects the performance of the code
            self.clear_blocks(grid, np.random.randint(35,57))
        return grid

    def populate(self, grid: np.ndarray((9,9), np.int8)) -> bool:
        """
        Populates the sudoku board from scratch

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid to populate

        Returns
        -------
        returns True if it was successful else False
        """
        pos = self.next_empty_cell(grid)
        # if there are no more empty cells then we are done
        if not pos:
            return True
        i, j = pos
        available = np.arange(1, 10)
        #shuffling ensures that a unique grid is generated each time
        np.random.shuffle(available)
        for curr in available:
            if self.is_valid(grid, curr, (i,j)):
                grid[i, j] = curr
                if self.populate(grid):
                    return True
            grid[i, j] = 0
        return False

    def next_empty_cell(self, grid: np.ndarray((9,9), np.int8), row_by_row: bool = False) -> tuple:
        """
        finds the next empy cell, denoted by a cell whose value is 0

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8
            the grid to search
        row_by_row: bool, optional, default: False
            indicates whether to move row by row or column by column
        Returns
        -------
        the position of the next empty cell
        """
        for i in range(len(grid)):
            for j in range(len(grid)):
                # while testing, i found that it was faster to solve column by column most times
                # however, the visualization was more intuitive row by row
                # therefore, the row_by_row parameter is actually only used when visualizing the solving process
                pos = (i,j) if row_by_row else (j,i)
                if grid[pos] == 0:
                    return pos
        return ()

    def is_valid(self, grid: np.ndarray((9,9), np.int8), val: int, position: tuple) -> bool:
        """
        Checks if a it is valid to place the in the position

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being worked on
        val: int
            the value to be inserted
        position: tuple
            the location of insertion
        Returns
        -------
        bool:
            indicates whether the move is valid
        """
        # the second expression checks if the value is in the row
        # position[0] denotes the row
        # the third expression checks if the value is in the column
        # position[1] indicates the colum
        result =   self.__in_box(grid, val,  position)\
            or  val in grid[position[0],]\
            or  val in grid[:,position[1]] # this notation checks all values in the specified column
        return not result
 

    def __in_box(self, grid: np.ndarray((9,9), np.int8), val: int, position: tuple) -> bool:
        """
        Checks if is in the current box
        Note: a box is a 3 by 3 grid

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being worked on
        val: int
            the value to be inserted
        position: tuple
            the location of insertion
        
        Returns
        -------
        bool:
            indicates whether the passed value is in the subgrid
        """
        row, column = position
        # gets the row and column of the first elemnt in the box
        box_start_row = row - row % 3
        box_start_column = column - column % 3 
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_column, box_start_column + 3):
                if val == grid[i, j]:
                    return True
        return False

    def clear_blocks(self, grid: np.ndarray((9,9), np.int8), num_to_clear: int) -> None:
        """
        removes random cells in place

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being worked on
        num_to_clear: int
            the number of cells to clear
        """
        # a set of all possible coordinates
        coordinates = {(i,j) for i in range(9) for j in range(9)}
        for _ in range(num_to_clear):
            val = choice(list(coordinates))
            coordinates.remove(val)
            grid[val[0], val[1]] = 0

    @staticmethod
    def print_board(board: list[list[int]]|np.ndarray((9,9), np.int8)) -> None:
        """
        Displays the board and its content
        if the value is 0, it displays a figure width space

        Parameters
        ----------
        board: list[list[int]]|np.ndarray((9,9), np.int8)
            the board to be printed
        """
        # this is quite stylized and was gotten through lots of trial and error
        # the unicode characters are box character
        char = "\u2533\u2501\u2501\u2501"
        for i, row in enumerate(board):
            if i > 0:
                if i %3 == 0 :
                    char = "\u254b\u2501\u2501\u2501"
                else:
                    char = "\u254b\u2504\u2504\u2504"
            print(" ", char * 9, char[0], sep="" )
            for j, col in enumerate(row):
                terminating = " \u2506 "
                if j%3 == 0:
                    print(' \u2503 ', end="")
                if j == 8:
                    terminating = " \u2503 "
                elif (j + 1) % 3 == 0:
                    terminating = ""
                if col == 0:
                    print("\u2007", end=terminating)
                else:
                    print(col, end=terminating)
            print()
        char = "\u253b\u2501\u2501\u2501"
        print(" ", char * 9, char[0], sep = "")

if __name__ == "__main__":
    a = Generator()
    board = a.generate()
    Generator.print_board(board)