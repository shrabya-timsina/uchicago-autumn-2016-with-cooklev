#  CS121: Schelling Model of Housing Segregation
#
#   Program for simulating of a variant of Schelling's model of
#   housing segregation.  This program takes four parameters:
#
#    filename -- name of a file containing a sample grid
#
#    R - The radius of the neighborhood: home (i, j) is in the
#        neighborhood of home (k,l) if |k-i| + |l-j| <= R.
#
#    threshold - minimum acceptable threshold for ratio of neighbor
#    value to the total number of homes in his neighborhood.
#
#    max_steps - the maximum number of passes to make over the
#    neighborhood during a simulation.
#
#  Sample use: python3 schelling.py tests/sample-grid.txt 1 0.51 3
#

import os
import sys
import utility


def is_satisfied(grid, R, threshold, location):
    '''
    Is the homeowner at the specified location satisfied?

    Inputs:
        grid: (list of lists of strings) the grid 
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        location: (int, int) a grid location

    Returns:
        True, if the location's neighbor score is at or above the threshold
    '''
    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    # We recommend adding an assertion to check that the location does
    # not contain an open (unoccupied) home.

    # Remove this comment and the next line, if you choose to use this
    # function in your decomposition.
    pass


def do_simulation(grid, R, threshold, max_steps):
    '''
    Do a full simulation.

    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        max_steps: (int) maximum number of steps to do

    Returns:
        The function number of steps executed.
    '''
    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    # YOUR CODE HERE
    # REPLACE 0 with an appropriate return value
    return 0


def go(args):
    '''
    Put it all together: parse the arguments, do the simulation and
    process the results.

    Inputs:
        args: (list of strings) the command-line arguments
    '''

    usage = "usage: python schelling.py <grid file name> <R > 0> <0 < threshold <= 1.0> <max steps >= 0>\n"
    grid = None
    threshold = 0.0
    R = 0
    max_steps = 0
    MAX_SMALL_GRID = 20

    if (len(args) != 5):
        print(usage)
        sys.exit(0)

    # parse and check the arguments
    try:
        grid = utility.read_grid(args[1])

        R = int(args[2])
        if R <= 0:
            print("R must be greater than zero")
            sys.exit(0)

        threshold = float(args[3])
        if (threshold <= 0.0 or threshold > 1.0):
            print("threshold must satisfy: 0 < threshold <= 1.0")
            sys.exit(0)

        max_steps = int(args[4])
        if max_steps <= 0:
            print("max_steps must be greater than or equal to zero")
            sys.exit(0)

    except:
        print(usage)
        sys.exit(0)

    num_steps = do_simulation(grid, R, threshold, max_steps)
    if len(grid) < MAX_SMALL_GRID:
        for row in grid:
            print(row)
    else:
        print("Result grid too large to print")

    print("Number of steps simulated: " + str(num_steps))


if __name__ == "__main__":
    go(sys.argv)
