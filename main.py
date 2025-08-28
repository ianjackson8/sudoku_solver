'''
Sudoku Solver

This script solves a given Sudoku puzzle

Author: Ian Jackson
Date 08-27-2025
Version 0.1
'''

#== Imports ==#
import puzzle

#== Global Variables ==#


#== Functions ==#


#== Main Code ==#
def main():
    grid = [[0,1,0, 0,8,6, 0,3,2],
            [0,2,0, 0,0,9, 6,5,0],
            [6,0,3, 0,0,0, 9,1,0],

            [0,0,1, 5,4,3, 2,0,6],
            [0,4,0, 0,2,0, 0,8,1],
            [2,5,0, 1,0,0, 0,0,0],

            [7,0,0, 0,0,5, 0,0,0],
            [1,0,0, 0,7,0, 8,6,5],
            [0,9,8, 0,0,1, 3,0,4]]
    
    puz = puzzle.Puzzle(grid)
    puz.display()

    print()
    # Test the position (0,4) as requested
    x = 0
    y = 4
    sample_cell = puz.get_cell(x,y)
    print(f"Testing position ({x},{y}) which should have value 8:")
    print(f"Cell: {sample_cell.value}\nPossible Values: {sample_cell.possible_values}\nRelative Position: ({sample_cell.x_pos_rel}, {sample_cell.y_pos_rel})\nAbsolute Position: ({sample_cell.x_pos_abs}, {sample_cell.y_pos_abs})\nBox ID: {puz.get_box_id(x,y)}\nRow ID: {puz.get_row_id(x,y)}\nColumn ID: {puz.get_column_id(x,y)}")

    print()
    for i in range(81):
        cell = puz.cells[i]
        print(f"Cell {i}: Value: {cell.value}, ({cell.x_pos_abs}, {cell.y_pos_abs})")

if __name__ == "__main__":
    main()