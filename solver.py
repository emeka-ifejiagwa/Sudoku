from __future__ import annotations
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
    llowed_values(self, grid: np.ndarray((9,9), np.int8), pos: tuple) -> list
        returns a list of possible/ valid values for a given location
    """

    def cache_values(self, grid: np.ndarray((9,9), np.int8)) -> dict:
        """
        This returns a given loaction and the valid values for that location

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
        return cache

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

    def solve(self, board: list[list[int]]|np.ndarray((9,9), np.int8), descending: bool= False) -> np.ndarray((9,9), np.int8):
        """
        Solves the given problem.
        This checks that the given board is valid else an exception is raised

        Parameters
        ----------
        board: list[list[int]]|np.ndarray((9,9), np.int8
            the board to solve
        descending: optional, bool default: False
            determines how to the guesses
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
        print("Solving")
        if self.fill(grid, self.cache_values(grid), descending):
            return grid
        return None

    def fill(self, grid: np.ndarray((9,9), np.int8), cache: dict, descending: bool = False) -> bool:
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
        
        available = cache[pos] if not descending else reversed(cache[pos])
        # rather than checking all values from 1..9, we are checking only the valid ones
        for i in available:
            if self.is_valid(grid, i, pos):
                grid[x, y] = i
                if self.fill(grid, cache, descending):
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
        solver = Solver()
        # the intuition here is that if there is a unique solution, solving using values of 1..9 
        # and solving using values from 9..1 should approach the same values
        # so far, i my tests, this works, but it only takes one wrong result to disporve this method
        solution1 = solver.solve(board)
        solution2 = solver.solve(board, descending=True)
        return np.array_equal(solution1, solution2)


if __name__ == "__main__":
    game = generator.Generator().generate()
    Solver.print_board(game)
    solver = Solver()
    res = solver.solve(game)
    Solver.print_board(res)
    print(Solver.has_unique_solution(game))
    print(Solver.validate(res))
