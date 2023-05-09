import argparse
import sys


#########################

def move_cursor(x, y):
    sys.stdout.write(f'\033[{y};{x}H')
    sys.stdout.flush()


def get_box_index(x, y):
    start_x = 0
    start_y = 0

    if x < 3:
        start_x = 0
    elif x < 6:
        start_x = 3
    else:
        start_x = 6

    if y < 3:
        start_y = 0
    elif y < 6:
        start_y = 3
    else:
        start_y = 6

    return start_x, start_y


#########################


class Cell:
    def __init__(self, x, y):
        self.possibles = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.value = 'X'
        self.x = x
        self.y = y

    def remove(self, val):
        solve = False
        update = False
        if val in self.possibles:
            self.possibles.remove(val)
            update = True

        # check to see if there is only 1 possible
        if update is True and len(self.possibles) == 1:
            # solved cell
            print(f'solved1 ({self.x},{self.y}) - {val}, {self.possibles}')
            self.value = self.possibles[0]
            solve = True
            # input()

        return solve

    def solve(self, val):
        solve = False
        if self.value == 'X' and val in self.possibles:
            print(f'solved2 ({self.x},{self.y}) - {val}, {self.possibles}')
            self.value = val
            self.possibles = [val]
            solve = True
            # input()
        return solve

    def display(self):
        return f'{self.value}'

    def debug(self):
        return f'({self.x},{self.y}) - {self.possibles}'


class Sodoku:
    def __init__(self):
        self.cells = []
        self.init()

    def init(self):
        for x in range(0, 9):
            row = []
            for y in range(0, 9):
                row.append(Cell(x, y))
            self.cells.append(row)

    def populate(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        for x in range(len(lines)):
            line_split = lines[x].strip().split(',')
            for y in range(len(line_split)):
                if line_split[y] != '0':
                    self.cells[x][y].value = line_split[y]
                    self.cells[x][y].possibles = [line_split[y]]

    def display(self):
        for x in range(0, 9):
            for y in range(0, 9):
                sys.stdout.write(self.cells[x][y].display() + ' ')
            print()
        print()

    def debug(self):
        for x in range(0, 9):
            for y in range(0, 9):
                # print(self.cells[x][y].debug())
                if self.cells[x][y].value == 'X':
                    sys.stdout.write(self.cells[x][y].debug() + ' ')
            print()
        print()

    def get_row(self, x, y):
        row = []
        for i in range(0, 9):
            if i != y:
                row.append(self.cells[x][i])
        return row

    def get_column(self, x, y):
        column = []
        for i in range(0, 9):
            if i != x:
                column.append(self.cells[i][y])
        return column

    def get_box(self, x, y):
        start_x, start_y = get_box_index(x, y)
        box = []
        for i in range(start_x, start_x+3):
            for j in range(start_y, start_y+3):
                if i != x or j != y:
                    box.append(self.cells[i][j])
        return box

    #########################
    # Solvers
    #########################

    def _last_possible(self, cell, cells):
        for cell2 in cells:
            if cell2.value != 'X':  # if cell solved
                ret = cell.remove(cell2.value)
                if ret is True:
                    return True
        return False

    def last_possible(self):
        for rows in self.cells:
            for cell in rows:
                if cell.value == 'X':  # if cell not solved
                    # print('Cell', cell.x, cell.y)
                    # print('Before', cell.possibles)
                    cell_row = self.get_row(cell.x, cell.y)
                    ret = self._last_possible(cell, cell_row)
                    if ret is True:
                        return True

                    cell_column = self.get_column(cell.x, cell.y)
                    ret = self._last_possible(cell, cell_column)
                    if ret is True:
                        return True

                    cell_box = self.get_box(cell.x, cell.y)
                    ret = self._last_possible(cell, cell_box)
                    if ret is True:
                        return True
                    # print('After', cell.possibles)
                    # input()
        return False

    def _last_remaining(self, cell, cells):
        possibles = []
        for cell2 in cells:
            if cell2.value == 'X':
                possibles += cell2.possibles

        for val in cell.possibles:
            if val not in possibles:
                ret = cell.solve(val)
                if ret is True:
                    return True
        return False

    def last_remaining(self):
        for rows in self.cells:
            for cell in rows:
                if cell.value == 'X':
                    # print('Cell', cell.x, cell.y)
                    # print('Before', cell.possibles)
                    cell_row = self.get_row(cell.x, cell.y)
                    ret = self._last_remaining(cell, cell_row)
                    if ret is True:
                        return True

                    cell_column = self.get_column(cell.x, cell.y)
                    ret = self._last_remaining(cell, cell_column)
                    if ret is True:
                        return True

                    cell_box = self.get_box(cell.x, cell.y)
                    ret = self._last_remaining(cell, cell_box)
                    if ret is True:
                        return True
                    # print('After', cell.possibles)
                    # input()
        return False

    def _naked_doubles(self, cell, cells):
        solve = False
        c2 = None
        possibles = []
        for cell2 in cells:
            if cell.possibles == cell2.possibles:
                c2 = cell2
                possibles = cell.possibles

        if c2 is not None and len(possibles) > 0:
            print(f'one!!!! ({cell.x},{cell.y}) - {cell.possibles}')
            print(f'two!!!! ({c2.x},{c2.y}) - {c2.possibles}')
            for cell2 in cells:
                if cell2 != c2:
                    for pos in possibles:
                        if cell2.value == 'X' and pos in cell2.possibles:
                            ret = cell2.remove(pos)
                            print(f'here!!!! {pos} - ({cell2.x},{cell2.y}) - {cell2.possibles}')
                            input()
                            if ret is True:
                                solve = True
        return solve

    def naked_doubles(self):
        for rows in self.cells:
            for cell in rows:
                if cell.value == 'X' and len(cell.possibles) == 2:  # if cell not solved and only 2 possibles
                    # print('Cell', cell.x, cell.y)
                    # print('Before', cell.possibles)
                    cell_row = self.get_row(cell.x, cell.y)
                    ret = self._naked_doubles(cell, cell_row)
                    if ret is True:
                        return True

                    cell_column = self.get_column(cell.x, cell.y)
                    ret = self._naked_doubles(cell, cell_column)
                    if ret is True:
                        return True

                    cell_box = self.get_box(cell.x, cell.y)
                    ret = self._naked_doubles(cell, cell_box)
                    if ret is True:
                        return True
                    # print('After', cell.possibles)
                    # input()
        return False


def main():
    parser = argparse.ArgumentParser(description='What the program does')
    parser.add_argument('filename', default='easy1.txt')
    args = parser.parse_args()

    game = Sodoku()
    game.populate(args.filename)
    game.display()
    ret = True
    while ret is True:
        ret = game.last_possible()
        if ret is True:
            game.display()
            continue

        ret = game.last_remaining()
        if ret is True:
            game.display()
            continue

        ret = game.naked_doubles()
        if ret is True:
            game.display()
            continue
        # game.debug()
        # input()
    # game.debug()


if __name__ == '__main__':
    main()
