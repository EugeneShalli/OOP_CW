import tkinter as tk


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main_window(root)

    def init_main_window(self, root):
        
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.title("Bookshop manager")
    root.geometry("1050x650+400+200")
    root.resizable(False, False)
    root.mainloop()
