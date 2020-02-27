from random import seed, shuffle, choice
from copy import deepcopy

'''
A brute force algorithm visits the empty cells in some order, filling in digits sequentially, or backtracking when the number is found to be not valid.
Briefly, a program would solve a puzzle by placing the digit "1" in the first cell and checking if it is allowed to be there. 
If there are no violations (checking row, column, and box constraints) then the algorithm advances to the next cell and places a "1" in that cell. 
When checking for violations, if it is discovered that the "1" is not allowed, the value is advanced to "2". 
If a cell is discovered where none of the 9 digits is allowed, then the algorithm leaves that cell blank and moves back to the previous cell. 
The value in that cell is then incremented by one. This is repeated until the allowed value in the last (81st) cell is discovered.
'''

"""
Find row, col of an unassigned cell
If there is none, return true
For digits from 1 to 9
  a) If there is no conflict for digit at row, col
      assign digit to row, col and recursively try fill in rest of grid
  b) If recursion successful, return true
  c) Else, remove digit and try another
If all digits have been tried and nothing worked, return false
  """


def print_grid(grid):
    s = ""
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            s += "{}{} ".format(" " if (num <= 9 or type(num)
                                        == str) else "", num)
        s += '\n'
    print(s)


def grid_full(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True


def number_already_in_box(grid, corner_row, corner_col, number):
    for row in range(3):
        for col in range(3):
            if grid[corner_row + row][corner_col + col] == number:
                return True
    return False


def find_unassigned_space(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)


def isValidMove(number, row, col, grid):
    # check row
    if number in grid[row]:
        return False
    # check column
    if any(number == grid[x][col] for x in range(9)):
        return False
    # check 3x3 box
    if number_already_in_box(grid, row - row % 3, col - col % 3, number):
        return False
    # all checks have passed, then it's valid
    return True


def solve(grid):
    seed()
    if grid_full(grid):
        return True

    row, col = find_unassigned_space(grid)
    numbers = list(range(1, 10))
    shuffle(numbers)
    for number in numbers:
        if isValidMove(number, row, col, grid):
            grid[row][col] = number
            if grid_full(grid):
                return True
            if solve(grid):
                return True
            # unsuccessful
            grid[row][col] = 0
    return False


def generate_puzzle(clues=17):
    if clues < 17:
        clues = 17

    # first create a solution
    solution = [[0 for i in range(9)] for j in range(9)]
    solve(solution)

    # create a copy
    clues_needed = 81 - clues
    grid = deepcopy(solution)
    while(clues_needed > 0):
        seed()
        test_grid = deepcopy(grid)
        next_removal = False
        while not next_removal:
            row = choice(range(9))
            col = choice(range(9))
            if grid[row][col] != "_":
                next_removal = True
        test_grid[row][col] = 0
        if solve(test_grid):
            grid[row][col] = "_"
            clues_needed -= 1

    print("Puzzle:")
    print_grid(grid)
    print("\nSolution:")
    print_grid(solution)
    return grid


if __name__ == '__main__':
    puzzle = generate_puzzle(clues=25)
