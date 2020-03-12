import tkinter as tk
from tkinter import ttk
import logging

class Exceptwindow1(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # self.view = app
        self.init_child()

    def init_child(self):
        logging.info("Raised exception 1")

        self.title('Ошибка')
        self.geometry('420x250+400+300')
        self.resizable(False, False)

        label_error = tk.Label(self, font='Courier 14', text='Цена, Себестоимость и Количество \n должны быть числами')
        label_error.place(x=30, y=100)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=215)

        self.grab_set()
        self.focus_set()


class Exceptwindow2(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # self.view = app
        self.init_child()

    def init_child(self):
        logging.info("Raised exception 2")

        self.geometry('420x250+400+300')
        self.resizable(False, False)

        label_error = tk.Label(self, font='Courier 14', text='Название, Автор и Издательство \n не могут быть пустыми')
        label_error.place(x=35, y=100)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=215)

        self.grab_set()
        self.focus_set()

class MyException(Exception):
    pass
