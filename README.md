# COMP131_Sudoku
Sudoku Solver | COMP131 | HW3
Vladimir Porokhin and Victor Arsenescu


Each board was implemented as a list of length 81. This made it easier to
isolate an individual cell's row, column, and region (3x3 grid). 

To make it more efficient to store and adjust each cell's domain, domains
were represented as an int whose ith bit was set to 1 if 1 + i (<= 9) was
a possible value for that cell. 

With these elements in place, the board was solved with recursive backtracking.
At each iteration, a new set of domains was generated for all the cells on the 
board by looping through all the cells in each "house" (row + col + region)
and only keeping values in the domain that do not exist elsewhere in the house.

Once the new board has been computed, a technique called "hidden singles" is used
to futher prune the domains. This works by iterating through all cells in each
house and checking if any cell in each house has a unique value in its domain - 
that is, if one cell has a value in its domain that no other cell in the house
has. If we find this to be the case, (and only in this case), we set the value
of the cell to that unique value and recursively call solveBoard after taking
another "step" (just a way of tracking where we are).

This could potentially solve the puzzle. If it does not (as in the hard case), 
the cells are sorted by the number of potential values in their domain (minimum
remaining value heuristic) and the value of the cell with the fewest values
available is guessed (usually good odds, since minimum is often 2 or 3 values).
The cell's value is then set to that guess, and an attempt is made to solve the
board by recursively calling solveBoard after taking another step. If that fails,
the next guess is made, etc.

