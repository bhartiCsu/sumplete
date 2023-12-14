from typing import List, Tuple

def generate_variables(size: Tuple[int, int]) -> List[str]:
    return ['G{}'.format(i + 1) for i in range(size[0] * size[1])]

def generate_domains(size: Tuple[int, int], grid_values: List[List[int]]) -> dict:
    domains = {}
    for i in range(size[0]):
        for j in range(size[1]):
            variable = 'G{}'.format(i * size[1] + j + 1)
            domains[variable] = [0, grid_values[i][j]]
    return domains

def generate_neighbors(size: Tuple[int, int]):
    neighbors = {}
    for i in range(size[0]):
        for j in range(size[1]):
            current_var = 'G{}'.format(i * size[1] + j + 1)
            neighbor_vars = [current_var]

            # Add neighbors in the same row
            neighbor_vars += ['G{}'.format(i * size[1] + k + 1) for k in range(size[1]) if k != j]

            # Add neighbors in the same column
            neighbor_vars += ['G{}'.format(k * size[1] + j + 1) for k in range(size[0]) if k != i]

            neighbors[current_var] = neighbor_vars

    return neighbors

def generate_constraints(size: Tuple[int, int], grid_values: List[List[int]], row_sums: List[int], col_sums: List[int]) -> dict:
    constraints = {}

    # Unary constraints
    unary_constraints = {}
    for i in range(size[0]):
        for j in range(size[1]):
            variable = 'G{}'.format(i * size[1] + j + 1)
            unary_constraints[variable] = {'0', str(grid_values[i][j])}
    constraints.update(unary_constraints)

    # Binary constraints for row sums
    for i in range(size[0]):
        row_variables = ['G{}'.format(i * size[1] + j + 1) for j in range(size[1])]
        constraint_key = '+'.join(row_variables)
        constraints[constraint_key] = {'S{}'.format(i + 1)}

    # Binary constraints for column sums
    for j in range(size[1]):
        col_variables = ['G{}'.format(i * size[1] + j + 1) for i in range(size[0])]
        constraint_key = '+'.join(col_variables)
        constraints[constraint_key] = {'S{}'.format(size[0] + j + 1)}

    return constraints

def get_sumplete_csp(size: Tuple[int, int], grid_values: List[List[int]], row_sums: List[int], col_sums: List[int]) -> Tuple[List[List[int]], List[int], List[int]]:
    # Generate variables, domains, and constraints
    variables = generate_variables(size)
    domains = generate_domains(size, grid_values)
    constraints = generate_constraints(size, grid_values, row_sums, col_sums)
    neighbors = generate_neighbors(size)
    # Display the generated variables and domains (optional)
    print("Variables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)
    print("Neighbors:", neighbors)
    

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
    get_sumplete_csp(size, grid, row_sums, col_sums)
    

if __name__ == "__main__":
    main()
