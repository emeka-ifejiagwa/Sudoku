import pygame as pg
import sys
from sudoku import Sudoku
from solver import Solver
import numpy as np

grid = Sudoku()
print("SUDOKUU!!!")
correct = set() # used to hold the positon correctly filled cells
# all initially filled cells are correctly filled cells
for i, row in enumerate(grid):
    for j, elem in enumerate(row):
        if elem > 0:
            correct.add((i,j))
image = None # stores the image displayed if the entered value is correct or wrong
wrong = {} # stores the wrong values
notes= {} # stores the notes
FPS = 60 # frames per second
clock = pg.time.Clock()
insert_mode = True # the two modes are insert mode and note mode

screensize = 500, 650
background_color = (0,0,0)
RADIUS = 20
pg.init()
start = pg.time.get_ticks()
screen = pg.display.set_mode(screensize)
pg.display.set_caption("Sudoku")
my_font = pg.font.SysFont("roboto mono", 40)

def draw_background():
    """Draw the bakground"""
    screen.fill(background_color)
    pg.draw.rect(screen, (255,255,255), pg.Rect(25, 25, 450, 450), 4, border_radius= RADIUS)
    for i in range(1, 9):
        width = 1 if i % 3 else 3
        pg.draw.line(screen, (255,255,255), (25, i * 50 + 25), (474, i * 50 + 25), width=width)
        pg.draw.line(screen, (255,255,255), (i * 50 + 25, 25), (i * 50 + 25, 474), width=width)

def get_time(display: bool = True):
    """
    This sets the timer
    
    Parameters
    ----------
    display: bool, optional, default: True
        indicates whether or not to display the timer
    """
    global finish_time
    elapsed = (pg.time.get_ticks() - start) # in milliseconds
    milliseconds = str(elapsed % 1000).zfill(3)
    elapsed//=1000
    sec = str(elapsed % 60).zfill(2)
    mins = str((elapsed // 60) % 60).zfill(2)
    hours = str(elapsed // 3600).zfill(2)
    time_taken = f"{hours} : {mins} : {sec} : {milliseconds}"
    if display:
        timer = my_font.render(time_taken, True, (255,255,255))
        pg.draw.rect(screen, background_color, pg.Rect((500 - timer.get_width())/2, 500, timer.get_width(), timer.get_height()))
        screen.blit(timer, ((500 - timer.get_width())/2, 600))
    return time_taken
    
def draw_numbers():
    """Displays the number"""
    # the current state stores all the entered numbers
    # the code after this ensures that all the correct numbers which were not original
    # are printed in green
    # at first all numbers are printed in green
    # formula for placement: (j + 1) * 50 - 7, (i + 1) * 50 - 12)
    for i, row in enumerate(grid.current_state):
        for j, element in enumerate(row):
            if element != 0:
                text = my_font.render(str(element), True, (150,255,150))
                screen.blit(text, ((j + 1) * 50 - 7, (i + 1) * 50 - 12))  
    # ensures that the numbers in the original grid are printed in the base color 
    for i, row in enumerate(grid.initial_state):
        for j, element in enumerate(row):
            if element != 0:
                text = my_font.render(str(element), True, (255,255,255))
                screen.blit(text, ((j + 1) * 50 - 7, (i + 1) * 50 - 12))
    # ensure that the wrong numbers are printed in red
    for coord in wrong:
        if wrong[coord] != 0:
            i, j = coord
            text = my_font.render(str(wrong[coord]), True, (255,100,100))
            screen.blit(text, ((j + 1) * 50 - 7, (i + 1) * 50 - 12))
    # displays the notes and  blocks all wrong numbers put before
    for i, j in notes:
        # block the previous wrong elements
        pg.draw.rect(screen, background_color, pg.Rect(j * 50 + 25 + 4, i * 50 + 25 + 4, 40, 40),border_radius=20)
        temp_font = pg.font.SysFont("san serif", 30)
        text = temp_font.render(str(notes[(i,j)]), True, (250, 238, 5))
        screen.blit(text, ((j + 1) * 50 - 7, (i + 1) * 50 - 12))


def highlight(pos: tuple):
    """
    Highlights the current row, column and subgrid

    Parameters
    ----------
    pos: tuple
        stores the current location of the mouse
    """
    m_x, m_y = pos
    # the grid occupies coourdinated from (25,25) to (475,475)
    # anything before or after is not in the sudoku grid
    if 25 <= m_x < 475 and 25 <= m_y < 475:
        row_x, row_y = 25, m_y - (m_y - 25) % 50
        col_x, col_y = m_x - (m_x - 25) % 50, 25
        # curve the highlight line if its at the edges
        t_rad = RADIUS if row_y == 25 else -1
        b_rad = RADIUS if row_y == 425 else -1
        pg.draw.rect(screen, (250, 238, 5), pg.Rect(row_x, row_y, 450, 51), width=4,\
            border_top_left_radius=t_rad, border_top_right_radius=t_rad,\
            border_bottom_left_radius= b_rad, border_bottom_right_radius=b_rad)

        l_rad = RADIUS if col_x == 25 else -1
        r_rad = RADIUS if col_x == 425 else -1
        pg.draw.rect(screen, (250, 238, 5), pg.Rect(col_x, col_y, 51, 450), width=4,\
            border_top_left_radius=l_rad, border_top_right_radius=r_rad,\
            border_bottom_left_radius= l_rad, border_bottom_right_radius=r_rad)

        i = (m_x - 25)//50
        j = (m_y - 25)//50
        box_x, box_y = (i - i%3) * 50 + 25, (j - j%3) * 50 + 25
        topleftrad = RADIUS if (i - i%3)  == 0 and (j - j%3) == 0 else -1
        toprightrad = RADIUS if (i - i%3)  == 6 and (j - j%3) == 0 else -1
        buttomleftrad = RADIUS if (i - i%3)  == 0 and (j - j%3) == 6 else -1
        buttomrightrad = RADIUS if (i - i%3)  == 6 and (j - j%3) == 6 else -1
        pg.draw.rect(screen, (250, 238, 5), pg.Rect(box_x, box_y, 150, 150), width=4,\
            border_top_left_radius=topleftrad, border_top_right_radius=toprightrad,\
            border_bottom_left_radius= buttomleftrad, border_bottom_right_radius=buttomrightrad)

def pos_is_filled(m_pos: tuple):
    """
    Checks if the position is correctly filled
    
    Parameters
    ----------
    m_pos: tuple
        the mouse coordinates
    
    Returns
    -------
    bool
        indicates if the the position is filled
    """
    m_x, m_y = m_pos
    if (25 < m_x < 475) and (25 < m_y < 475):
        # convert these coordinates to the location of the 9*9 sudoku grid
        m_x = (m_x - 25)//50
        m_y = (m_y - 25)//50
        if (m_y, m_x) in correct:
            return True
        return False
    return True

def check(coord: tuple, val: int):
    """
    Checks if the value placed in the provided location is correct
    
    Parameters
    ----------
    coord: tuple
        the sudoku location on the grid
    val: int
        the value to check
    """
    global image
    x, y = coord
    # if the value is correct display a tick meaning its correct
    # add it to the set of correctly placed values
    # and remove from wrong
    # else display an X
    if grid.solution[x][y] == val:
        correct.add((x,y))
        # everything is put into wrong until it is verified
        wrong.pop((x,y))
        image = pg.image.load("images/tick.png", "Correct!")
        image = pg.transform.scale(image, (image.get_width()/10, image.get_height()/10))
    else:
        image = pg.image.load("images/x.png", "Wrong!")
        image = pg.transform.scale(image, (image.get_width()/10, image.get_height()/10))


def insert():
    """Inserts the typed number into the Sudoku's current state"""
    while True:
        pos = pg.mouse.get_pos()
        m_x, m_y = pos
        # convert the mouse position to positions on the sudoku
        m_x = (m_x - 25)//50
        m_y = (m_y - 25)//50
        for event in pg.event.get():
            if pos_is_filled(pos):
                return
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return
                if event.key == pg.K_0:
                    # hitting ) clears the cell content if it is wrong or if it's a note
                    if (m_y, m_x) in notes:
                        notes.pop((m_y, m_x))
                    if (m_y, m_x) in wrong:
                        wrong.pop((m_y, m_x))
                    grid.current_state[m_y][m_x] = 0
                elif pg.K_0 < event.key <= pg.K_9:
                    # if we had a note at that location, remove it
                    if (m_y, m_x) in notes:
                        notes.pop((m_y, m_x))
                    val = event.key - 48
                    grid.current_state[m_y][m_x] = val
                    wrong[(m_y, m_x)] = val
                    check((m_y, m_x), val)
                return
            return
                
def note():
    """Allows users to note one number per block"""
    global image
    
    while True:
        pos = pg.mouse.get_pos()
        m_x, m_y = pos
        m_x = (m_x - 25)//50
        m_y = (m_y - 25)//50
        image = None # if we are taking notes, no tick or X should be shown
        for event in pg.event.get():
            # if the position is already filled correctly
            # n o need to note
            if pos_is_filled(pos):
                return
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE or event.key == pg.K_0:
                    if (m_y, m_x) in notes:
                        notes.pop((m_y, m_x))
                elif pg.K_0 < event.key <= pg.K_9:
                    # if the location was wrongly filled, repplace it with a note
                    notes[(m_y, m_x)] = event.key - 48
                    grid.current_state[m_y][m_x] = 0 # remove any wrong value placed there
                    if (m_y, m_x) in wrong:
                        wrong.pop((m_y, m_x))
                elif event.key == pg.K_RETURN and (m_y, m_x) in notes:
                    val = notes.pop((m_y, m_x))
                    grid.current_state[m_y][m_x] = val
                    wrong[(m_y, m_x)] = val
                    check((m_y, m_x), val)
                return
            return
                
def complete():
    """Displays time taken"""
    pg.draw.rect(screen, background_color, pg.Rect(0,0, screen.get_width(), screen.get_height()))
    text = f"WELL DONE!!!"
    time = f"TIME TAKEN: {get_time(display = False)}"
    end_text = my_font.render(text, True, (150,255,150))
    screen.blit(end_text, ((screen.get_width() - end_text.get_width())/2, (screen.get_height() - end_text.get_height())/2 - 50))
    end_text = my_font.render(time, True, (150,255,150))
    screen.blit(end_text, ((screen.get_width() - end_text.get_width())/2, (screen.get_height() - end_text.get_height())/2))
    pg.display.flip()
    pg.time.delay(3000)
    sys.exit()

def solve():
    notes.clear()
    wrong.clear()
    grid.current_state =  np.array(grid.initial_state)
    draw_background()
    draw_numbers()
    solver = Solver()
    candidates = solver.get_candidates(grid.current_state)
    if fill(solver, grid.current_state, solver.cache_values(grid.current_state, candidates)[0]):
        assert solver.validate(grid.current_state)
        pg.time.delay(2000)
        sys.exit()
    
def fill(solver, grid, cache):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    pos = solver.next_empty_cell(grid, row_by_row = True)
    if not pos:
        return True
    x, y = pos
    # rather than going thrugh to see if there are any other solutions
    available = cache[pos]
    for i in available:
        if solver.is_valid(grid, i, pos):
            grid[x][y] = i
            draw_background()
            draw_numbers()
            topleftrad, toprightrad, buttomleftrad, buttomrightrad = -1, -1, -1, -1
            if x == 0 and y == 0:
                topleftrad = 20
            elif x == 0 and y == 8:
                toprightrad = 20
            elif x == 8 and y == 0:
                buttomleftrad = 20
            elif x == 8 and y == 8:
                buttomrightrad = 20
            pg.draw.rect(screen, (255, 255, 0), pg.Rect(y * 50 + 25, x * 50 + 25, 50, 50), 3,\
                border_top_left_radius=topleftrad, border_top_right_radius=toprightrad,\
                    border_bottom_left_radius=buttomleftrad, border_bottom_right_radius=buttomrightrad)
            pg.display.flip()
            pg.time.delay(75)
            if fill(solver, grid, cache):
                return True
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(y * 50 + 25, x * 50 + 25, 50, 50), 3,\
                border_top_left_radius=topleftrad, border_top_right_radius=toprightrad,\
                    border_bottom_left_radius=buttomleftrad, border_bottom_right_radius=buttomrightrad)
            pg.display.flip()
            pg.time.delay(50)
            grid[x][y] = 0
    return False


def game_loop():
    global insert_mode
    clock.tick(FPS)
    draw_background()
    draw_numbers()
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_n:
            insert_mode = not insert_mode
        if event.type == pg.MOUSEBUTTONUP:
            if insert_mode:
                insert()
            else:
                note()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            solve()
    highlight(pg.mouse.get_pos())
    get_time()
    # indicates the mode for the user
    mode = my_font.render("NOTE MODE", True, (255,255,255)) if not insert_mode else my_font.render("INSERT MODE", True, (255,255,255))
    screen.blit(mode, ((500 - mode.get_width())/2, 570))
    if image:
        screen.blit(image, ((500 - image.get_width())/2,500))
    if len(correct) == 81:
        assert Solver().validate(grid.current_state)
        complete()
    pg.display.flip()

while True:
    game_loop()