#  Names: Shrabya Timsina and Steven Cooklev
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

### GRADER COMMENT: Overall function composition. PENALTY: -5

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
 
    
    #unpacking location tuple to get info on row and col of home owner
    (home_row, home_col) = location
    #finding home owner's colour 
    homeowner_colour = grid[home_row][home_col]
   
    
    #ensuring we are not checking an empty house

    ### GRADER COMMENT: It's fine if you want include 
    # your own assertion statements to add another layer
    # of error-checking to your code, but in this case you're
    # asserting over a string, which by inspecting will always
    # return True. Assign home_taken to actual booleans instead
    # of strings if you want to check this next time. PENALTY: -1

    if grid[home_row][home_col] == "R" or grid[home_row][home_col] == "B":
       home_taken = "True"
    else: 
        home_taken = "False"
    assert home_taken
    
    blue_num = 0 #num of ne ighbours of blue colour
    red_num = 0 #num of neighbours of blue colour
    open_num = 0 #num of open homes in neighbourhood
    total_neighbour = 0 #total number of homes in the neighbourhood
    
    #finding neighbours and their colours around the owner's location
    for row in range(max(0, home_row - R), \
        min(home_row + R +1, len(grid))):     #running through rows

        for col in range(max(0, home_col - R), \
            min(home_col + R +1, len(grid))): #running through columns

            neighbour_formula = abs(home_row - row) + abs(home_col - col)

            #checking if neighbour criteria is fulfilled
            if neighbour_formula >= 0 and neighbour_formula <= R:
                total_neighbour = total_neighbour + 1
                
                if grid[row][col] == "B":
                    blue_num = blue_num + 1
                
                elif grid[row][col] == "R":
                    red_num = red_num + 1
                
                else:
                    open_num = open_num + 1

    
    #checking satisfaction score against threshold

    ###GRADER COMMENT: If you're going to handle all 
    # of the different cases for color properties
    # of homeowners ("B", "R", etc) your code will
    # be less scalable and maintainable than if you 
    # are just concerned with matching the homeowner
    # to all of the corresponding neighbors with the 
    # same color property. (i.e. homeowner_color = grid[row][col]
    # instead of expanding into cases). PENALTY: -1

    if homeowner_colour == "B":
        satisfaction = blue_num + (0.5 * open_num)
    else:
        satisfaction = red_num + (0.5 * open_num)

    ### GRADER COMMENT: You can just do 
    # return (satisfaction/total_neighbour >= threshold)

    if (satisfaction/total_neighbour) >= threshold:
        return True
    else:
        return False
       

def find_open_locations(grid):
    '''
    create and initialize the list of open location

    Inputs:
        grid: (list of lists of strings) the grid 
        
    Returns:
        available_homes: a list of tuples of location of unoccupied homes
    '''
    
    # initializing list of unoccupied homes
    available_homes = []
    
    num_row = len(grid)
    num_col = len(grid[0])

    #running loops across rows and then columns of city to find open houses
    for row in range(0, num_row):
        for col in range(0, num_col):
            
            if grid[row][col] == "O":
                open_coords = (row, col)
                available_homes.append(open_coords)

    return available_homes 
            

### GRADER COMMENT: Please choose a better function
# name, e.g. get_disatisfied_owners. PENALTY: -1

def find_dissas_owners(grid, R, threshold):
    '''
    create and initialize the list of unsatisfied homeowners

    Inputs:
        grid: (list of lists of strings) the grid 
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold

    Returns:
        dissas_owners: a list tuples of location of of unsatisfied owners
    '''

    # initializing list of dissastisfied owners
    dissas_owners = []
    
    num_row = len(grid)
    num_col = len(grid[0])

    #loops across rows and then columns of city to find dissastisfied owners
    for row in range(0, num_row):
        for col in range(0, num_col):
            if not grid[row][col] == "O":
                dissas_coords = (row, col)
                satischeck = is_satisfied(grid, R, threshold, dissas_coords)
                ### GRADER COMMENT: Can also say (if !satischeck:)
                if satischeck == False:
                    dissas_owners.append(dissas_coords)

    return dissas_owners

def relocate(grid, R, threshold, available_homes, dissas_owners):
    '''
    attempt to relocate an owner to a new location
    
    Inputs:
        grid: (list of lists of strings) the grid 
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        available_homes: a list of unoccupied homes
        dissas_owners: a list of unsatisfied owners

    Returns:
        grid: list of lists of strings of post-relocation grid
    '''
    ### GRADER COMMENT: You mention that the return value 
    # is an nxn array, but you actually return a boolean, grid_change
    # PENALTY: -1

    grid_change = False

    ### GRADER COMMENT: Be more precise with 
    # variable names. I can infer that dis_own
    # represents disatisfied_owner, but out of 
    # context it isn't always clear.

    for dis_own in dissas_owners:
        (d_row, d_col) = dis_own
        disass_colour = grid[d_row][d_col]

        # Checks if previously unsatisfied homeowners are now satisfied
        #if false then runs the code below
        #if true then goes on to next dissastisfied owner
        satischeck = is_satisfied(grid, R, threshold, dis_own)
        if satischeck == False:

            for homes in available_homes:
                (h_row, h_col) = homes

                #occupying tentatively and then check for satistifaction
                #changing open to new owners colour
                grid[h_row][h_col] = disass_colour 
                #changing dissatisfactory place to open
                grid[d_row][d_col] = "O" 
                
                #check for satistifaction after tentative move
                satischeck = is_satisfied(grid, R, threshold, homes)
                if satischeck == False:
                    #still not satisfied so undoing changes to grid
                    grid[d_row][d_col] = disass_colour #changing back to original colours
                    grid[h_row][h_col] = "O" # changing available home back to open
                    #code now loops to next available location
                    
                else:
                    #locking in the move 
                    #removing new place from open homes list
                    available_homes.remove(homes)
                    #adding original place to open homes list
                    available_homes.insert(0, dis_own)
                    grid_change = True
                    break #goes on to the next dissastisfied owner

       
    
     
    return grid_change
        
def do_simulation(grid, R, threshold, max_steps):
    '''
    Do a full simulation.

    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        max_steps: (int) maximum number of steps to do

    Returns:
        steps or max_steps : The function number of steps executed.
    '''
    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    available_homes = find_open_locations(grid) #getting list of open homes
    #getting pre-simulation list of dissastisfied owners
    dissas_owners = find_dissas_owners(grid, R, threshold) 
    
    for steps in range(0, max_steps):
        #runs one step of the simulation
        perform_step = relocate(grid, R, threshold, available_homes, dissas_owners)
          
        #checks for changes in grid
        #if true then goes on to next step / if false returns num of steps    
        if perform_step == False:
            ### GRADER COMMENT: It's not ideal to return any variable + n,
            # the modifications should occur before the return statement.
            # PENALTY: -1
            return steps + 1
        else:
            dissas_owners = find_dissas_owners(grid, R, threshold)

    return max_steps







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
