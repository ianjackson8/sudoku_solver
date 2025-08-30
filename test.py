#!/usr/bin/env python3
'''
Test script to benchmark all solving methods against all puzzle files.

Author: Ian Jackson
Date: 08-29-2025
'''

import os
import glob
from puzzle import Puzzle
from solver import Solver

def load_puzzle_from_file(filepath):
    '''
    Load a puzzle from a text file.
    
    Args:
        filepath (str): Path to the puzzle file
        
    Returns:
        Puzzle: The loaded puzzle object
    '''
    grid = []
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.isspace():  # Skip empty lines
                row = [int(char) for char in line]
                grid.append(row)
    
    return Puzzle(grid)

def run_solver_test(puzzle, method):
    '''
    Run a solver test on a puzzle with a specific method.
    
    Args:
        puzzle (Puzzle): The puzzle to solve
        method (str): The solving method to use
        
    Returns:
        dict: Results including efficiency ratio and cells filled
    '''
    # Create a deep copy of the puzzle for each test
    # We'll recreate from the original grid to ensure clean state
    original_grid = [[puzzle.cells[row * 9 + col].value for col in range(9)] for row in range(9)]
    test_puzzle = Puzzle(original_grid)
    
    solver = Solver(test_puzzle, method=method)
    solver.solve()
    
    stats = solver.get_detailed_stats()
    
    return {
        'cells_filled': stats['cells_filled'],
        'efficiency_ratio': round(stats['efficiency_ratio'], 3),
        'solved': solver.solved,
        'unsolvable': stats['unsolvable'],
        'solver_iterations': stats['solver_iterations'],
        'logical_steps': stats['logical_steps']
    }

def main():
    '''
    Main function to run all tests and display results.
    '''
    # Define the solving methods to test
    methods = ['elimination', 'elimination_plus', 'elimination_pro', 'random']
    
    # Find all puzzle files
    puzzle_dir = 'puzzles'
    puzzle_files = glob.glob(os.path.join(puzzle_dir, '*.txt'))
    puzzle_files.sort()  # Sort for consistent ordering
    
    if not puzzle_files:
        print(f"No puzzle files found in {puzzle_dir} directory!")
        return
    
    # Load all puzzles
    puzzles = {}
    for filepath in puzzle_files:
        filename = os.path.basename(filepath)
        puzzle_name = os.path.splitext(filename)[0]
        try:
            puzzles[puzzle_name] = load_puzzle_from_file(filepath)
            print(f"Loaded puzzle: {puzzle_name}")
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
    
    if not puzzles:
        print("No puzzles could be loaded!")
        return
    
    print(f"\nRunning tests on {len(puzzles)} puzzles with {len(methods)} methods...\n")
    
    # Run tests and collect results
    results = {}
    for method in methods:
        results[method] = {}
        for puzzle_name, puzzle in puzzles.items():
            print(f"Testing {method} on {puzzle_name}...")
            try:
                result = run_solver_test(puzzle, method)
                results[method][puzzle_name] = result
            except Exception as e:
                print(f"Error testing {method} on {puzzle_name}: {e}")
                results[method][puzzle_name] = {
                    'cells_filled': 0,
                    'efficiency_ratio': 0.0,
                    'solved': False,
                    'unsolvable': True,
                    'solver_iterations': 0,
                    'logical_steps': 0
                }
    
    # Get puzzle names for table headers
    puzzle_names = list(puzzles.keys())
    
    # Display main results table
    print("\n" + "="*100)
    print("SUDOKU SOLVER PERFORMANCE TABLE")
    print("="*100)
    
    # Header
    header = f"{'Method':<18}"
    for name in puzzle_names:
        header += f"{name:<16}"
    print(header)
    print("-" * len(header))
    
    # Data rows for each method - show three lines per method
    for method in methods:
        # Line 1: Method name and status symbols
        row1 = f"{method:<18}"
        # Line 2: ER/CF values  
        row2 = f"{'':<18}"
        # Line 3: Total operations values
        row3 = f"{'':<18}"
        
        for puzzle_name in puzzle_names:
            result = results[method][puzzle_name]
            if result['solved']:
                row1 += f"{'✅ solved':<16}"
                row2 += f"ER: {result['efficiency_ratio']:<11}"
                total_ops = result['solver_iterations'] + result['logical_steps']
                row3 += f"TO: {total_ops:<11}"
            else:
                row1 += f"{'❌ unsolved':<16}"
                row2 += f"CF: {result['cells_filled']:<11}"
                row3 += f"{'':<16}"
        
        print(row1)
        print(row2)
        if any(results[method][puzzle_name]['solved'] for puzzle_name in puzzle_names):
            print(row3)
        print()  # Add spacing between methods
    
    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    
    for method in methods:
        solved_count = sum(1 for result in results[method].values() if result['solved'])
        total_cells = sum(result['cells_filled'] for result in results[method].values())
        avg_efficiency = sum(result['efficiency_ratio'] for result in results[method].values()) / len(results[method])
        
        print(f"\n{method.upper()}:")
        print(f"  Puzzles solved: {solved_count}/{len(puzzles)}")
        print(f"  Total cells filled: {total_cells}")
        print(f"  Average efficiency ratio: {avg_efficiency:.3f}")

if __name__ == "__main__":
    main()
