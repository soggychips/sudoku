from random import seed, shuffle, choice
from copy import deepcopy


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
