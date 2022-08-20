from solver import Solver
from sudoku import Sudoku
from generator import Generator
from time import time

# feel free to try out the given boards
board1 =[[9,0,0,0,1,0,0,0,5],
        [0,2,0,0,5,3,1,0,0],
        [0,0,0,4,9,0,8,0,2],
        [7,0,2,5,0,0,9,8,4],
        [0,0,1,0,0,9,0,5,0],
        [0,5,9,0,2,7,0,0,3],
        [1,4,5,9,6,0,3,0,0],
        [6,0,0,1,0,5,0,0,9],
        [0,0,8,0,7,0,5,0,0]]

board2 = [[0,0,0,2,6,0,7,0,1],
        [6,8,0,0,7,0,0,9,0],
        [1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0],
        [0,0,4,6,0,2,9,0,0],
        [0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4],
        [0,4,0,0,5,0,0,3,6],
        [7,0,3,0,1,8,0,0,0]]

board2 = [[0,0,0,8,0,0,4,0,3],
         [2,0,0,0,0,4,8,9,0],
         [0,9,0,0,0,0,0,0,2],
         [0,0,0,0,2,9,0,1,0],
         [0,0,0,0,0,0,0,0,0],
         [0,7,0,6,5,0,0,0,0],
         [9,0,0,0,0,0,0,8,0],
         [0,6,2,7,0,0,0,0,1],
         [4,0,3,0,0,6,0,0,0]]

generator = Generator()
Generator.print_board(generator.generate())

# Arto Inkala's Sudoku
hardest_sudoku_ever = [[8,0,0,0,0,0,0,0,0],
                       [0,0,3,6,0,0,0,0,0],
                       [0,7,0,0,9,0,2,0,0],
                       [0,5,0,0,0,7,0,0,0],
                       [0,0,0,0,4,5,7,0,0],
                       [0,0,0,1,0,0,0,3,0],
                       [0,0,1,0,0,0,0,6,8],
                       [0,0,8,5,0,0,0,1,0],
                       [0,9,0,0,0,0,4,0,0]]
hardest_sudoku_solver = Solver()
start = time()
hs1 = hardest_sudoku_solver.solve(hardest_sudoku_ever)
end = time() - start
print(f"Time: {end}")
Solver.print_board(hs1)
assert Solver.validate(hs1)
assert Solver.has_unique_solution(hardest_sudoku_ever)


game = Sudoku()
Sudoku.print_board(game)
Sudoku.print_board(game.solution)