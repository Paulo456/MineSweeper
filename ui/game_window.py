from tkinter import Tk, Button, Frame, Label

import constants as const
from logic.minefield import Minefield


def get_color_by_value(value):
    if value == const.CELL_WITH_MINE:
        return 'red', 'red'
    if value == 0:
        return 'yellow', 'lightgrey'
    if value == 1:
        return 'green', 'lightgrey'
    if value == 2:
        return 'blue', 'lightgrey'
    if value == 3:
        return 'red', 'lightgrey'

    return 'purple', 'lightgrey'


class GameWindow(object):
    BUTTON_SIZE = 32

    def __init__(self, width, height, mines):
        self.minefield = Minefield(width, height, mines)

        self.window = Tk()
        self.window.geometry('%dx%d' % (width * self.BUTTON_SIZE, height * self.BUTTON_SIZE))
        self.window.title('Сапер')
        self.window.resizable(False, False)

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

        self.buttons[0][0].bind('<Control-Button-1>', self.cheat_clicked)

    def left_button_clicked(self, event):
        x_str, y_str = event.widget.name.split("x")
        x = int(x_str)
        y = int(y_str)

        opened_cells = self.minefield.open_cells(x, y)
        self.show_opened_cells(opened_cells)

        if self.minefield.is_game_ended(opened_cells) is const.GAME_STATE_LOST:
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

        if value == const.FLAG_ADDED:
            button.configure(text='F', bg='yellow')

        if value == const.FLAG_UNKNOWN:
            button.configure(text='?', bg='blue')

        if value == const.FLAG_NOT_SET:
            button.configure(text='   ', bg='white')

        if self.minefield.is_game_ended() is const.GAME_STATE_WIN:
            self.show_success_message()

    def cheat_clicked(self, event):
        all_cells = self.minefield.show_all_cells()
        self.show_opened_cells(all_cells)
        if self.minefield.is_game_ended() is const.GAME_STATE_WIN:
            self.show_success_message()
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

            if value == const.CELL_WITH_MINE:
                value = "M"
                button.configure(font=("Wingdings", 20))
            if value == 0:
                value = "  "

            color, background = get_color_by_value(value)
            button.configure(text=value, fg=color, bg=background)
