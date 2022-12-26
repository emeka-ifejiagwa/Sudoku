from solver import Solver
import numpy as np
from generator import Generator
class Sudoku:
    """
    This is the sudoku game itself
    The game generated is almost always guaranteed to have a unique solution

    Attributes
    ----------
    initial_state: np.ndarray((9,9), np.int8)
        stores the given problem
        Note: This value should never be changed for a given sudoku
    current_state: np.ndarray((9,9), np.int8)
        stores the current state of the sudoku as the user attempts to solve
    solution: np.ndarray((9,9), np.int8)
        stores the solver used to generate the solution
    counter: int
        the counter used by the iterator
    
    Staticmethods
    -------------
    print_board(board) -> None
        displays the sudoku grid
    """

    def __init__(self):
        problem = Generator().generate()
        print("Generating...")
        while not Solver.has_unique_solution(problem):
            # randomly choose from the api or from the generator
            problem = Generator().generate()
            print("Generating...")
        self.initial_state = problem
        self.current_state = np.array(problem) # adeep copy of the problem as this would change constantly
        self.solution = Solver().solve(problem)
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= len(self.current_state):
            self.counter = 0
            raise StopIteration
        obj = self.current_state[self.counter]
        self.counter += 1
        return obj
    
    @staticmethod
    def print_board(board) -> None:
        """
        Displays the sudoku board in a stylized manner

        Parameters
        ----------
        board: Sudoku
            the sudoku board to be printed
        """
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
                # if value is zero, print figure wide space
                if col == 0:
                    print("\u2007", end=terminating)
                else:
                    print(col, end=terminating)
            print()
        char = "\u253b\u2501\u2501\u2501"
        print(" ", char * 9, char[0], sep = "")

if __name__ == "__main__":
    grid = Sudoku()
    Sudoku.print_board(grid)
    Sudoku.print_board(grid.initial_state)
    Sudoku.print_board(grid.current_state)
    Sudoku.print_board(grid.solution)