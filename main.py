import tkinter as tk
from tkinter import ttk
import pyodbc
"""
This is program to manage the bookshop storage
"""


class MainWindow(tk.Frame):
    """
    Main window form class
    """
    def __init__(self, root):
        """
        Initializing of the Object(MainWindow) and starting to fill it with components
        :param root:
        """
        super().__init__(root)
        self.init_main_window(root)
        self.db = db
        self.view_records()

    def init_main_window(self, root):
        """
        Creating and filling of MainWindow with different interactive buttons and elements:
        Toolbar, Add Button, Edit Button, Delete Button,
        :param root:
        :return:
        """

        # Toolbar adding
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Adding of button "Add"
        self.add_img = tk.PhotoImage(file='files/add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить', bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        # Adding of button "Edit"
        self.update_img = tk.PhotoImage(file='files/update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Adding of button "Delete"
        self.delete_img = tk.PhotoImage(file='files/delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0,
                               compound=tk.TOP, image=self.delete_img)
        btn_delete.pack(side=tk.LEFT)

        # Adding of button "Refresh"
        self.refresh_img = tk.PhotoImage(file='files/refresh.gif')
        btn_refresh_dialog = tk.Button(toolbar, text='Рефреш', bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.refresh_img)
        btn_refresh_dialog.pack(side=tk.LEFT)

        # Adding of button "Add to the basket"
        self.put_basket_img = tk.PhotoImage(file='files/buy.gif')
        btn_put_basket_dialog = tk.Button(toolbar, text='Открыть', bg='#d7d8e0', bd=0,
                                       compound=tk.TOP, image=self.put_basket_img)
        btn_put_basket_dialog.pack(side=tk.LEFT)
        
        # Adding of button "Open the basket"
        self.basket_img = tk.PhotoImage(file='files/bag.gif')
        btn_basket_dialog = tk.Button(toolbar, text='Сохранить', bg='#d7d8e0', bd=0,
                                          compound=tk.TOP, image=self.basket_img)
        btn_basket_dialog.pack(side=tk.LEFT)

        # Adding of button "Search"
        self.search_img = tk.PhotoImage(file='files/search.gif')
        btn_search_dialog = tk.Button(toolbar, text='Расширенный поиск', bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.search_img)
        btn_search_dialog.pack(side=tk.RIGHT)

        # Creating and placing of search elements
        label_name = tk.Label(toolbar, text='Поле поиска:', bg='#d7d8e0')
        label_name.place(x=585, y=5)

        label_name = tk.Label(toolbar, text='Ищем:', bg='#d7d8e0')
        label_name.place(x=585, y=35)

        label_name = tk.Label(toolbar, text='До:', bg='#d7d8e0')
        label_name.place(x=585, y=65)

        # Creating Combobox of search fields
        self.combobox = ttk.Combobox(toolbar, values=[u'Название', u'Автор', u'Издательство', u'Цена от',
                                                      u'Количество от'], width=37)
        self.combobox.place(x=675, y=5)

        # Creating a field to take the search parametr
        self.entry_search1 = ttk.Entry(toolbar, width=40)
        self.entry_search1.place(x=675, y=35)

        # Creating a field to take the search parametr
        self.entry_searср2 = ttk.Entry(toolbar, width=40)
        self.entry_searср2.place(x=675, y=65)

        self.tree = ttk.Treeview(self, columns=('ID', 'title', 'author', 'publisher', 'price', 'selfprice', 'amount'),
                                 height=30, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('title', width=310, anchor=tk.CENTER)
        self.tree.column('author', width=205, anchor=tk.CENTER)
        self.tree.column('publisher', width=200, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)
        self.tree.column('selfprice', width=100, anchor=tk.CENTER)
        self.tree.column('amount', width=100, anchor=tk.CENTER)

        self.tree.pack()

    def view_records(self):
        result = self.db.cursor.execute('''SELECT * FROM books''').fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in result]

    def records(self, title, author, publisher, price, selfprice, amount):
        self.db.insert_data(title, author, publisher, price, selfprice, amount)
        self.view_records()



class DB:
    def __init__(self):
        self.server = 'DESKTOP-T7F4G41'
        self.database = 'example'
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + self.server + '; DATABASE=' + self.database +
            '; Trusted_Connection=yes;' + ' MARS_Connection = Yes;')
        self.cursor = self.conn.cursor()

        print("Successful connection")

        try:
            self.cursor.execute(
                """
                SELECT count(*) FROM example.dbo.books
                """
            )
            exist = True
        except:
            exist = False

        if not exist:
            self.cursor.execute('''CREATE TABLE books (id INTEGER IDENTITY NOT NULL PRIMARY KEY, title text, author text, publisher text,
                             price integer, selfprice integer, amount integer )''')
            self.conn.commit()


    def insert_data(self, id, title, author, publisher, price, selfprice, amount):
        insert_query = '''INSERT into books VALUES (?, ?, ?, ?, ?, ?, ?)'''

        self.cursor.execute(insert_query, id, title, author, publisher, price, selfprice, amount)
        self.conn.commit()



if __name__ == "__main__":

    # server = 'DESKTOP-T7F4G41'
    # database = 'example'
    #
    # server_connection(server, database)
    id = 2
    title = "AAAAAAAAA"
    author = "Tolstoy"
    publisher = "AST"
    price = 360
    selfprice = 200
    amount = 12
    db = DB()
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.title("Bookshop manager")
    root.geometry("1050x650+400+200")
    root.resizable(False, False)
    root.mainloop()
