from typing import List, Tuple
import itertools

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

def is_valid_grid_size(size: Tuple[int, int]) -> bool:
    valid_sizes = [(3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
    return size in valid_sizes

def get_grid_values(size: Tuple[int, int]) -> Tuple[List[List[int]], List[int], List[int]]:
    # Initialize grid
    grid = [[0] * size[1] for _ in range(size[0])]

    # Input values for each grid
    print("\nPlease input values for each grid ({}X{} format):".format(size[0], size[1]))
    for i in range(size[0]):
        for j in range(size[1]):
            while True:
                try:
                    value = int(input("Enter value for G{}: ".format(i * size[1] + j + 1)))
                    grid[i][j] = value
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

    # Input target row sums
    print("\nPlease input target row sums (S1 to S{}):".format(size[0]))

    row_sums = [0] * size[0]
    for i in range(size[0]):
        while True:
            try:
                value = int(input("Enter value for S{}: ".format(i + 1)))
                row_sums[i] = value
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    # Input target column sums
    print("\nPlease input target column sums (S{} to S{}):".format(size[0] + 1, 2 * size[1]))
    col_sums = [0] * size[1]
    for j in range(size[1]):
        while True:
            try:
                value = int(input("Enter value for S{}: ".format(size[0] + j + 1)))
                col_sums[j] = value
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    return grid, row_sums, col_sums

def display_grid_format(size: Tuple[int, int]):
    print("Grid Format:")
    for i in range(size[0]):
        for j in range(size[1]):
            print("G{}  ".format(i * size[1] + j + 1), end="")
        print("S{}".format(i + 1))

    for j in range(size[1]):
        print("S{}".format(size[0] + j + 1), end="  ")

    print("\n")
    
def main():
    # Get grid size from user
    while True:
        try:
            grid_size_input = input("Enter the grid size (e.g., 3X3, 4X4, 5X5, 6X6, 7X7, 8X8, or 9X9): ").lower()
            size = tuple(map(int, grid_size_input.split("x")))
            if is_valid_grid_size(size):
                break
            else:
                print("Invalid grid size. Please enter a valid size.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid grid size.")

   
    # Display the grid format
    display_grid_format(size)

    # Get grid values, row sums, and column sums from the user
    grid, row_sums, col_sums = get_grid_values(size)
    
 
    # Display the entered values
    print("\nEntered values:")
    print("Grid:")
    for row in grid:
        print(row)
    print("Row Sums:", row_sums)
    print("Column Sums:", col_sums)
    solve_sumplete(grid, row_sums, col_sums)
    print(grid)
    

if __name__ == "__main__":
    main()
