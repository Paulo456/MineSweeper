from tkinter import *
from random import choice

FLAG_NOT_SET = 0
FLAG_ADDED = 1
FLAG_UNKNOWN = 2


class Pole(object):  # создаем Класс поля, наследуемся от Object
    def __init__(self, master, row, column):  # Инициализация поля. master - окно Tk().
        self.button = Button(master, text='   ')  # Создаем для нашего поля атрибут 'button'
        self.mine = False  # Переменная наличия мины в поле
        self.value = 0  # Кол-во мин вокруг
        self.viewed = False  # Открыто/закрыто поле
        self.flag = FLAG_NOT_SET
        self.around = []  # Массив, содержащий координаты соседних клеток
        self.clr = 'black'  # Цвет текста
        self.bg = None  # Цвет фона
        self.row = row  # Строка
        self.column = column  # Столбец

    def setAround(self):
        if self.row == 0:
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
        elif self.row == len(buttons) - 1:
            self.around.append([self.row - 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])
        else:
            self.around.append([self.row - 1, self.column])
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])

    def open_cell(self, event):
        if self.value == 0:  # Устанавливаем цвета. Можно написать и для 6,7 и 8, но у меня закончилась фантазия
            self.clr = 'yellow'
            self.value = None
            self.bg = 'lightgrey'
        elif self.value == 1:
            self.clr = 'green'
        elif self.value == 2:
            self.clr = 'blue'
        elif self.value == 3:
            self.clr = 'red'
        elif self.value == 4:
            self.clr = 'purple'

        if self.mine and not self.viewed and not self.flag:  # Если в клетке есть мина, она еще не открыта и на ней нет флага
            self.button.configure(text='B', bg='red')  # Показываем пользователю, что тут есть мина
            self.viewed = True  # Говорим, что клетка раскрыта
            for q in mines:
                buttons[q[0]][q[1]].open_cell('<Button-1>')  # Я сейчас буду вскрывать ВСЕ мины
            create_losing_window()  # Вызываем окно проигрыша

        elif not self.viewed and not self.flag:  # Если мины нет, клетка не открыта и флаг не стоит
            self.button.configure(text=self.value, fg=self.clr, bg=self.bg)  # выводим в текст поля значение
            self.viewed = True
            if self.value == None:  # Если вокруг нет мин
                for k in self.around:
                    buttons[k[0]][k[1]].open_cell('<Button-1>')  # Открываем все поля вокруг

    def set_flag(self, event):
        if self.viewed:
            return

        if self.flag == FLAG_NOT_SET:
            self.flag = FLAG_ADDED  # Ставим флаг
            self.button.configure(text='F', bg='yellow')  # Выводим флаг
            flags.append([self.row, self.column])  # Добавляем в массив флагов
        elif self.flag == FLAG_ADDED:  # Если флаг стоим
            self.flag = FLAG_UNKNOWN  # Ставим значение '?'
            self.button.configure(text='?', bg='blue')  # Выводим его
            flags.pop(flags.index([self.row, self.column]))  # Удаляем флаг из массива флагов
        elif self.flag == FLAG_UNKNOWN:  # Если вопрос
            self.flag = FLAG_NOT_SET  # Устанавливаем на отсутствие флага
            self.button.configure(text='   ', bg='white')  # Выводим пустоту
        if sorted(mines) == sorted(flags) and mines != []:  # если массив флагов идентичен массиву мин
            create_win_window()  # Сообщаем о победе


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
            for k in j.around:
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


def create_game_window(high, lenght, bombs_count):  # получаем значения
    window = Tk()
    window.title('Сапер')
    global buttons
    global mines
    global flags
    flags = []  # Массив, содержащий в себе места, где стоят флажки
    mines = []  # Массив, содержащий в себе места, где лежат мины
    buttons = [[Pole(window, row, column) for column in range(high)] for row in
               range(lenght)]  # Двумерный массив, в котором лежат поля

    for i in buttons:  # Цикл по строкам
        for j in i:  # Цикл по элементам строки
            j.button.grid(column=i.index(j), row=buttons.index(i), ipadx=7,
                          ipady=1)  # Размещаем все в одной сетке при помощи grid
            j.button.bind('<Button-1>', j.open_cell)  # Биндим открывание клетки
            j.button.bind('<Button-3>', j.set_flag)  # Установка флажка
            j.setAround()  # Функция заполнения массива self.around

    initialize_mines(bombs_count)

    buttons[0][0].button.bind('<Control-Button-1>', cheat)  # создаем комбинацию клавиш для быстрого решения
    window.resizable(False, False)  # запрещаем изменения размера
    window.mainloop()


def initialize_mines(bombs_count):
    create_mines(0, bombs_count)
    calculate_cell_values()


def create_main_window():
    def run_game():
        high, lenght, bombs_count = read_settings()
        create_game_window(high, lenght, bombs_count)  # Начинаем игру, передавая кол-во полей

    def read_settings():
        bombs_count = 10
        high = 9
        lenght = 9

        if mineText.get('1.0', END) != '\n':  # Проверяем наличие текста
            bombs_count = int(mineText.get('1.0', END))  # Если текст есть, то это и будет кол-во бомб

        if highText.get('1.0', END) != '\n':
            high = int(highText.get('1.0', END))

        if lenghtText.get('1.0', END) != '\n':
            lenght = int(lenghtText.get('1.0', END))

        return high, lenght, bombs_count

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
