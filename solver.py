'''
Solver class for Sudoku puzzles.

Author: Ian Jackson
Date: 08-28-2025
'''

#== Imports ==#
import random
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
        elif self.method == "elimination_plus":
            self._solve_by_elimination_plus()
        elif self.method == "elimination_pro":
            self._solve_by_elimination_pro()
        elif self.method == "random":
            self._solve_by_random()
        else:
            raise ValueError(f"Unknown solving method: {self.method}")
        
    def _solve_by_elimination(self):
        '''
        Solve the puzzle using the elimination method.
        '''
        self._solve_by_elimination_base(use_pairs=False, use_triples=False)

    def _solve_by_elimination_plus(self):
        '''
        Solve puzzle using an enhanced elimination method.
        If stagnation occurs, look for obvious pairs
        '''
        self._solve_by_elimination_base(use_pairs=True, use_triples=False)

    def _solve_by_elimination_pro(self):
        '''
        solve puzzle using elimination method with obvious pairs AND triples
        '''
        self._solve_by_elimination_base(use_pairs=True, use_triples=True)

    def _solve_by_elimination_base(self, use_pairs=False, use_triples=False):
        '''
        Base elimination method that can be configured with different advanced techniques.
        
        Args:
            use_pairs (bool): Whether to use obvious pairs technique
            use_triples (bool): Whether to use obvious triples technique
        '''
        max_iterations_without_progress = 5
        
        while not self.solved and not self.unsolvable:
            self.solver_iterations += 1
            cells_filled_this_iteration = 0
            
            # Basic elimination: iterate all cells in puzzle
            cells_filled_this_iteration += self._perform_basic_elimination()
            
            # Apply advanced techniques if enabled
            if use_pairs:
                cells_filled_this_iteration += self._apply_pairs_technique()
            
            if use_triples:
                cells_filled_this_iteration += self._apply_triples_technique()
            
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

    def _perform_basic_elimination(self):
        '''
        Perform basic elimination for all filled cells and fill cells with single possibilities.
        
        Returns:
            int: Number of cells filled in this iteration
        '''
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
        
        return cells_filled_this_iteration

    def _apply_pairs_technique(self):
        '''
        Apply the obvious pairs technique to all units (rows, columns, boxes).
        
        Returns:
            int: Number of cells filled as a result of this technique
        '''
        cells_filled_this_iteration = 0
        
        # Check for obvious pairs in rows, columns, and boxes
        for unit in self.puzzle.rows + self.puzzle.columns + self.puzzle.boxes:
            # Find all cells with exactly two possible values
            pairs = {}
            for cell in unit.cells:
                if cell.value == 0 and len(cell.possible_values) == 2:
                    key = frozenset(cell.possible_values)
                    if key in pairs:
                        pairs[key].append(cell)
                    else:
                        pairs[key] = [cell]
            
            # If a pair is found in exactly two cells, eliminate those values from other cells
            for key, cells_with_pair in pairs.items():
                if len(cells_with_pair) == 2:
                    for cell in unit.cells:
                        if cell not in cells_with_pair and cell.value == 0:
                            for val in key:
                                if val in cell.possible_values:
                                    cell.remove_possible_value(val)
                                    self.elimination_operations += 1
                                    self.logical_steps += 1
                                    # If this elimination leads to a single possibility, fill it in
                                    if len(cell.possible_values) == 1:
                                        cell.value = cell.possible_values.pop()
                                        self.cells_filled += 1
                                        cells_filled_this_iteration += 1
                                        self.logical_steps += 1
        
        return cells_filled_this_iteration

    def _apply_triples_technique(self):
        '''
        Apply the obvious triples technique to all units (rows, columns, boxes).
        
        Returns:
            int: Number of cells filled as a result of this technique
        '''
        cells_filled_this_iteration = 0
        
        # check for obvious triples in rows, columns, and boxes
        for unit in self.puzzle.rows + self.puzzle.columns + self.puzzle.boxes:
            # Find all cells with exactly three possible values
            triples = {}
            for cell in unit.cells:
                if cell.value == 0 and len(cell.possible_values) == 3:
                    key = frozenset(cell.possible_values)
                    if key in triples:
                        triples[key].append(cell)
                    else:
                        triples[key] = [cell]
            
            # If a triple is found in exactly three cells, eliminate those values from other cells
            for key, cells_with_triple in triples.items():
                if len(cells_with_triple) == 3:
                    for cell in unit.cells:
                        if cell not in cells_with_triple and cell.value == 0:
                            for val in key:
                                if val in cell.possible_values:
                                    cell.remove_possible_value(val)
                                    self.elimination_operations += 1
                                    self.logical_steps += 1
                                    # If this elimination leads to a single possibility, fill it in
                                    if len(cell.possible_values) == 1:
                                        cell.value = cell.possible_values.pop()
                                        self.cells_filled += 1
                                        cells_filled_this_iteration += 1
                                        self.logical_steps += 1
        
        return cells_filled_this_iteration

    def _solve_by_random(self):
        '''
        Solve the puzzle using a random filling method.
        Note: This method is inefficient and primarily for demonstration.
        '''
        max_attempts = 10000  # Prevent infinite loops
        attempt = 0
        
        while not self.solved and not self.unsolvable and attempt < max_attempts:
            self.solver_iterations += 1
            attempt += 1
            cells_filled_this_iteration = 0
            
            # Find all empty cells
            empty_cells = [cell for cell in self.puzzle.cells if cell.value == 0]
            
            if not empty_cells:
                self.solved = True
                break
            
            # Randomly select an empty cell
            target_cell = random.choice(empty_cells)
            
            # Get valid values for this cell (values not in row, column, or box)
            valid_values = self._get_valid_values_for_cell(target_cell)
            
            if valid_values:
                # Randomly select a valid value
                selected_value = random.choice(list(valid_values))
                target_cell.value = selected_value
                target_cell.possible_values = {selected_value}
                
                self.cells_filled += 1
                cells_filled_this_iteration += 1
                self.logical_steps += 1
                
                # Check if puzzle is solved after each placement
                self.solved = self.puzzle.is_solved()
            else:
                # No valid values available - this approach has hit a dead end
                # In a more sophisticated implementation, we would backtrack
                # For this simple random method, we'll mark as unsolvable
                self.unsolvable = True
                break
            
            # Update legacy steps counter
            self.steps = self.cells_filled
        
        # If we've exceeded max attempts, mark as unsolvable
        if attempt >= max_attempts:
            self.unsolvable = True
    
    def _get_valid_values_for_cell(self, cell):
        '''
        Get valid values for a specific cell based on Sudoku constraints.
        
        Args:
            cell (Cell): The cell to check
            
        Returns:
            set: Set of valid values (1-9) for this cell
        '''
        if cell.value != 0:
            return set()  # Cell is already filled
        
        # Start with all possible values
        valid_values = set(range(1, 10))
        
        # Remove values already in the same row
        row = self.puzzle.rows[cell.x_pos_abs]
        for c in row.cells:
            if c.value != 0:
                valid_values.discard(c.value)
        
        # Remove values already in the same column
        col = self.puzzle.columns[cell.y_pos_abs]
        for c in col.cells:
            if c.value != 0:
                valid_values.discard(c.value)
        
        # Remove values already in the same box
        box_id = (cell.x_pos_abs // 3) * 3 + (cell.y_pos_abs // 3)
        box = self.puzzle.boxes[box_id]
        for c in box.cells:
            if c.value != 0:
                valid_values.discard(c.value)
        
        return valid_values

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
