'''
Sudoku Solver

This script solves a given Sudoku puzzle

Author: Ian Jackson
Date 08-27-2025
Version 0.2
'''

#== Imports ==#
import puzzle
import solver
import time
import os
import argparse

#== Global Variables ==#


#== Functions ==#
def setup_argument_parser():
    """
    Set up command line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Sudoku Solver - Solve Sudoku puzzles from text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py -i easy_000.txt
  python main.py --input hard_000.txt
  python main.py -i puzzles/easy_000.txt
  python main.py  # Uses default easy puzzle

Puzzle file format:
  - 9 lines of 9 digits each
  - 0 represents empty cells
  - Blank lines are ignored
        '''
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Input puzzle file (e.g., easy_000.txt). If only filename is provided, looks in puzzles/ directory.'
    )
    
    parser.add_argument(
        '-m', '--method',
        type=str,
        choices=['elimination', 'random', 'elimination_plus', 'elimination_pro'],
        default='elimination',
        help='Solving method to use (default: elimination)'
    )
    
    return parser

def load_puzzle_from_file(filepath):
    """
    Load a Sudoku puzzle from a text file.
    
    Expected format:
    - 9 lines of 9 digits each (0 for empty cells)
    - Blank lines are ignored
    - Each line represents a row in the Sudoku grid
    
    Args:
        filepath (str): Path to the puzzle file
        
    Returns:
        List[List[int]]: 9x9 grid representing the puzzle
    """
    grid = []
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                
                # Convert line to list of integers
                if len(line) == 9 and line.isdigit():
                    row = [int(digit) for digit in line]
                    grid.append(row)
                else:
                    raise ValueError(f"Invalid line format: '{line}'. Expected 9 digits.")
        
        # Validate grid size
        if len(grid) != 9:
            raise ValueError(f"Invalid grid size: {len(grid)} rows. Expected 9 rows.")
            
        return grid
        
    except FileNotFoundError:
        print(f"❌ Error: Puzzle file '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"❌ Error loading puzzle: {e}")
        return None


#== Main Code ==#
def main():
    # Set up command line argument parsing
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Determine puzzle file to load
    if args.input:
        # Check if the input is just a filename or a full path
        if os.path.dirname(args.input):
            # Full path provided
            puzzle_file = args.input
        else:
            # Just filename provided, look in puzzles directory
            puzzle_file = os.path.join('puzzles', args.input)
        
        # Extract puzzle name from filename for display
        puzzle_name = os.path.splitext(os.path.basename(args.input))[0]
    else:
        # Default puzzle if no input specified
        puzzle_file = 'puzzles/easy_000.txt'
        puzzle_name = 'easy_000 (default)'
    
    print(f"🎯 Loading puzzle from file: {puzzle_file}")
    grid = load_puzzle_from_file(puzzle_file)
    
    if grid is None:
        print("❌ Failed to load puzzle. Exiting.")
        return
    
    print(f"✅ Successfully loaded puzzle: {puzzle_name}")
    puz = puzzle.Puzzle(grid)
    
    # Display the initial puzzle
    print(f"\n📋 INITIAL SUDOKU PUZZLE ({puzzle_name.upper()}):")
    print("=" * 40)
    puz.display()
    
    # Count empty cells
    empty_cells = sum(1 for row in grid for cell in row if cell == 0)
    print(f"\n📊 PUZZLE STATISTICS:")
    print(f"   • Empty cells: {empty_cells}/81")
    print(f"   • Filled cells: {81 - empty_cells}/81")
    print(f"   • Completion: {((81 - empty_cells) / 81) * 100:.1f}%")

    print("\n🔄 SOLVING PUZZLE...")
    print("=" * 40)

    # solve the puzzle with timing
    start_time = time.time()
    sol = solver.Solver(puz, method=args.method)
    sol.solve()
    end_time = time.time()
    solve_time = end_time - start_time
    
    # Display the solved puzzle
    print("\n✅ SOLVED SUDOKU PUZZLE:")
    print("=" * 40)
    puz.display()
    
    # Display solution statistics
    stats = sol.get_detailed_stats()
    print(f"\n📈 SOLUTION STATISTICS:")
    print(f"   • Solving method: {sol.method}")
    print(f"   • Time to solve: {solve_time:.4f} seconds")
    print(f"   • Cells filled: {stats['cells_filled']} (legacy steps: {sol.steps})")
    print(f"   • Logical reasoning steps: {stats['logical_steps']}")
    print(f"   • Elimination operations: {stats['elimination_operations']}")
    print(f"   • Solver iterations: {stats['solver_iterations']}")
    print(f"   • Total operations: {stats['total_reasoning_operations']}")
    print(f"   • Efficiency ratio: {stats['efficiency_ratio']:.2f} cells/iteration")
    print(f"   • Average eliminations per cell: {stats['eliminations_per_cell']:.1f}")
    
    # Handle puzzle completion status
    if sol.solved:
        print(f"   • Puzzle solved: ✅ Yes")
    elif stats['unsolvable']:
        print(f"   • Puzzle solved: ❌ No - Unsolvable with current method")
        print(f"   • Iterations without progress: {stats['iterations_without_progress']}")
        print(f"   • Reason: No progress for 5+ consecutive iterations")
    else:
        print(f"   • Puzzle solved: ⚠️ Incomplete")
    
    # Performance rating based on efficiency (only if solved)
    if sol.solved:
        if stats['solver_iterations'] <= 5:
            print(f"   • Solving efficiency: 🎯 Excellent!")
        elif stats['solver_iterations'] <= 10:
            print(f"   • Solving efficiency: ✨ Good!")
        elif stats['solver_iterations'] <= 20:
            print(f"   • Solving efficiency: 👍 Fair")
        else:
            print(f"   • Solving efficiency: 🔄 Many iterations needed")
    
    if solve_time < 0.001:
        print(f"   • Speed performance: ⚡ Lightning fast!")
    elif solve_time < 0.01:
        print(f"   • Speed performance: 🚀 Very fast!")
    elif solve_time < 0.1:
        print(f"   • Speed performance: ✨ Fast!")
    else:
        print(f"   • Speed performance: 🐌 Could be faster")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()