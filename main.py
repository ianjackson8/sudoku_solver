'''
Sudoku Solver

This script solves a given Sudoku puzzle

Author: Ian Jackson
Date 08-27-2025
Version 0.1
'''

#== Imports ==#
import puzzle
import solver
import time

#== Global Variables ==#


#== Functions ==#


#== Main Code ==#
def main():
    grid_easy = [[0,1,0, 0,8,6, 0,3,2],
                [0,2,0, 0,0,9, 6,5,0],
                [6,0,3, 0,0,0, 9,1,0],

                [0,0,1, 5,4,3, 2,0,6],
                [0,4,0, 0,2,0, 0,8,1],
                [2,5,0, 1,0,0, 0,0,0],

                [7,0,0, 0,0,5, 0,0,0],
                [1,0,0, 0,7,0, 8,6,5],
                [0,9,8, 0,0,1, 3,0,4]]
    
    grid_nsol = [[1,1,0, 0,8,6, 0,3,2],
                [0,2,0, 0,0,9, 6,5,0],
                [6,0,3, 0,0,0, 9,1,0],

                [0,0,1, 5,4,3, 2,0,6],
                [0,4,0, 0,2,0, 0,8,1],
                [2,5,0, 1,0,0, 0,0,0],

                [7,0,0, 0,0,5, 0,0,0],
                [1,0,0, 0,7,0, 8,6,5],
                [0,9,8, 0,0,1, 3,0,4]]
    
    grid_hard = [[0,0,0, 0,0,0, 0,1,0],
                [4,0,0, 0,0,0, 0,0,0],
                [0,2,0, 0,0,0, 0,0,0],

                [0,0,0, 0,5,0, 4,0,7],
                [0,0,8, 0,0,0, 3,0,0],
                [0,0,1, 0,9,0, 0,0,0],

                [3,0,0, 4,0,0, 2,0,0],
                [0,5,0, 1,0,0, 0,0,0],
                [0,0,0, 8,0,6, 0,0,0]]
    
    grid = grid_easy
    puz = puzzle.Puzzle(grid)
    
    # Display the initial puzzle
    print("📋 INITIAL SUDOKU PUZZLE:")
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
    sol = solver.Solver(puz)
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