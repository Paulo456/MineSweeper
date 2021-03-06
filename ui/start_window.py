from tkinter import Tk, Text, Label, Button, END

from ui.game_window import GameWindow


class StartWindow(object):
    def __init__(self):
        self.width = 9
        self.height = 9
        self.mines = 10

        self.window = Tk()
        self.window.title('Настройки')
        self.window.geometry('200x150')

        self.mine_input = None
        self.width_input = None
        self.height_input = None

        self.create_ui()

    def create_ui(self):
        self.mine_input = Text(self.window, width=5, height=1)  # Создаем поля для ввода текста и пояснения
        self.mine_input.insert(END, self.mines)
        self.mine_input.place(x=75, y=5)

        mines_label = Label(self.window, height=1, text='Бомбы:')
        mines_label.place(x=5, y=5)

        self.width_input = Text(self.window, width=5, height=1)
        self.width_input.insert(END, self.width)
        self.width_input.place(x=75, y=30)

        width_label = Label(self.window, height=1, text='Ширина:')
        width_label.place(x=5, y=30)

        self.height_input = Text(self.window, width=5, height=1)
        self.height_input.insert(END, self.height)
        self.height_input.place(x=75, y=55)

        height_label = Label(self.window, height=1, text='Высота:')
        height_label.place(x=5, y=55)

        button = Button(self.window, text='Начать:', command=self.start_game)
        button.place(x=70, y=90)

    def run(self):
        self.window.mainloop()

    def validate_settings(self):
        self.mines = self.validate_input(self.mine_input, 10)
        self.width = self.validate_input(self.width_input, 9)
        self.height = self.validate_input(self.height_input, 9)

    def validate_input(self, input, default):
        val = input.get('1.0', END)
        trimmed_val = val.lstrip().rstrip()
        if not trimmed_val:
            return default

        val = int(val)
        return val

    def start_game(self):
        self.validate_settings()
        game_window = GameWindow(self.width, self.height, self.mines)
        game_window.run()
