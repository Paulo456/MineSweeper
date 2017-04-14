from tkinter import *
from random import randint

FLAG_NOT_SET = 0
FLAG_ADDED = 1
FLAG_UNKNOWN = 2


def get_color_by_value(value):
    if value == -1:
        return ('red', 'red')
    if value == 0:
        return ('yellow', 'lightgrey')
    if value == 1:
        return ('green', 'lightgrey')
    if value == 2:
        return ('blue', 'lightgrey')
    if value == 3:
        return ('red', 'lightgrey')

    return ('purple', 'lightgrey')


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


def create_losing_window():
    window = Tk()
    window.title('Вы проиграли:-(')
    window.geometry('300x100')
    loseLabe = Label(window, text='В следующий раз повезет больше!')
    loseLabe.pack()
    window.mainloop()


def create_win_window():
    window = Tk()
    window.geometry('300x100')
    window.title('Вы победили!')
    winLabe = Label(window, text='Поздравляем!')
    winLabe.pack()
    window.mainloop()


def cheat(event):
    for t in mines:
        pole_array[t[0]][t[1]].set_flag('<Button-1>')


class MainWindow(object):
    def __init__(self):
        self.width = 9
        self.height = 9
        self.mines = 10

        self.window = Tk()
        self.window.title('Настройки')  # Пишем название окна
        self.window.geometry('200x150')  # Задаем размер

        self.mineText = None
        self.highText = None
        self.lenghtText = None

        self.create_ui()

    def create_ui(self):
        self.mineText = Text(self.window, width=5, height=1)  # Создаем поля для ввода текста и пояснения
        self.mineText.place(x=75, y=5)

        mineLabe = Label(self.window, height=1, text='Бомбы:')
        mineLabe.place(x=5, y=5)

        self.highText = Text(self.window, width=5, height=1)
        self.highText.place(x=75, y=30)

        highLabe = Label(self.window, height=1, text='Ширина:')
        highLabe.place(x=5, y=30)

        self.lenghtText = Text(self.window, width=5, height=1)
        self.lenghtText.place(x=75, y=55)

        lenghtLabe = Label(self.window, height=1, text='Высота:')
        lenghtLabe.place(x=5, y=55)

        self.mineBut = Button(self.window, text='Начать:', command=self.start_game)  # Создаем кнопку
        self.mineBut.place(x=70, y=90)  # Размещаем это все

    def run(self):
        self.window.mainloop()

    def validate_input(self):
        if self.mineText.get('1.0', END) != '\n':  # Проверяем наличие текста
            self.mines = int(self.mineText.get('1.0', END))  # Если текст есть, то это и будет кол-во бомб

        if self.highText.get('1.0', END) != '\n':
            self.width = int(self.highText.get('1.0', END))

        if self.lenghtText.get('1.0', END) != '\n':
            self.height = int(self.lenghtText.get('1.0', END))

    def start_game(self):
        self.validate_input()
        mineWindow = MinefieldWindow(self.width, self.height, self.mines)
        mineWindow.run()


class Minefield(object):
    def __init__(self, width, height, bombs_count):
        self.width = width
        self.height = height
        self.bombs_count = bombs_count
        self.mines = []
        self.flags = []

        self.fields = [[None, ] * width for i in range(height)]

        self.initialize_mines()

    def initialize_mines(self):
        self.create_mines(0)

    def create_mines(self, bombs_paced):
        if bombs_paced == self.bombs_count:
            return

        rand_row = randint(0, self.width - 1)
        rand_column = randint(0, self.height - 1)

        rand_cell = (rand_row, rand_column)

        # Проверяем, что выбранное поле не выбиралось до этого
        if rand_cell not in self.mines:
            # b.mine = True  # Ставим мину
            self.mines.append(rand_cell)  # Добавляем ее в массив
            self.create_mines(bombs_paced + 1)  # Вызываем установщик, сказав, что одна мина уже есть
        else:
            self.create_mines(bombs_paced)  # Вызываем установщик еще раз

    def open_cells(self, x, y):
        return self.check_nearest_cells(x, y)

    def nearest_mines_count(self, x, y):
        count = 0
        for mine in self.mines:
            if abs(mine[0] - x) < 2:
                if abs(mine[1] - y) < 2:
                    count += 1
        return count

    def check_nearest_cells(self, x, y):
        if self.fields[x][y] != None:
            return []

        if (x, y) in self.mines:
            value = -1
        else:
            value = self.nearest_mines_count(x, y)

        self.fields[x][y] = value
        result = [(x, y, value), ]
        if value != 0:
            return result

        untrimed_neighbors = get_all_neighbors(x, y)
        neighbors = [i for i in untrimed_neighbors if not is_outside(i, self.width, self.height)]
        unvisited_neighbors = [i for i in neighbors if self.fields[i[0]][i[1]] == None]
        for i in unvisited_neighbors:
            result.extend(self.check_nearest_cells(i[0], i[1]))
        return result

    def loggle_flag(self, x, y):
        if self.fields[x][y] != None:
            return

        flag = next((flag for flag in self.flags if flag[0] == x and flag[1] == y), None)
        if not flag:
            flag = [x, y, FLAG_NOT_SET]
            self.flags.append(flag)

        if flag[2] == FLAG_NOT_SET:
            flag[2] = FLAG_ADDED
            return flag

        if flag[2] == FLAG_ADDED:
            flag[2] = FLAG_UNKNOWN
            return flag

        flag[2] = FLAG_NOT_SET
        self.flags.remove(flag)

        return flag


class MinefieldWindow(object):
    def __init__(self, width, height, mines):
        self.minefield = Minefield(width, height, mines)

        self.window = Tk()
        self.window.title('Сапер')
        self.window.resizable(False, False)  # запрещаем изменения размера

        self.buttons = []
        self.create_ui()

    def create_ui(self):
        for x in range(self.minefield.width):
            buttons_row = []
            for y in range(self.minefield.height):
                button = Button(self.window, text='   ')
                button.grid(column=x, row=y, ipadx=7, ipady=1)
                button.bind('<Button-1>', self.left_button_clicked)
                button.bind('<Button-3>', self.right_button_clicked)
                button.name = "%dx%d" % (x, y)
                buttons_row.append(button)
            self.buttons.append(buttons_row)

        self.buttons[0][0].bind('<Control-Button-1>',
                                self.cheat_clicked)  # создаем комбинацию клавиш для быстрого решения

    def left_button_clicked(self, event):
        x_str, y_str = event.widget.name.split("x")
        x = int(x_str)
        y = int(y_str)

        opened_cells = self.minefield.open_cells(x, y)
        self.show_opened_cells(opened_cells)

        bombs = [i for i in opened_cells if i[2] == -1]
        if bombs:
            self.exit()
            create_losing_window()

    def right_button_clicked(self, event):
        x_str, y_str = event.widget.name.split("x")
        x = int(x_str)
        y = int(y_str)
        flag = self.minefield.loggle_flag(x, y)
        if not flag:
            return

        button = self.buttons[flag[0]][flag[1]]

        value = flag[2]

        if value == FLAG_ADDED:
            button.configure(text='F', bg='yellow')

        if value == FLAG_UNKNOWN:
            button.configure(text='?', bg='blue')

        if value == FLAG_NOT_SET:
            button.configure(text='   ', bg='white')

        flags_coords = [(i[0], i[1]) for i in self.minefield.flags]

        if sorted(self.minefield.mines) == sorted(flags_coords):
            self.exit()
            create_win_window()

    def cheat_clicked(self, event):
        print("Cheat is clicked")

    def run(self):
        self.window.mainloop()

    def exit(self):
        self.window.destroy()

    def show_opened_cells(self, opened_cells):
        for cell in opened_cells:
            x, y, value = cell
            if value == -1:
                value = "Ṓ"
            if value == 0:
                value = "  "
            button = self.buttons[x][y]
            color, background = get_color_by_value(value)
            button.configure(text=value, fg=color, bg=background)  # выводим в текст поля значение


if __name__ == "__main__":
    window = MainWindow()
    window.run()
