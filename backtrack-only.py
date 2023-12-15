def is_valid_solution(grid, row_sums, col_sums):
    # Check if the sum of each row and column matches the target
    for i in range(len(grid)):
        if sum(grid[i][j] for j in range(len(grid)) if grid[i][j] != 'X') != row_sums[i]:
            return False
        if sum(grid[j][i] for j in range(len(grid)) if grid[j][i] != 'X') != col_sums[i]:
            return False
    return True

def solve_sumplete(grid, row_sums, col_sums, cell=0):
    if cell == len(grid)**2:
        return is_valid_solution(grid, row_sums, col_sums)

    row, col = divmod(cell, len(grid))

    # Try deleting the number
    original_value = grid[row][col]
    grid[row][col] = 'X'
    if solve_sumplete(grid, row_sums, col_sums, cell + 1):
        return True

    # Backtrack
    grid[row][col] = original_value
    return solve_sumplete(grid, row_sums, col_sums, cell + 1)

grid = [
    [9, 8, 3],
    [6, 6, 3],
    [3, 8, 8]
]
row_sums = [12, 9, 0]
col_sums = [9, 6, 6]

grid2 = [
    [8, 2, 9],
    [2, 9, 5],
    [1, 7, 4]
]
row_sums2 = [11, 2, 5]
col_sums2 = [3, 2, 13]

solve_sumplete(grid, row_sums, col_sums)
print(grid)
solve_sumplete(grid2, row_sums2, col_sums2)
print(grid2)
