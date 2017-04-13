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
    top_neighbors = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1]]
    center_neighbors = [[x - 1, y], [x, y], [x + 1, y]]
    bottom_neighbors = [[x - 1, y + 1], [x, y + 1], [x + 1, y + 1]]

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


class Pole(object):  # создаем Класс поля, наследуемся от Object
    def __init__(self, minefield, row, column):  # Инициализация поля. master - окно Tk().
        # self.button = Button(master, text='   ')  # Создаем для нашего поля атрибут 'button'
        self.mine = False  # Переменная наличия мины в поле
        self.value = 0  # Кол-во мин вокруг
        self.viewed = False  # Открыто/закрыто поле
        self.flag = FLAG_NOT_SET
        self.neighbors = []  # Массив, содержащий координаты соседних клеток
        self.clr = 'black'  # Цвет текста
        self.bg = None  # Цвет фона
        self.row = row  # Строка
        self.column = column  # Столбец
        self.minefield = minefield

    def find_neighbors(self):
        x = self.row
        y = self.column

        width = len(pole_array[0])
        height = len(pole_array)

        untrimed_neighbors = get_all_neighbors(x, y)
        self.neighbors = [i for i in untrimed_neighbors if not is_outside(i, width, height)]

    def open_cell(self, event=None):
        if self.viewed:
            return

        self.color_button()

        if self.mine and not self.flag:
            self.make_boom()
            return

        if not self.flag:
            self.clear_buttons()

    def clear_buttons(self):
        self.button.configure(text=self.value, fg=self.clr, bg=self.bg)  # выводим в текст поля значение
        self.viewed = True
        if self.value == None:  # Если вокруг нет мин
            for k in self.neighbors:
                pole_array[k[0]][k[1]].open_cell()  # Открываем все поля вокруг

    def make_boom(self):
        self.button.configure(text='B', bg='red')  # Показываем пользователю, что тут есть мина
        self.viewed = True  # Говорим, что клетка раскрыта
        for q in self.minefield.mines:
            pole_array[q[0]][q[1]].open_cell()  # Я сейчас буду вскрывать ВСЕ мины
        create_losing_window()  # Вызываем окно проигрыша

    def color_button(self):
        self.clr = get_color_by_value(self.value)
        if self.value == 0:
            self.value = None
            self.bg = 'lightgrey'

    def set_flag(self, event):
        if self.viewed:
            return

        self.toggle_flag()
        self.check_completition()

    def toggle_flag(self):
        if self.flag == FLAG_NOT_SET:
            self.flag = FLAG_ADDED
            self.button.configure(text='F', bg='yellow')
            self.minefield.flags.append([self.row, self.column])
            return

        if self.flag == FLAG_ADDED:
            self.flag = FLAG_UNKNOWN
            self.button.configure(text='?', bg='blue')
            self.minefield.flags.pop(self.minefield.flags.index([self.row, self.column]))
            return

        if self.flag == FLAG_UNKNOWN:
            self.flag = FLAG_NOT_SET
            self.button.configure(text='   ', bg='white')
            return

    def check_completition(self):
        if sorted(self.minefield.mines) == sorted(self.minefield.flags):
            create_win_window()


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

        self.fields = [[None,]*width for i in range(height)]

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
        cell = (x, y)
        if cell in self.mines:
            return [(x, y, -1), ]
        value = self.nearest_mines_count(x, y)
        self.fields[x][y] = value
        return [(x, y, value),]

    def nearest_mines_count(self, x, y):
        count = 0
        for mine in self.mines:
            if abs(mine[0]-x) < 2:
                if abs(mine[1]-y) < 2:
                    count +=1
        return count


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

    def right_button_clicked(self, event):
        print("Right button clicked", event)

    def cheat_clicked(self, event):
        print("Cheat is clicked")

    def run(self):
        self.window.mainloop()

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
