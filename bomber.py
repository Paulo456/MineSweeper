from tkinter import *
from random import randint

FLAG_NOT_SET = 0
FLAG_ADDED = 1
FLAG_UNKNOWN = 2


def get_color_by_value(value):
    if value == 0:
        return 'yellow'
    if value == 1:
        return 'green'
    if value == 2:
        return 'blue'
    if value == 3:
        return 'red'

    return 'purple'


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


class Minefield(object):
    def __init__(self, width, height, bombs_count):
        self.width = width
        self.height = height
        self.bombs_count = bombs_count
        self.mines = []
        self.flags = []

        self.initialize_mines()

    def initialize_mines(self):
        self.create_mines(0)

    def create_mines(self, bombs_paced):
        if bombs_paced == self.bombs_count:
            return

        rand_row = randint(0, self.width - 1)
        rand_column = randint(0, self.height - 1)

        rand_cell = [rand_row, rand_column]

        # Проверяем, что выбранное поле не выбиралось до этого
        if rand_cell not in self.mines:
            # b.mine = True  # Ставим мину
            self.mines.append(rand_cell)  # Добавляем ее в массив
            self.create_mines(bombs_paced + 1)  # Вызываем установщик, сказав, что одна мина уже есть
        else:
            self.create_mines(bombs_paced)  # Вызываем установщик еще раз


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


class MinefieldWindow(object):
    def __init__(self, minefield):
        self.minefield = minefield

        self.window = Tk()
        self.window.title('Сапер')
        self.window.resizable(False, False)  # запрещаем изменения размера

        self.buttons = []
        self.create_ui();

    def create_ui(self):
        for x in range(self.minefield.width):
            buttons_row = []
            for y in range(self.minefield.height):
                button = Button(self.window, text='   ')
                button.grid(column=x, row=y, ipadx=7, ipady=1)
                button.bind('<Button-1>', self.left_button_clicked)
                button.bind('<Button-3>', self.right_button_clicked)
                buttons_row.append(button)
            self.buttons.append(buttons_row)

    def left_button_clicked(self, event):
        print("left button clicked", event)

    def right_button_clicked(self, event):
        print("Right button clicked", event)

    def run(self):
        self.window.mainloop()


def create_game_window(minefield):  # получаем значения
    global pole_array
    pole_array = [[Pole(minefield, row, column) for column in range(minefield.width)] for row in
                  range(minefield.height)]  # Двумерный массив, в котором лежат поля

    # for i in pole_array:  # Цикл по строкам
    #     for j in i:  # Цикл по элементам строки
    #         j.button.grid(column=i.index(j), row=pole_array.index(i), ipadx=7,
    #                       ipady=1)  # Размещаем все в одной сетке при помощи grid
    #         j.button.bind('<Button-1>', j.open_cell)  # Биндим открывание клетки
    #         j.button.bind('<Button-3>', j.set_flag)  # Установка флажка
    #         j.find_neighbors()  # Функция заполнения массива self.around

    # pole_array[0][0].button.bind('<Control-Button-1>', cheat)  # создаем комбинацию клавиш для быстрого решения

    mineWindow = MinefieldWindow(minefield)
    mineWindow.run()


def create_main_window():
    def run_game():
        width, height, bombs_count = read_settings()
        minefield = Minefield(width, height, bombs_count)
        create_game_window(minefield)

    def read_settings():
        bombs_count = 10
        width = 9
        height = 9

        if mineText.get('1.0', END) != '\n':  # Проверяем наличие текста
            bombs_count = int(mineText.get('1.0', END))  # Если текст есть, то это и будет кол-во бомб

        if highText.get('1.0', END) != '\n':
            width = int(highText.get('1.0', END))

        if lenghtText.get('1.0', END) != '\n':
            height = int(lenghtText.get('1.0', END))

        return width, height, bombs_count

    window = Tk()
    window.title('Настройки')  # Пишем название окна
    window.geometry('200x150')  # Задаем размер
    mineText = Text(window, width=5, height=1)  # Создаем поля для ввода текста и пояснения
    mineLabe = Label(window, height=1, text='Бомбы:')
    highText = Text(window, width=5, height=1)
    highLabe = Label(window, height=1, text='Ширина:')
    lenghtText = Text(window, width=5, height=1)
    lenghtLabe = Label(window, height=1, text='Высота:')
    mineBut = Button(window, text='Начать:', command=run_game)  # Создаем кнопку
    mineBut.place(x=70, y=90)  # Размещаем это все
    mineText.place(x=75, y=5)
    mineLabe.place(x=5, y=5)
    highText.place(x=75, y=30)
    highLabe.place(x=5, y=30)
    lenghtText.place(x=75, y=55)
    lenghtLabe.place(x=5, y=55)
    window.mainloop()


if __name__ == "__main__":
    create_main_window()
