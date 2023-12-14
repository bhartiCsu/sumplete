
"""

 (             *     (    (                       (        )   (                 (
 )\ )        (  `    )\ ) )\ )        *   )       )\ )  ( /(   )\ )              )\ )
(()/(    (   )\))(  (()/((()/(  (   ` )  /( (    (()/(  )\()) (()/( (   (   (   (()/(
 /(_))   )\ ((_)()\  /(_))/(_)) )\   ( )(_)))\    /(_))((_)\   /(_)))\  )\  )\   /(_))
(_))  _ ((_)(_()((_)(_)) (_))  ((_) (_(_())((_)  (_))    ((_) (_)) ((_)((_)((_) (_))
/ __|| | | ||  \/  || _ \| |   | __||_   _|| __| / __|  / _ \ | |  \ \ / / | __|| _ \
\__ \| |_| || |\/| ||  _/| |__ | _|   | |  | _|  \__ \ | (_) || |__ \ V /  | _| |   /
|___/ \___/ |_|  |_||_|  |____||___|  |_|  |___| |___/  \___/ |____| \_/   |___||_|_\



This Python script implements a Constraint Satisfaction Problem (CSP) solver for a grid puzzle. 
The puzzle involves filling a grid with values while satisfying row and column sum constraints.
The script defines functions for CSP initialization, variable ordering, consistency checking, 
domain reduction, and backtracking search. It also provides functions for generating variables, 
domains, neighbors, and constraints based on user input. The main function prompts the user to 
input the puzzle size, grid values, and target sums. The script then solves the puzzle using 
the CSP solver and displays the solution or indicates if no solution is found.





"""



from typing import List, Tuple


def initialize_variables(variables, domains, constraints, neighbors):
    assignment = {}
    for var in variables:
        assignment[var] = domains[var][0]  # Initialize with the first value in the domain
        if not is_consistent(var, assignment[var], assignment, constraints, domains, neighbors):
            # If constraints are not satisfied, backtrack and try the second value
            assignment[var] = domains[var][1]
    return assignment

def order_variables(variables, domains):
    return sorted(variables, key=lambda var: len(domains[var]))

def is_consistent(variable, value, assignment, constraints, domains, neighbors):
    # Check unary constraints
    if variable in constraints and value not in constraints[variable]:
        return False

    # Check binary constraints
    for neighbor in neighbors[variable]:
        if neighbor in assignment:
            if (neighbor, value, variable, assignment[neighbor]) in constraints:
                return False
            if (variable, value, neighbor, assignment[neighbor]) in constraints:
                return False

    return True

def reduce_domain(variable, value, domains, assignment, constraints):
    reduced_domain = [v for v in domains[variable] if is_consistent(variable, v, assignment, constraints, domains)]
    return reduced_domain

def assign_value(variable, value, assignment):
    assignment[variable] = value

def forward_check(variable, value, domains, assignment, constraints):
    for neighbor in domains[variable]:
        if neighbor not in assignment:
            domains[neighbor] = reduce_domain(neighbor, value, domains, assignment, constraints)
            
def select_unassigned_variable(assignment, variables, domains):
    unassigned_variables = [var for var in variables if not assignment[var]]
    return unassigned_variables[0] if unassigned_variables else None

def order_domain_values(variable, domains, assignment, constraints):
    # You can implement your own value ordering heuristic here.
    return domains[variable]

def backtrack_search(assignment, variables, domains, constraints, neighbors):
    if all(assignment[var] for var in variables):
        return assignment  # Solution found

    var = select_unassigned_variable(assignment, variables, domains)
    ordered_values = order_domain_values(var, domains, assignment, constraints)

    for value in ordered_values:
        if is_consistent(var, value, assignment, constraints, domains, neighbors):
            assign_value(var, value, assignment)
            forward_check(var, value, domains, assignment, constraints)

            result = backtrack_search(assignment, variables, domains, constraints, neighbors)
            if result:
                return result  # Solution found

            # Backtrack
            assignment[var] = ''
            for neighbor in domains[var]:
                if neighbor not in assignment:
                    domains[neighbor] = reduce_domain(neighbor, value, domains, assignment, constraints)

    return None  # No solution


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

    # Unary constraints for grid values
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
        constraints[constraint_key] = {str(row_sums[i])}

    # Binary constraints for column sums
    for j in range(size[1]):
        col_variables = ['G{}'.format(i * size[1] + j + 1) for i in range(size[0])]
        constraint_key = '+'.join(col_variables)
        constraints[constraint_key] = {str(col_sums[j])}

    return constraints

def get_sumplete_csp(size: Tuple[int, int], grid_values: List[List[int]], row_sums: List[int], col_sums: List[int]) -> Tuple[List[List[int]], List[int], List[int]]:
    # Generate variables, domains, and constraints
    variables = generate_variables(size)
    domains = generate_domains(size, grid_values)
    constraints = generate_constraints(size, grid_values, row_sums, col_sums)
    neighbors = generate_neighbors(size)
    assignment = initialize_variables(variables, domains, constraints, neighbors)
    result = backtrack_search(assignment, variables, domains, constraints, neighbors)
    # Display the generated variables and domains (optional)
    print("Variables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)
    print("Neighbors:", neighbors)
    print("Result:", result)
    
    if result:
        print("Solution found:")
        for var, value in result.items():
            print("{var}: {value}")
    else:
        print("No solution found.")
    

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
