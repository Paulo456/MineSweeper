from tkinter import *
from random import choice

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


class Pole(object):  # создаем Класс поля, наследуемся от Object
    def __init__(self, master, minefield, row, column):  # Инициализация поля. master - окно Tk().
        self.button = Button(master, text='   ')  # Создаем для нашего поля атрибут 'button'
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

        width = len(buttons[0])
        height = len(buttons)

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
                buttons[k[0]][k[1]].open_cell()  # Открываем все поля вокруг

    def make_boom(self):
        self.button.configure(text='B', bg='red')  # Показываем пользователю, что тут есть мина
        self.viewed = True  # Говорим, что клетка раскрыта
        for q in mines:
            buttons[q[0]][q[1]].open_cell()  # Я сейчас буду вскрывать ВСЕ мины
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
        if sorted(mines) == sorted(self.minefield.flags):
            create_win_window()


def create_losing_window():
    window = Tk()
    window.title('Вы проиграли:-(')
    window.geometry('300x100')
    loseLabe = Label(window, text='В следующий раз повезет больше!')
    loseLabe.pack()
    mines = []
    window.mainloop()


def create_mines(bombs_count, max_bombs_count):  # Получаем массив полей вокруг и координаты нажатого поля
    if bombs_count == max_bombs_count:
        return

    a = choice(buttons)  # Выбираем рандомную строку
    b = choice(a)  # Рандомное поле
    rand_row = buttons.index(a)
    rand_column = a.index(b)
    rand_cell = [rand_row, rand_column]

    # Проверяем, что выбранное поле не выбиралось до этого
    if rand_cell not in mines:
        b.mine = True  # Ставим мину
        mines.append(rand_cell)  # Добавляем ее в массив
        create_mines(bombs_count + 1, max_bombs_count)  # Вызываем установщик, сказав, что одна мина уже есть
    else:
        create_mines(bombs_count, max_bombs_count)  # Вызываем установщик еще раз


def calculate_cell_values():
    for i in buttons:
        for j in i:
            for k in j.neighbors:
                # Если в одном из полей k мина, учеличиваем значение поля
                if buttons[k[0]][k[1]].mine:
                    buttons[buttons.index(i)][i.index(j)].value += 1


def create_win_window():
    window = Tk()
    window.geometry('300x100')
    window.title('Вы победили!')
    winLabe = Label(window, text='Поздравляем!')
    winLabe.pack()
    window.mainloop()


def cheat(event):
    for t in mines:
        buttons[t[0]][t[1]].set_flag('<Button-1>')


# high, lenght, bombs_count
def create_game_window(minefield):  # получаем значения
    window = Tk()
    window.title('Сапер')
    global buttons
    global mines
    mines = []  # Массив, содержащий в себе места, где лежат мины
    buttons = [[Pole(window, minefield, row, column) for column in range(minefield.width)] for row in
               range(minefield.height)]  # Двумерный массив, в котором лежат поля

    for i in buttons:  # Цикл по строкам
        for j in i:  # Цикл по элементам строки
            j.button.grid(column=i.index(j), row=buttons.index(i), ipadx=7,
                          ipady=1)  # Размещаем все в одной сетке при помощи grid
            j.button.bind('<Button-1>', j.open_cell)  # Биндим открывание клетки
            j.button.bind('<Button-3>', j.set_flag)  # Установка флажка
            j.find_neighbors()  # Функция заполнения массива self.around

    initialize_mines(minefield.bombs_count)

    buttons[0][0].button.bind('<Control-Button-1>', cheat)  # создаем комбинацию клавиш для быстрого решения
    window.resizable(False, False)  # запрещаем изменения размера
    window.mainloop()


def initialize_mines(bombs_count):
    create_mines(0, bombs_count)
    calculate_cell_values()


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
