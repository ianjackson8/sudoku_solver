'''
Solver class for Sudoku puzzles.

Author: Ian Jackson
Date: 08-28-2025
'''

#== Imports ==#
from puzzle import Puzzle, Cell, Box, Row

#== Global Variables ==#


#== Classes ==#
class Solver:
    def __init__(self, puzzle: Puzzle, method: str = "elimination"):
        '''
        Initialize the Solver with a given Puzzle.
        Args:
            puzzle (Puzzle): The Sudoku puzzle to solve.
            method (str, optional): The solving method to use. Defaults to "elimination".
        '''
        self.puzzle = puzzle
        self.method = method

        # Enhanced step tracking
        self.steps = 0  # Keep for backward compatibility
        self.cells_filled = 0  # Number of cells actually filled
        self.elimination_operations = 0  # Number of constraint eliminations
        self.solver_iterations = 0  # Number of complete puzzle passes
        self.logical_steps = 0  # Number of logical reasoning steps
        self.solved = False
        self.unsolvable = False  # Track if puzzle is unsolvable
        self.iterations_without_progress = 0  # Track stagnant iterations

    def solve(self):
        '''
        Solve the Sudoku puzzle using the specified method.
        '''
        if self.method == "elimination":
            self._solve_by_elimination()
        else:
            raise ValueError(f"Unknown solving method: {self.method}")
        
    def _solve_by_elimination(self):
        '''
        Solve the puzzle using the elimination method.
        '''
        max_iterations_without_progress = 5
        
        while not self.solved and not self.unsolvable:
            self.solver_iterations += 1
            cells_filled_this_iteration = 0
            
            # iterate all cells in puzzle
            for i in range(81):
                # if the cell is filled in, get the data
                cell = self.puzzle.cells[i]
                if cell.value != 0:
                    self.logical_steps += 1  # Count each logical reasoning step
                    val = cell.value
                    x_pos = cell.x_pos_abs
                    y_pos = cell.y_pos_abs

                    # eliminate this value from all cells in the same row
                    row = self.puzzle.rows[x_pos]
                    for c in row.cells:
                        if val in c.possible_values:
                            c.remove_possible_value(val)
                            self.elimination_operations += 1

                    # eliminate this value from all cells in the same column
                    col = self.puzzle.columns[y_pos]
                    for c in col.cells:
                        if val in c.possible_values:
                            c.remove_possible_value(val)
                            self.elimination_operations += 1

                    # eliminate this value from all cells in the same box
                    box_id = (x_pos // 3) * 3 + (y_pos // 3)
                    box = self.puzzle.boxes[box_id]
                    for c in box.cells:
                        if val in c.possible_values:
                            c.remove_possible_value(val)
                            self.elimination_operations += 1

            # After elimination, fill in cells with a single possible value
            for cell in self.puzzle.cells:
                if cell.value == 0 and len(cell.possible_values) == 1:
                    cell.value = cell.possible_values.pop()
                    self.cells_filled += 1
                    cells_filled_this_iteration += 1
                    
            # Update legacy steps counter (for backward compatibility)
            self.steps = self.cells_filled
            
            # Check for progress and handle stagnation
            if cells_filled_this_iteration == 0:
                self.iterations_without_progress += 1
                if self.iterations_without_progress >= max_iterations_without_progress:
                    self.unsolvable = True
                    break
            else:
                # Reset counter if we made progress
                self.iterations_without_progress = 0

            # Check if the puzzle is solved
            self.solved = self.puzzle.is_solved()

    def get_detailed_stats(self):
        '''
        Get detailed solving statistics.
        
        Returns:
            dict: Dictionary containing various solving metrics
        '''
        return {
            'cells_filled': self.cells_filled,
            'elimination_operations': self.elimination_operations,
            'solver_iterations': self.solver_iterations,
            'logical_steps': self.logical_steps,
            'total_reasoning_operations': self.logical_steps + self.elimination_operations,
            'efficiency_ratio': self.cells_filled / max(1, self.solver_iterations),
            'eliminations_per_cell': self.elimination_operations / max(1, self.cells_filled),
            'unsolvable': self.unsolvable,
            'iterations_without_progress': self.iterations_without_progress
        }
