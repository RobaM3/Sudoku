
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diagonals

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    for unit in unitlist:
        for eachBox in unit:
            for otherBoxes in unit:
                if eachBox!=otherBoxes and values[eachBox]==values[otherBoxes] and len(values[otherBoxes])==2:
                    for valRem in unit:
                        if valRem!=otherBoxes and valRem!=eachBox:
                            for num in values[eachBox]:
                                if num in values[valRem]:
                                    values[valRem]=values[valRem].replace(num,'')

    return values
    # TODO: Implement this function!


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solvedBoxes = []
    for box in boxes:
        if len(values[box]) == 1:
            solvedBoxes.append(box)
    for b in solvedBoxes:
        for peer in peers[b]:
            if values[b] in values[peer]:
                values[peer] = values[peer].replace(values[b],'')
                       
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        oldStr=""
        newStr=""
        for box in unit:
            if values[box]!=1:
                oldStr+=values[box]
        for let in oldStr:
            newStr=oldStr
            newStr = newStr.replace(let,'',1)
            if let not in newStr:
                for box in unit:
                    for ans in values[box]:
                        if let == ans:
                            values[box] = let
            
    return values



def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function

    solved = False
    while not solved:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values=eliminate(values)
        values=only_choice(values)
        values=naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        solved = solved_values_after==solved_values_before
        if len([box for box in values.keys() if len(values[box])==0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    
    values=reduce_puzzle(values)
    
    if values is False:
        return False 
    if all(len(values[box])==1 for box in boxes):
        return values
    
    shortest, box = min((len(values[box]), box) for box in boxes if len(values[box])>1)
    

    for num in values[box]:
        newSud = values.copy()
        newSud[box] = num
        newSudSearch = search(newSud)
        if newSudSearch:
            return newSudSearch
    


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
