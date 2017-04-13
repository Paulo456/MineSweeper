from tkinter import *
from random import choice


class Pole(object):  # создаем Класс поля, наследуемся от Object
    def __init__(self, master, row, column):  # Инициализация поля. master - окно Tk().
        self.button = Button(master, text='   ')  # Создаем для нашего поля атрибут 'button'
        self.mine = False  # Переменная наличия мины в поле
        self.value = 0  # Кол-во мин вокруг
        self.viewed = False  # Открыто/закрыто поле
        self.flag = 0  # 0 - флага нет, 1 - флаг стоит, 2 - стоит "?"
        self.around = []  # Массив, содержащий координаты соседних клеток
        self.clr = 'black'  # Цвет текста
        self.bg = None  # Цвет фона
        self.row = row  # Строка
        self.column = column  # Столбец

    def viewAround(self):
        return self.around

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

    def view(self, event):
        if mines == []:  # При первом нажатии
            seter(0, self.around, self.row, self.column)  # Устанавливаем мины
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
                buttons[q[0]][q[1]].view('<Button-1>')  # Я сейчас буду вскрывать ВСЕ мины
            create_losing_window()  # Вызываем окно проигрыша

        elif not self.viewed and not self.flag:  # Если мины нет, клетка не открыта и флаг не стоит
            self.button.configure(text=self.value, fg=self.clr, bg=self.bg)  # выводим в текст поля значение
            self.viewed = True
            if self.value == None:  # Если вокруг нет мин
                for k in self.around:
                    buttons[k[0]][k[1]].view('<Button-1>')  # Открываем все поля вокруг

    def setFlag(self, event):
        if self.flag == 0 and not self.viewed:  # Если поле не открыто и флага нет
            self.flag = 1  # Ставим флаг
            self.button.configure(text='F', bg='yellow')  # Выводим флаг
            flags.append([self.row, self.column])  # Добавляем в массив флагов
        elif self.flag == 1:  # Если флаг стоим
            self.flag = 2  # Ставим значение '?'
            self.button.configure(text='?', bg='blue')  # Выводим его
            flags.pop(flags.index([self.row, self.column]))  # Удаляем флаг из массива флагов
        elif self.flag == 2:  # Если вопрос
            self.flag = 0  # Устанавливаем на отсутствие флага
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


def seter(q, around, row, column):  # Получаем массив полей вокруг и координаты нажатого поля
    if q == bombs:  # Если кол-во установленных бомб = кол-ву заявленных
        for i in buttons:  # Шагаем по строкам
            for j in i:  # Шагаем по полям в строке i
                for k in j.around:  # Шагаем по полям вокруг выбранного поля j
                    if buttons[k[0]][k[1]].mine:  # Если в одном из полей k мина
                        buttons[buttons.index(i)][i.index(j)].value += 1  # То увеличиваем значение поля j
        return
    a = choice(buttons)  # Выбираем рандомную строку
    b = choice(a)  # Рандомное поле
    if [buttons.index(a), a.index(b)] not in mines and [buttons.index(a), a.index(b)] not in around and [
        buttons.index(a), a.index(b)] != [row,
                                          column]:  # Проверяем, что выбранное поле не выбиралось до этого и, что не является полем на которую мы нажали (или окружающим ее полем)
        b.mine = True  # Ставим мину
        mines.append([buttons.index(a), a.index(b)])  # Добавляем ее в массив
        seter(q + 1, around, row, column)  # Вызываем установщик, сказав, что одна мина уже есть
    else:
        seter(q, around, row, column)  # Вызываем установщик еще раз


def create_win_window():
    window = Tk()
    window.geometry('300x100')
    window.title('Вы победили!')
    winLabe = Label(window, text='Поздравляем!')
    winLabe.pack()
    window.mainloop()


def cheat(event):
    for t in mines:
        buttons[t[0]][t[1]].setFlag('<Button-1>')


def create_game_window(high, lenght):  # получаем значения
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
            j.button.bind('<Button-1>', j.view)  # Биндим открывание клетки
            j.button.bind('<Button-3>', j.setFlag)  # Установка флажка
            j.setAround()  # Функция заполнения массива self.around
    buttons[0][0].button.bind('<Control-Button-1>', cheat)  # создаем комбинацию клавиш для быстрого решения
    window.resizable(False, False)  # запрещаем изменения размера
    window.mainloop()


def configurate_and_run_game():
    global bombs
    high, lenght = read_settings()
    create_game_window(high, lenght)  # Начинаем игру, передавая кол-во полей


def read_settings():
    global bombs
    if mineText.get('1.0', END) == '\n':  # Проверяем наличие текста
        bombs = 10  # Если текста нет, то по стандарту кол-во бомб - 10
    else:
        bombs = int(mineText.get('1.0', END))  # Если текст есть, то это и будет кол-во бомб
    if highText.get('1.0', END) == '\n':
        high = 9
    else:
        high = int(highText.get('1.0', END))
    if lenghtText.get('1.0', END) == '\n':
        lenght = 9
    else:
        lenght = int(lenghtText.get('1.0', END))
    return high, lenght


def create_main_window():
    global mineText, highText, lenghtText

    window = Tk()
    window.title('Настройки')  # Пишем название окна
    window.geometry('200x150')  # Задаем размер
    mineText = Text(window, width=5, height=1)  # Создаем поля для ввода текста и пояснения
    mineLabe = Label(window, height=1, text='Бомбы:')
    highText = Text(window, width=5, height=1)
    highLabe = Label(window, height=1, text='Ширина:')
    lenghtText = Text(window, width=5, height=1)
    lenghtLabe = Label(window, height=1, text='Высота:')
    mineBut = Button(window, text='Начать:', command=configurate_and_run_game)  # Создаем кнопку
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
