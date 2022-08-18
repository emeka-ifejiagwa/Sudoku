import numpy as np
import requests

# https://sudoku-api.vercel.app
# this website offered a means to generate sudoku boards with unique solutions
# I attempted to create a generator but it was too slow 
# and could take up to 10 minutes to generate one
def generate():
    url = "https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}"
    my_req = requests.get(url)
    numbers = []
    if my_req.status_code == 200:
        text = my_req.text
        for letter in text:
            if letter.isdigit():
                numbers.append(int(letter))
    return np.reshape(numbers, (9,9))

if __name__ == "__main__":
    print(generate())