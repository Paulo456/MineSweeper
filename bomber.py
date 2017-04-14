from tkinter import *
from random import randint

FLAG_NOT_SET = 0
FLAG_ADDED = 1
FLAG_UNKNOWN = 2

CELL_WITH_MINE = -1


def get_color_by_value(value):
    if value == CELL_WITH_MINE:
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
    def __init__(self, width, height, mines_count):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.mines = []
        self.flags = []

        self.fields = [[None, ] * width for i in range(height)]

        self.initialize_mines()

    def initialize_mines(self):
        self.create_mines(0)

    def create_mines(self, mines_paced):
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
            value = CELL_WITH_MINE
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

    def show_all_cells(self):
        result = []
        for x, row in enumerate(self.fields):
            for y, value in enumerate(row):
                if value == None:
                    if (x, y) in self.mines:
                        value = CELL_WITH_MINE
                    else:
                        value = self.nearest_mines_count(x, y)
                result.append((x, y, value), )
        return result


class MinefieldWindow(object):
    BUTTON_SIZE = 32

    def __init__(self, width, height, mines):
        self.minefield = Minefield(width, height, mines)

        self.window = Tk()
        self.window.geometry('%dx%d' % (width * self.BUTTON_SIZE, height * self.BUTTON_SIZE))
        self.window.title('Сапер')
        self.window.resizable(False, False)  # запрещаем изменения размера

        self.buttons = []
        self.create_ui()

    def create_ui(self):
        for x in range(self.minefield.width):
            buttons_row = []
            for y in range(self.minefield.height):
                button = Button(self.window)
                button.place(x=x * self.BUTTON_SIZE,
                             y=y * self.BUTTON_SIZE,
                             width=self.BUTTON_SIZE,
                             height=self.BUTTON_SIZE)
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

        mines = [i for i in opened_cells if i[2] == CELL_WITH_MINE]
        if mines:
            self.show_fail_message()

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
            self.show_success_message()

    def cheat_clicked(self, event):
        all_cells = self.minefield.show_all_cells()
        self.show_opened_cells(all_cells)
        self.show_success_message()

    def show_fail_message(self):
        frame_width = 200
        frame_height = 90
        frame = Frame(self.window, width=frame_width, height=frame_height, bg='indian red')
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        frame.place(x=(width - frame_width) // 2, y=(height - frame_height) // 2.3)
        caption = Label(frame, text='Вы проиграли', font=("Arial", 18), bg='indian red')
        caption.place(x=20, y=5)
        message = Label(frame, text="В следующий раз вам повезёт больше!",
                        font=("Arial", 12), justify="left",
                        wraplength=frame_width, bg='indian red')
        message.place(x=10, y=40)

    def show_success_message(self):
        frame_width = 200
        frame_height = 80
        frame = Frame(self.window, width=frame_width, height=frame_height, bg="forest green")
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        frame.place(x=(width - frame_width) // 2, y=(height - frame_height) // 2.3)
        caption = Label(frame, text='Поздравляем', font=("Arial", 18), bg="forest green")
        caption.place(x=20, y=5)
        message = Label(frame, text="Вы выйграли!", font=("Arial", 14), bg="forest green")
        message.place(x=35, y=40)

    def run(self):
        self.window.mainloop()

    def show_opened_cells(self, opened_cells):

        for cell in opened_cells:
            x, y, value = cell
            button = self.buttons[x][y]

            if value == CELL_WITH_MINE:
                value = "M"
                button.configure(font=("Wingdings", 20))
            if value == 0:
                value = "  "

            color, background = get_color_by_value(value)
            button.configure(text=value, fg=color, bg=background)  # выводим в текст поля значение


if __name__ == "__main__":
    window = MainWindow()
    window.run()
