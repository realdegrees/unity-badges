from typing import Callable, Optional, Tuple, Union
from PIL import Image
import textwrap
from typing import List
from util.text import get_text_dimensions

class Cell:
    def __init__(self, content: Union[str, Image.Image, None], color: Optional[str] = None):
        self.content = content
        self.color = color
        self.width = 0
        self.height = 0
        self.table: Table = None
        self.col = 0
        self.row = 0


class Table:
    def __init__(self, cells: List[List[Cell]], font, max_col_width: int = 100, gap: int = 5):
        self.rows_cnt = len(cells)
        self.cols_cnt = max(len(row) if row else 0 for row in cells)
        # Initialize the table with empty cells
        self.cells = [[Cell(None) for _ in range(self.cols_cnt)]
                      for _ in range(self.rows_cnt)]
        self.gap = gap

        # initialize width and height for each cell and set the table and row and col properties
        for row in range(self.rows_cnt):
            for col in range(self.cols_cnt):
                cellData = cells[row][col] if col < len(cells[row]) else None

                if cellData is None or not isinstance(cellData, Cell):
                    continue

                cell = self.cells[row][col]

                # Set the data from the arguments
                cell.content = cellData.content
                cell.color = cellData.color

                # Set important metadata
                cell.table = self
                cell.row = row
                cell.col = col

                if isinstance(cell.content, str):  # String content
                    width, height, content = get_text_dimensions(font, max_col_width, cell.content)
                    
                    cell.content = content
                    cell.width = width
                    cell.height = height

                elif isinstance(cell.content, Image.Image):  # Image content
                    if cell.content.width > max_col_width:
                        scale_factor = max_col_width / cell.content.width
                        new_height = int(cell.content.height * scale_factor)
                        cell.content = cell.content.resize(
                            (max_col_width, new_height))
                    cell.width = cell.content.width
                    cell.height = cell.content.height

                self.cells[row][col] = cell


    def get_cell_offset(self, cell: Union[Cell, Tuple]) -> Tuple[int, int]:
        x_offset = self.gap / 2
        y_offset = self.gap / 2
        
        for row in range(cell.row if isinstance(cell, Cell) else cell[0] if isinstance(cell, tuple) else 0):
            y_offset += self.get_row_height(row) + self.gap
        for col in range(cell.col if isinstance(cell, Cell) else cell[1] if isinstance(cell, tuple) else 0):
            x_offset += self.get_col_width(col) + self.gap
        return x_offset, y_offset

    def for_each_cell(self, callback: Callable[[Cell], None]):
        for row in range(self.rows_cnt):
            for col in range(self.cols_cnt):
                callback(self.cells[row][col])

    def for_each_row(self, callback: Callable[[int, int], None]):
        for row in range(self.rows_cnt):
            y_offset = 0
            for i in range(row):
                y_offset += self.get_row_height(i) + self.gap
                
            callback(y_offset, row)
            
    def get_row(self, row: int) -> List[Cell]:
        return self.cells[row]

    def get_col(self, col: int) -> List[Cell]:
        return [self.cells[row][col] for row in range(self.rows_cnt)]

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def get_height(self) -> int:
        return sum(self.get_row_height(i) for i in range(self.rows_cnt)) + (self.rows_cnt) * self.gap

    def get_width(self) -> int:
        return sum(self.get_col_width(i) for i in range(self.cols_cnt)) + (self.cols_cnt) * self.gap

    def get_row_height(self, row: int, withPadding=False) -> Optional[int]:
        return max(cell.height for cell in self.get_row(row)) + (self.gap / 2 if withPadding else 0)

    def get_col_width(self, col: int, withPadding=False) -> Optional[int]:
        return max(cell.width for cell in self.get_col(col)) + (self.gap / 2 if withPadding else 0)
