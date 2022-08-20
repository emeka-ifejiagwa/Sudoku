from __future__ import annotations
import collections
import generator
import numpy as np
class Solver(generator.Generator):
    """
    This class solves ccreates a solver which can solve Sudoku problems

    Staticmethods
    -------------
    has_unique_solution(board: list[list[int]]|np.ndarray((9,9), np.int8)) -> bool
        checks if a given board has unique solutions
    validate(grid: np.ndarray((9,9), np.int8)) -> bool
        validates the solution
    
    Methods
    -------
    solve(self, board: list[list[int]]|np.ndarray((9,9), np.int8)) -> np.ndarray((9,9), np.int8)
        Solves the sudoku problem in-place
    fill(self, grid: np.ndarray((9,9), np.int8) -> bool
        fills in the empty cells
    cache_values(self, grid: np.ndarray((9,9), np.int8)) -> dict
        this returns adictionary of possible values in a certain location
    allowed_values(self, grid: np.ndarray((9,9), np.int8), pos: tuple) -> list
        returns a list of possible/ valid values for a given location
    get_candidates(self, grid: np.ndarray((9,9), np.int8)) -> dict
        gets the candidate of a particular cell
    """

    def allowed_values(self, grid: np.ndarray((9,9), np.int8), pos: tuple) -> list:
        """
        Gets the valid candidates for a particular cell

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being worked on
        pos: tuple
            the coordinates to work on
        
        Returns
        -------
        list
            a list of valid candidates
        """
        available = []
        for num in range(1, 10):
            if self.is_valid(grid, num, pos):
                available.append(num)
        return available

    def get_candidates(self, grid: np.ndarray((9,9), np.int8)) -> dict:
        """
        Finds the candidates for all empty cells

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being worked on
        
        Returns
        -------
        dict
            a dictionary with coordinates as keys and valid candidates as values
        """
        cache = {}
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 0:
                    cache[(i, j)] = self.allowed_values(grid, (i,j))
        return cache #cache is a tuple of positions with a list of candidates

    def cache_values(self, grid: np.ndarray((9,9), np.int8), cache: dict) -> tuple:
        """
        Orders the candidates according to frequency
        If a cell has only one candidate, that candiate is inserted directly

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being evaluated
        cache: dict
            a cache containing positions and candidates

        Returns
        -------
        tuple (bool, dict)
            an indicator for whether a new value was inserted directly into the grid, the cache updated by frequency
        """

        valuesfound = False # stores if we found the correct value of a cell
        # freq_cache stores the positions and frequenceis without the numbers/values
        freq_cache = {}
        colcount = [None for _ in range(9)] # stores the numbers in a particular column and the frequency
        rowcount = [None for _ in range(9)] # stores the numbers in a particular row and the frequency
        boxcount = [None for _ in range(9)] # stores the numbers in a particular subgrid and the frequency
        
        # loop through the the cells in each row and add the frequency for each number
        for row in range(9):
            templist = []
            for col in range(9):
                if (row, col) in cache:
                    templist.extend(cache[(row,col)])
            rowcount[row] = dict(collections.Counter(templist))

        # loop through the the cells in each column and add the frequency for each number
        for col in range(9):
            templist = []
            for row in range(9):
                if (row, col) in cache:
                    templist.extend(cache[(row,col)])
            colcount[col] = dict(collections.Counter(templist))
        
        # loop through the the cells in each subgrid and add the frequency for each number
        # the subgrids are numbered 0 to 8 (the top 3 subgrids, the middle and the last)
        for box_num in range(9):
            templist = []
            box_start_row = 3 * (box_num//3)
            box_start_col = 3 * (box_num % 3)
            for row in range(box_start_row, box_start_row + 3):
                for col in range(box_start_col, box_start_col + 3):
                    if (row, col) in cache:
                        templist.extend(cache[(row,col)])
            boxcount[box_num] = dict(collections.Counter(templist))
            
        # for each cell, if there is a value that is a candidate for only one cell
        # fill it in because if another value is placed in that cell, that value would have no place to be
        for row in range(9):
            for col in range(9):
                templist = []
                box_num = (row //3) * 3 + col//3
                if (row, col) in cache:
                    for val in cache[(row, col)]:
                        # if the a cell's candidate has only that cell as an option, fill it up
                        # note, each columns data occupies the corresponding index in the columns list
                        # this is true for both the row and the box
                        if colcount[col][val] == 1 or rowcount[row][val]== 1 or boxcount[box_num][val] == 1:
                            grid[row,col] = val
                            valuesfound = True
                        else:
                            templist.append(colcount[col][val] + rowcount[row][val] + boxcount[box_num][val])
                    freq_cache[(row, col)] = templist
        # since each key (the position) in the cache corresponds with the that of freq_cache
        # we zip the values together meaning that we make a tuple of the numbers and the corresponding frequencies
        # sort them in order of increasing frequencies
        for k in cache:
            cache[k] =[val for _, val in sorted(zip(freq_cache[k], cache[k]))]
        return cache, valuesfound

    def solve(self, board: list[list[int]]|np.ndarray((9,9), np.int8)) -> np.ndarray((9,9), np.int8):
        """
        Solves the given problem.
        This checks that the given board is valid else an exception is raised

        Parameters
        ----------
        board: list[list[int]]|np.ndarray((9,9), np.int8
            the board to solve

        Returns
        -------
        np.ndarray((9,9), np.int8
            the solved board
        """
        grid = np.array(board)
        # check
        try:
            assert grid.shape == (9,9) # grid is a 9 by 9 board
            assert (grid < 10).all() and (grid > -1).all() # all numbers in grid are valid numbers
        except AssertionError:
            print("Invalid boaard!!")
        # print("Solving")
        # while we find the correct value for a cell, keep caching the values
        # and updating the grid
        found_new_val = True
        while found_new_val:
            candidates = self.get_candidates(grid)
            cache, found_new_val = self.cache_values(grid, candidates)
        if self.fill(grid, cache):
            return grid
        return None

    def fill(self, grid: np.ndarray((9,9), np.int8), cache: dict) -> bool:
        """
        Fills the board with values until a solutiion is found

        Parameters
        ----------
        grid: np.ndarray((9,9), np.int8)
            the grid being solved
        cache: dict
            stores the valid candidates for each empty cell

        Returns
        -------
        bool
            whether or not the board could be solved/filled
        """
        pos = self.next_empty_cell(grid)
        if not pos:
            return True
        x, y = pos
        # rather than checking all values from 1..9, we are checking only the valid ones
        for i in cache[pos]:
            if self.is_valid(grid, i, pos):
                grid[x, y] = i
                if self.fill(grid, cache):
                    return True
                grid[x, y] = 0
        return False

    @staticmethod
    def validate(grid: np.ndarray((9,9), np.int8)) -> bool:
        """
        Validates all values in their current position
        It checks that every value in its corresponding position follows the rules of sudoku

        Parameters
        ----------
        grid: Generator
            the grid to validate

        Returns
        -------
        bool:
            indicates if all values are valid
        """
        ## all the columns, boxes, and rows have to have 1 to 9
        # this means that the sum of all the values there should be 45
        box_sum = 0
        for i in range(9):
            # sum of the row and columns respectively
            if sum(grid[i])  != 45 or sum(grid[:, i]) != 45:
                return False
        
        # sum of the boxes/ subgrids
        # there are 9 3*3 grids, 3 each row and three on each colunn
        # the entire sudoku also be seen as a large subgrid
        for x in range(9):
            box_start_row = 3 * (x//3)
            box_start_column = 3 * (x % 3)
            for i in range(box_start_row, box_start_row + 3):
                for j in range(box_start_column, box_start_column + 3):
                    box_sum += grid[i, j]
            if box_sum != 45:
                return False
            box_sum = 0
        return True

    @staticmethod
    def has_unique_solution(board: list[list[int]]|np.ndarray((9,9), np.int8)) -> bool:
        """
        Checks if a board has a unique solution

        Rarameters
        ----------
        board: list[list[int]]|np.ndarray((9,9), np.int8)
            the board to check
        
        Returns
        -------
        bool
            indicates if a board has a unique solution
        """
        board = np.array(board)
        try:
            assert board.shape == (9,9) # grid is a 9 by 9 board
            assert (board < 10).all() and (board > -1).all() # all numbers in grid are valid numbers
        except AssertionError:
            print("Invalid boaard!!")
        solver = Solver()
        found_new_val = True
        while found_new_val:
            candidates = solver.get_candidates(board)
            cache, found_new_val = solver.cache_values(board, candidates)
        counter = 0
        def unique(grid, cache):
            nonlocal counter
            pos = solver.next_empty_cell(grid)
            # no need to move further if the counter detects another colution
            if counter > 1:
                return False
            if not pos:
                counter += 1
                return False # do not stop when we have found a solution
            x, y = pos
            for i in cache[pos]:
                if solver.is_valid(grid, i, pos):
                    grid[x, y] = i
                    if unique(grid, cache)and counter < 2:
                        return True
                    grid[x, y] = 0
            return False
        unique(board, cache)
        if counter < 2:
            return True
        return False


if __name__ == "__main__":
    game = generator.Generator().generate()
    Solver.print_board(game)
    solver = Solver()
    res = solver.solve(game)
    Solver.print_board(res)
    print(Solver.has_unique_solution(game))
    print(Solver.validate(res))