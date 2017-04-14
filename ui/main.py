from tkinter import Tk, Text, Label, Button, END

from ui.minefield import MinefieldWindow


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
