'''
Puzzle class for managing puzzle state and operations

Author: Ian Jackson
Date: 08-27-2025
'''

#== Imports ==#


#== Global Variables ==#


#== Classes ==#
class Cell:
    def __init__(self, value: int = 0):
        '''
        Initialize a Cell with a given value.

        Args:
            value (int, optional): The value of the cell. Defaults to 0.
        '''
        self.value = value
        self.possible_values = set(range(1, 10)) if value == 0 else {value}

        # x and y positions
        self.x_pos_rel: int | None = None
        self.y_pos_rel: int | None = None
        self.x_pos_abs: int | None = None
        self.y_pos_abs: int | None = None

class Box:
    def __init__(self, id: int, cells: list[Cell]):
        '''
        Initialize a Box with a given ID and list of Cells.

        Args:
            id (int): The ID of the box.
            cells (list[Cell]): The list of cells in the box.
        '''
        self.id = id
        self.cells = cells
        self.is_sat = False


class Row: 
    def __init__(self, id: int, cells: list[Cell]):
        '''
        Initialize a Row with a given ID and list of Cells.

        Args:
            id (int): The ID of the row.
            cells (list[Cell]): The list of cells in the row.
        '''
        self.id = id
        self.cells = cells
        self.is_sat = False

class Column:
    def __init__(self, id: int, cells: list[Cell]):
        '''
        Initialize a Column with a given ID and list of Cells.

        Args:
            id (int): The ID of the column.
            cells (list[Cell]): The list of cells in the column.
        '''
        self.id = id
        self.cells = cells
        self.is_sat = False

class Puzzle:
    def __init__(self, grid: list[list[int]]):
        '''
        Initialize a Puzzle with a given grid.

        Args:
            grid (list[list[int]]): The 2D list representing the puzzle grid.
        '''
        self.grid = grid
        self.cells = [Cell(value=grid[y][x]) for y in range(9) for x in range(9)]
        self.boxes = [Box(id=i, cells=[]) for i in range(9)]
        self.rows = [Row(id=i, cells=[]) for i in range(9)]
        self.columns = [Column(id=i, cells=[]) for i in range(9)]

        # Assign cells to boxes, rows, and columns
        for row in range(9):
            for col in range(9):
                cell = self.cells[row * 9 + col]
                box_id = (row // 3) * 3 + (col // 3)
                self.boxes[box_id].cells.append(cell)
                self.rows[row].cells.append(cell)
                self.columns[col].cells.append(cell)

                # Set cell positions (stored as row, column for consistency with display)
                cell.x_pos_rel = col % 3  # relative column within box
                cell.y_pos_rel = row % 3  # relative row within box
                cell.x_pos_abs = row      # absolute row (for get_cell x parameter)
                cell.y_pos_abs = col      # absolute column (for get_cell y parameter)

    def get_cell(self, x: int, y: int) -> Cell:
        '''
        Get the Cell at the given (x, y) position.

        Args:
            x (int): The x-coordinate (row, 0-8).
            y (int): The y-coordinate (column, 0-8).

        Returns:
            Cell: The Cell at the specified position.
        '''
        return self.cells[x * 9 + y]
    
    def get_box_id(self, x: int, y: int) -> int:
        '''
        Get the box ID for the cell at the given (x, y) position.

        Args:
            x (int): The x-coordinate (row, 0-8).
            y (int): The y-coordinate (column, 0-8).

        Returns:
            int: The box ID (1-9).
        '''
        return (x // 3) * 3 + (y // 3) + 1
    
    def get_row_id(self, x: int, y: int) -> int:
        '''
        Get the row ID for the cell at the given (x, y) position.

        Args:
            x (int): The x-coordinate (row, 0-8).
            y (int): The y-coordinate (column, 0-8).

        Returns:
            int: The row ID (1-9).
        '''
        return x + 1
    
    def get_column_id(self, x: int, y: int) -> int:
        '''
        Get the column ID for the cell at the given (x, y) position.

        Args:
            x (int): The x-coordinate (row, 0-8).
            y (int): The y-coordinate (column, 0-8).

        Returns:
            int: The column ID (1-9).
        '''
        return y + 1

    def display(self):
        '''
        Display the current state of the puzzle grid.
        '''
        for y in range(9):
            if y % 3 == 0 and y != 0:
                print("- - - + - - - + - - -")
            row = ""
            for x in range(9):
                if x % 3 == 0 and x != 0:
                    row += "| "
                cell_value = self.cells[y * 9 + x].value
                row += f"{cell_value if cell_value != 0 else '.'} "
            print(row)
        print()