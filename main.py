from typing import List, Literal, Self


class Cell:
    def __init__(self,
                 content: Literal['?', 'F', ' '] | int,
                 row: int,
                 col: int,
                 parent: 'MineSweeper'
                 ) -> None:
        self.content: Literal['?', 'F', ' '] | int = content
        self.row: int = row
        self.col: int = col
        self.parent: MineSweeper = parent
        self.neighbours: List[Cell] = []

    def __str__(self):
        return f'{self.content}'

    def __repr__(self):
        return f'Cell(content={self.content}, row={self.row}, col={self.col}, parent=MineSweeper())'

    def init_neighbours(self) -> None:
        neighbours: List[Cell] = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 and y != 0:
                    neighbours.append(self.parent.get_cell(self.row + x, self.col + y))
        neighbours = [cell for cell in neighbours if cell]
        self.neighbours = neighbours

class MineSweeper:
    def __init__(self) -> None:
        self.board: List[List[Cell]] = [[Cell(0, 10 - row, col + 1, self) for col in range(10)] for row in range(10)]
        for i in range(10):
            for j in range(10):
                self.board[i][j].init_neighbours()
        self.main_cycle()

    def get_cell(self, row: int, col: int) -> Cell | None:
        if row in range(10) and col in range(10):
            return self.board[row][col]
        return None

    def move(self, row: int, col: int, move_type: Literal['Open', 'Flag']) -> None:
        row = row - 1
        col = 10 - col
        cell = self.get_cell(row, col)
        match move_type:
            case 'Open':
                cell.open()
            case 'Flag':
                cell.set_flag()

    def main_cycle(self) -> None:
        while True:
            print(self)
            try:
                row, coll, move_type = eval(input())
                self.move(row, coll, move_type)
            except Exception:
                pass


    def __str__(self) -> str:
        table_str: str = ''
        for row in self.board:
            table_str += '  '.join(map(str, row)) + '\n'
        table_str = table_str.strip()
        return table_str

    def __repr__(self) -> str:
        return "MineSweeper()"

MineSweeper()