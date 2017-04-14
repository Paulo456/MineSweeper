from random import randint
import constants as const


def get_all_neighbors(x, y):
    top_neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
    center_neighbors = [(x - 1, y), (x, y), (x + 1, y)]
    bottom_neighbors = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

    result = []
    result.extend(top_neighbors)
    result.extend(center_neighbors)
    result.extend(bottom_neighbors)
    return result


def is_outside(pos, width, height):
    if pos[0] < 0:
        return True

    if pos[0] >= width:
        return True

    if pos[1] < 0:
        return True

    if pos[1] >= height:
        return True

    return False


class Minefield(object):
    def __init__(self, width, height, mines_count):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.mines = []
        self.flags = []
        self.fields = [[None, ] * height for i in range(width)]
        self.gamestate = const.GAME_STATE_PLAY

        self.create_mines()

    def create_mines(self, mines_paced=0):
        if mines_paced == self.mines_count:
            return

        rand_row = randint(0, self.width - 1)
        rand_column = randint(0, self.height - 1)

        rand_cell = (rand_row, rand_column)

        if rand_cell not in self.mines:
            self.mines.append(rand_cell)
            self.create_mines(mines_paced + 1)
        else:
            self.create_mines(mines_paced)

    def open_cells(self, x, y):
        if self.fields[x][y] is not None:
            return []

        if (x, y) in self.mines:
            value = const.CELL_WITH_MINE
        else:
            value = self.nearest_mines_count(x, y)

        self.fields[x][y] = value
        result = [(x, y, value), ]
        if value != 0:
            return result

        untrimed_neighbors = get_all_neighbors(x, y)
        neighbors = [i for i in untrimed_neighbors if not is_outside(i, self.width, self.height)]
        unvisited_neighbors = [i for i in neighbors if self.fields[i[0]][i[1]] is None]
        for i in unvisited_neighbors:
            result.extend(self.open_cells(i[0], i[1]))
        return result

    def nearest_mines_count(self, x, y):
        count = 0
        for mine in self.mines:
            if abs(mine[0] - x) < 2:
                if abs(mine[1] - y) < 2:
                    count += 1
        return count

    def loggle_flag(self, x, y):
        if self.fields[x][y] is not None:
            return

        flag = next((flag for flag in self.flags if flag[0] == x and flag[1] == y), None)
        if not flag:
            flag = [x, y, const.FLAG_NOT_SET]
            self.flags.append(flag)

        if flag[2] == const.FLAG_NOT_SET:
            flag[2] = const.FLAG_ADDED
            return flag

        if flag[2] == const.FLAG_ADDED:
            flag[2] = const.FLAG_UNKNOWN
            return flag

        flag[2] = const.FLAG_NOT_SET
        self.flags.remove(flag)

        return flag

    def show_all_cells(self):
        result = []
        for x, row in enumerate(self.fields):
            for y, value in enumerate(row):
                if value is None:
                    if (x, y) in self.mines:
                        value = const.CELL_WITH_MINE
                    else:
                        value = self.nearest_mines_count(x, y)
                result.append((x, y, value), )
        return result

    def is_game_ended(self, opened_cells=None):
        if opened_cells:
            mines = [i for i in opened_cells if i[2] == const.CELL_WITH_MINE]
            if mines:
                self.gamestate = const.GAME_STATE_LOST
                return self.gamestate

        flags_coords = [(i[0], i[1]) for i in self.flags]

        if sorted(self.mines) == sorted(flags_coords):
            self.gamestate = const.GAME_STATE_WIN
            return self.gamestate

        return self.gamestate
