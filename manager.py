import tkinter as tk
from tkinter import ttk
import sqlite3
import pyodbc
import csv
import database as base
from xml.etree import ElementTree
import thread as thr
import pdfkit
from xml.dom.minidom import parse, parseString
from abc import ABC, abstractmethod
import time
import os
import exceptions as ex
import logging
#from xml.etree import ElementTree
import xml.etree.ElementTree as ET
# from lxml import etree as et

from fpdf import FPDF


flag = 0
choice = 0

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main(root)
        logging.info("Main window created")
        self.db = db
        self.view_records()
        logging.info("Records from DataBase viewed")

    def init_main(self, root):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)



        self.add_img = tk.PhotoImage(file='files/add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='files/update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='files/delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='files/refresh.gif')
        btn_open_dialog = tk.Button(toolbar, text='Рефреш', command=self.view_records, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.refresh_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='files/search.gif')
        btn_open_dialog = tk.Button(toolbar, text='Поиск', command=self.search, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.search_img)
        btn_open_dialog.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'title', 'author', 'publisher', 'price', 'selfprice', 'amount'),
                                 height=30, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('title', width=310, anchor=tk.CENTER)
        self.tree.column('author', width=205, anchor=tk.CENTER)
        self.tree.column('publisher', width=200, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)
        self.tree.column('selfprice', width=100, anchor=tk.CENTER)
        self.tree.column('amount', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('title', text='Наименование', command=lambda: \
            self.treeview_sort_column(self.tree, 'title', False))
        self.tree.heading('author', text='Автор', command=lambda: \
            self.treeview_sort_column(self.tree, 'author', False))
        self.tree.heading('publisher', text='Издательство', command=lambda: \
            self.treeview_sort_column(self.tree, 'publisher', False))
        self.tree.heading('price', text='Цена', command=lambda: \
            self.treeview_sort_column(self.tree, 'price', False))
        self.tree.heading('selfprice', text='Себестоимость', command=lambda: \
            self.treeview_sort_column(self.tree, 'selfprice', False))
        self.tree.heading('amount', text='Количество', command=lambda: \
            self.treeview_sort_column(self.tree, 'amount', False))

        label_name = tk.Label(toolbar, text='Поле поиска:', bg='#d7d8e0')
        label_name.place(x=830, y=5)

        label_name = tk.Label(toolbar, text='Ищем:', bg='#d7d8e0')
        label_name.place(x=830, y=35)

        label_name = tk.Label(toolbar, text='До:', bg='#d7d8e0')
        label_name.place(x=830, y=65)
        self.entry_sear = ttk.Entry(toolbar, width=40)
        self.entry_sear.place(x=920, y=65)

        self.combobox = ttk.Combobox(toolbar, values=[u'Название', u'Автор', u'Издательство', u'Цена от',
                                                      u'Количество от'], width=37)
        self.combobox.place(x=920, y=5)

        self.entry_search = ttk.Entry(toolbar, width=40)
        self.entry_search.place(x=920, y=35)

        self.tree.pack()

        ###################################################
        downbar = tk.Frame(bg='white', bd=2)
        downbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.export_csv = tk.PhotoImage(file='files/csv.gif')
        btn_open_dialog = tk.Button(downbar, text='Экспортв в CSV', command=self.write_csv, bg='white', bd=0,
                                    compound=tk.TOP, image=self.export_csv)
        btn_open_dialog.pack(side=tk.LEFT)

        self.export_xml = tk.PhotoImage(file='files/xml.gif')
        btn_open_dialog = tk.Button(downbar, text='Экспортв в XML', command=self.write_xml, bg='white', bd=0,
                                    compound=tk.TOP, image=self.export_xml)
        btn_open_dialog.pack(side=tk.LEFT)

        self.export_html = tk.PhotoImage(file='files/html.gif')
        btn_open_dialog = tk.Button(downbar, text='Экспортв в HTML', command=self.create_html, bg='white', bd=0,
                                    compound=tk.TOP, image=self.export_html)
        btn_open_dialog.pack(side=tk.LEFT)

        self.export_pdf = tk.PhotoImage(file='files/pdf.gif')
        btn_open_dialog = tk.Button(downbar, text='Экспортв в PDF', command=self.create_pdf, bg='white', bd=0,
                                    compound=tk.TOP, image=self.export_pdf)
        btn_open_dialog.pack(side=tk.LEFT)

        self.export_all = tk.PhotoImage(file='files/all.gif')
        btn_open_dialog = tk.Button(downbar, text='Экспортв в ALL', command=self.threads, bg='white', bd=0,
                                    compound=tk.TOP, image=self.export_all)
        btn_open_dialog.pack(side=tk.LEFT)


        self.import_csv = tk.PhotoImage(file='files/fromcsv.gif')
        btn_open_dialog = tk.Button(downbar, text='Импорт из CSV', command=self.read_csv, bg='white', bd=0,
                                    compound=tk.TOP, image=self.import_csv)
        btn_open_dialog.pack(side=tk.RIGHT)

        self.import_xml = tk.PhotoImage(file='files/fromxml.gif')
        btn_open_dialog = tk.Button(downbar, text='Импорт из XML', command=self.read_xml, bg='white', bd=0,
                                    compound=tk.TOP, image=self.import_xml)
        btn_open_dialog.pack(side=tk.RIGHT)

        ###################################################


        ############################################################
        self.put_bucket = tk.PhotoImage(file='files/buy.gif')
        btn_put = tk.Button(toolbar, text='Добавить в корзину', bg='#d7d8e0', bd=0,
                            image=self.put_bucket,
                            compound=tk.TOP, command=self.put_to_bucket)
        btn_put.pack(side=tk.LEFT)

        self.bucket_img = tk.PhotoImage(file='files/bag.gif')
        btn_bucket = tk.Button(toolbar, text='Открыть корзину', bg='#d7d8e0', bd=0,
                               image=self.bucket_img,
                               compound=tk.TOP, command=self.open_bucket)
        btn_bucket.pack(side=tk.LEFT)
        # btn_bucket = tk.Button(toolbar, text='R', bg='#d7d8e0', bd=0,  # image=self.bucket_img,
        #                        compound=tk.TOP, command=self.view_records)
        # btn_bucket.pack(side=tk.LEFT)
        ############################################################

    def records(self, title, author, publisher, price, selfprice, amount):
        self.db.insert_data(title, author, publisher, price, selfprice, amount)
        self.view_records()

    def search(self):
        self.val = self.combobox.get()

        if self.val == 'Название':
            line = '%' + self.entry_search.get() + '%'
            self.db.c.execute("SELECT * FROM books WHERE title LIKE ?", (line,))
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
             self.db.c.fetchall()]
        elif self.val == 'Автор':
            line = '%' + self.entry_search.get() + '%'
            self.db.c.execute("SELECT * FROM books WHERE author LIKE ?", (line,))
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
             self.db.c.fetchall()]
        elif self.val == 'Издательство':
            line = '%' + self.entry_search.get() + '%'
            self.db.c.execute("SELECT * FROM books WHERE publisher LIKE ?", (line,))
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
             self.db.c.fetchall()]
        elif self.val == 'Цена от':
            if len(self.entry_search.get()) == 0:
                self.entry_search.insert(0, 0)
            self.db.c.execute("SELECT * FROM books WHERE price BETWEEN ? AND ?", (self.entry_search.get(),
                                                                                  self.entry_sear.get(),))
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
             self.db.c.fetchall()]
        elif self.val == 'Количество от':
            if len(self.entry_search.get()) == 0:
                self.entry_search.insert(0, 0)
            self.db.c.execute("SELECT * FROM books WHERE amount BETWEEN ? AND ?", (self.entry_search.get(),
                                                                                   self.entry_sear.get(),))
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
             self.db.c.fetchall()]

    def update_record(self, title, author, publisher, price, selfprice, amount, ID):
        logging.info("Button update_record pressed")
        global flag
        flag = 0
        try:
            var1 = int(price)
            var2 = int(selfprice)
            var3 = int(amount)
            if len(title) == 0:
                raise MyException
            if len(author) == 0:
                raise MyException
            if len(publisher) == 0:
                raise MyException
        except (TypeError, ValueError):
            ex.Exceptwindow1()
            flag = 1
        except MyException:
            ex.Exceptwindow2()
            flag = 1
        if flag == 0:
            self.db.c.execute('''UPDATE books SET title=?, author=?, publisher=?, price=?, selfprice=?, amount=? 
            WHERE ID=?''', (title, author, publisher, price, selfprice, amount, ID))
        self.db.conn.commit()
        self.view_records()

    def endwork(self, bla, name, author, publisher, price, selfprice, amount):
        bla.view.records(name, author, publisher, price, selfprice, amount)
        bla.entry_name.delete(0, 'end')
        bla.entry_author.delete(0, 'end')
        bla.entry_publisher.delete(0, 'end')
        bla.entry_price.delete(0, 'end')
        bla.entry_selfprice.delete(0, 'end')
        bla.entry_amount.delete(0, 'end')

    def view_records(self):
        self.db.c.execute('''SELECT * FROM books''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) for row in
         self.db.c.fetchall()]

    def delete_records(self):
        logging.info("Button delete_records pressed")
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM books WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def open_dialog(self):
        logging.info("Button add_new pressed")
        Child()

    def create_pdf(self):
        logging.info("Button create_pdf pressed")
        db.create_pdf()

    def create_html(self):
        logging.info("Button create_html pressed")
        db.create_html()

    def write_csv(self):
        logging.info("Button write_csv pressed")
        db.write_to_csv()

    def read_csv(self):
        logging.info("Button read_from_csv pressed")
        db.read_from_csv()
        self.view_records()

    def write_xml(self):
        logging.info("Button write_xml pressed")
        db.write_to_xml()

    def read_xml(self):
        logging.info("Button read_xml pressed")
        db.read_from_xml()

    def threads(self):
        logging.info("Button write_all pressed")
        db.parallel()

    def put_to_bucket(self):
        logging.info("Put to bucket")
        id=self.tree.set(self.tree.selection()[0], '#1')
        self.db.c.execute('''SELECT * FROM books WHERE ID=? ''', (id,))
        item = self.db.c.fetchall()
        it = item[0][6]-1
        if it < 1:
            self.db.c.execute('''DELETE FROM books WHERE ID=?''', (id,))
        else:
            self.db.c.execute('''UPDATE books SET title=?, author=?, publisher=?, price=?, selfprice=?, amount=? WHERE ID=?''', (item[0][1], item[0][2], item[0][3], item[0][4], item[0][5], it, id))
        self.db.c.execute(''' SELECT count(*) FROM bucket WHERE title LIKE ?''', (item[0][1], ))

        # if the count is 1, then table exists
        if self.db.c.fetchone()[0] == 1:
            self.db.c.execute('''SELECT * FROM bucket WHERE title LIKE ? ''', (item[0][1],))
            item2 = self.db.c.fetchall()
            self.db.c.execute('''UPDATE bucket SET title=?, author=?, publisher=?, price=?, amount=? WHERE ID=?''',
                              (item2[0][1], item2[0][2], item2[0][3], item2[0][4], item2[0][5]+1, item2[0][0]))
        else:
            self.db.c.execute('''INSERT INTO bucket(title, author, publisher, price, amount) VALUES(?, ?, ?, ?, ?)''',
                          (item[0][1], item[0][2], item[0][3], item[0][4], 1))

        #self.db.c.execute('''UPDATE products SET name=?, category=?, count=?, price=? WHERE ID=?''',
        #                  (name, category, count, price, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_bucket(self):
        root2 = tk.Tk()
        root2.title("Корзина°")
        root2.geometry("1280x820+400+200")
        root2.resizable(False, False)

        buck = Bucket(root2)
        buck.pack()
        root2.mainloop()



    def open_update_dialog(self):

        self.db.c.execute("SELECT * FROM books WHERE ID=?", (self.tree.set(self.tree.selection()[0], '#1'),))
        ID = self.tree.set(self.tree.selection()[0], '#1')
        name = self.db.c.fetchall()

        Update(name, ID)

    def treeview_sort_column(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
            #      ^^^^^^^^^^^^^^^^^^^^^^^
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: self.treeview_sort_column(tree, col, not reverse))


class MyException(Exception):
    pass


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def checkdata(self, name, author, publisher, price, selfprice, amount):
        global flag
        flag = 0
        try:
            var1 = int(price)
            var2 = int(selfprice)
            var3 = int(amount)
            if len(name) == 0:
                raise MyException
            if len(author) == 0:
                raise MyException
            if len(publisher) == 0:
                raise MyException
        except (TypeError, ValueError):
            ex.Exceptwindow1()
            flag = 1
        except MyException:
            ex.Exceptwindow2()
            flag = 1
        if flag == 0:
            But(self, name, author, publisher, price, selfprice, amount)

    def init_child(self):
        self.title('Добавить товар')
        self.geometry('420x250+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='Название:')
        label_name.place(x=50, y=30)
        label_author = tk.Label(self, text='Автор:')
        label_author.place(x=50, y=60)
        label_publisher = tk.Label(self, text='Издательство:')
        label_publisher.place(x=50, y=90)
        label_price = tk.Label(self, text='Цена:')
        label_price.place(x=50, y=120)
        label_selfprice = tk.Label(self, text='Себестоимость:')
        label_selfprice.place(x=50, y=150)
        label_amount = tk.Label(self, text='Количество:')
        label_amount.place(x=50, y=180)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=150, y=30, width=230)

        self.entry_author = ttk.Entry(self)
        self.entry_author.place(x=150, y=60, width=230)

        self.entry_publisher = ttk.Entry(self)
        self.entry_publisher.place(x=150, y=90, width=230)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=150, y=120, width=230)

        self.entry_selfprice = ttk.Entry(self)
        self.entry_selfprice.place(x=150, y=150, width=230)

        self.entry_amount = ttk.Entry(self)
        self.entry_amount.place(x=150, y=180, width=230)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=320, y=215)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=240, y=215)
        self.btn_ok.bind('<Button-1>', lambda event: self.checkdata(self.entry_name.get(),
                                                                    self.entry_author.get(),
                                                                    self.entry_publisher.get(),
                                                                    self.entry_price.get(),
                                                                    self.entry_selfprice.get(),
                                                                    self.entry_amount.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self, name, ID):
        super().__init__()
        self.init_edit(name, ID)
        self.view = app

    def init_edit(self, name, ID):
        self.title('Редактировать товар')
        btn_edit = ttk.Button(self, text='Редактировать', command=self.destroy)
        btn_edit.place(x=225, y=215)

        self.entry_name.insert(0, name[0][1])
        self.entry_author.insert(0, name[0][2])
        self.entry_publisher.insert(0, name[0][3])
        self.entry_price.insert(0, name[0][4])
        self.entry_selfprice.insert(0, name[0][5])
        self.entry_amount.insert(0, name[0][6])

        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_author.get(),
                                                                          self.entry_publisher.get(),
                                                                          self.entry_price.get(),
                                                                          self.entry_selfprice.get(),
                                                                          self.entry_amount.get(), ID))

        self.btn_ok.destroy()


class But(tk.Toplevel):
    def __init__(self, bla, name, author, publisher, price, selfprice, amount):
        super().__init__()
        self.view = app
        self.init_child(bla, name, author, publisher, price, selfprice, amount)

    def init_child(self, bla, name, author, publisher, price, selfprice, amount):
        self.title('Добавление')
        self.geometry('420x250+400+300')
        self.resizable(False, False)

        label_error = tk.Label(self, font='Courier 14', text='Вы уверены, что хотите добавить?')
        label_error.place(x=30, y=100)

        btn_yes = ttk.Button(self, text='Да', command=self.destroy)
        btn_yes.place(x=210, y=215)
        btn_yes.bind('<Button-1>', lambda event: self.view.endwork(bla, name, author, publisher, price,
                                                                   selfprice, amount))

        btn_cancel = ttk.Button(self, text='Нет', command=self.destroy)
        btn_cancel.place(x=300, y=215)

        self.grab_set()
        self.focus_set()







##################################################################################################################
class Bucket(tk.Frame):
    def __init__(self, root2):
        logging.info("Open the bucket")
        self.root2=root2
        self.db = db
        super().__init__(root2)
        self.init_main(root2)
        #self.Title('РљРѕСЂР·РёРЅР°')
        self.init_bucket()
        # Table.init_this(self)
        self.view = app
        self.view_records()

    def init_main(self, root):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # self.add_img = tk.PhotoImage(file='files/add.gif')
        # btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
        #                             compound=tk.TOP, image=self.add_img)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.update_img = tk.PhotoImage(file='files/update.gif')
        # btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
        #                             compound=tk.TOP, command=self.open_update_dialog)
        # btn_edit_dialog.pack(side=tk.LEFT)
        #
        # self.delete_img = tk.PhotoImage(file='files/delete.gif')
        # btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
        #                        compound=tk.TOP, command=self.delete_records)
        # btn_delete.pack(side=tk.LEFT)
        #
        # self.refresh_img = tk.PhotoImage(file='files/refresh.gif')
        # btn_open_dialog = tk.Button(toolbar, text='Рефреш', command=self.view_records, bg='#d7d8e0', bd=0,
        #                             compound=tk.TOP, image=self.refresh_img)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.search_img = tk.PhotoImage(file='files/search.gif')
        # btn_open_dialog = tk.Button(toolbar, text='Поиск', command=self.search, bg='#d7d8e0', bd=0,
        #                             compound=tk.TOP, image=self.search_img)
        # btn_open_dialog.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('ID', 'title', 'author', 'publisher', 'price', 'amount'),
                                 height=30, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('title', width=310, anchor=tk.CENTER)
        self.tree.column('author', width=205, anchor=tk.CENTER)
        self.tree.column('publisher', width=200, anchor=tk.CENTER)
        self.tree.column('price', width=100, anchor=tk.CENTER)
        #self.tree.column('selfprice', width=100, anchor=tk.CENTER)
        self.tree.column('amount', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('title', text='Наименование', command=lambda: \
            self.treeview_sort_column(self.tree, 'title', False))
        self.tree.heading('author', text='Автор', command=lambda: \
            self.treeview_sort_column(self.tree, 'author', False))
        self.tree.heading('publisher', text='Издательство', command=lambda: \
            self.treeview_sort_column(self.tree, 'publisher', False))
        self.tree.heading('price', text='Цена', command=lambda: \
            self.treeview_sort_column(self.tree, 'price', False))
        # self.tree.heading('selfprice', text='Себестоимость', command=lambda: \
        #     self.treeview_sort_column(self.tree, 'selfprice', False))
        self.tree.heading('amount', text='Количество', command=lambda: \
            self.treeview_sort_column(self.tree, 'amount', False))

        label_name = tk.Label(toolbar, text='Поле поиска:', bg='#d7d8e0')
        label_name.place(x=830, y=5)

        label_name = tk.Label(toolbar, text='Ищем:', bg='#d7d8e0')
        label_name.place(x=830, y=35)

        label_name = tk.Label(toolbar, text='До:', bg='#d7d8e0')
        label_name.place(x=830, y=65)
        self.entry_sear = ttk.Entry(toolbar, width=40)
        self.entry_sear.place(x=920, y=65)

        self.combobox = ttk.Combobox(toolbar, values=[u'Название', u'Автор', u'Издательство', u'Цена от',
                                                      u'Количество от'], width=37)
        self.combobox.place(x=920, y=5)

        self.entry_search = ttk.Entry(toolbar, width=40)
        self.entry_search.place(x=920, y=35)

        self.tree.pack()

        ###################################################
        downbar = tk.Frame(bg='white', bd=2)
        downbar.pack(side=tk.BOTTOM, fill=tk.X)

        # self.export_csv = tk.PhotoImage(file='files/csv.gif')
        # btn_open_dialog = tk.Button(downbar, text='Экспортв в CSV', command=self.write_csv, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.export_csv)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.export_xml = tk.PhotoImage(file='files/xml.gif')
        # btn_open_dialog = tk.Button(downbar, text='Экспортв в XML', command=self.write_xml, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.export_xml)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.export_html = tk.PhotoImage(file='files/html.gif')
        # btn_open_dialog = tk.Button(downbar, text='Экспортв в HTML', command=self.create_html, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.export_html)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.export_pdf = tk.PhotoImage(file='files/pdf.gif')
        # btn_open_dialog = tk.Button(downbar, text='Экспортв в PDF', command=self.create_pdf, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.export_pdf)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.export_all = tk.PhotoImage(file='files/all.gif')
        # btn_open_dialog = tk.Button(downbar, text='Экспортв в ALL', command=self.threads, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.export_all)
        # btn_open_dialog.pack(side=tk.LEFT)
        #
        # self.import_csv = tk.PhotoImage(file='files/fromcsv.gif')
        # btn_open_dialog = tk.Button(downbar, text='Импорт из CSV', command=self.read_csv, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.import_csv)
        # btn_open_dialog.pack(side=tk.RIGHT)
        #
        # self.import_xml = tk.PhotoImage(file='files/fromxml.gif')
        # btn_open_dialog = tk.Button(downbar, text='Импорт из XML', command=self.read_xml, bg='white', bd=0,
        #                             compound=tk.TOP, image=self.import_xml)
        # btn_open_dialog.pack(side=tk.RIGHT)

        ###################################################

        ############################################################
        # btn_put = tk.Button(toolbar, text='Добавить в корзину', bg='#d7d8e0', bd=0,
        #                     # image=self.bucket_img,
        #                     compound=tk.TOP, command=self.put_to_bucket)
        # btn_put.pack(side=tk.LEFT)
        #
        # # self.bucket_img = tk.PhotoImage(file='bucket.png')
        # btn_bucket = tk.Button(toolbar, text='Открыть корзину', bg='#d7d8e0', bd=0,
        #                        # image=self.bucket_img,
        #                        compound=tk.TOP, command=self.open_bucket)
        # btn_bucket.pack(side=tk.LEFT)
        # btn_bucket = tk.Button(toolbar, text='R', bg='#d7d8e0', bd=0,  # image=self.bucket_img,
        #                        compound=tk.TOP, command=self.view_records)
        # btn_bucket.pack(side=tk.LEFT)
        ############################################################

    def init_bucket(self):
        #self.title('РљРѕСЂР·РёРЅР°')
        btn_can = ttk.Button(self, text='Закрыть', command=self.root2.destroy)
        btn_can.pack(side=tk.BOTTOM)
        btn_del = ttk.Button(self, text='Убрать', command=self.delete_records)
        btn_del.pack(side=tk.BOTTOM)
        btn_buy = ttk.Button(self, text='Оформить', command=self.buy_something)
        btn_buy.pack(side=tk.BOTTOM)
        self.view_records()

        #btn_buy.bind('<Button-2>', lambda event: self.destroy)

    def view_records(self):
        # self.db.c.execute('''SELECT * FROM bucket''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        # [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
        # self.db.c.execute('''SELECT * FROM bucket''')
        # self.items = self.db.c.fetchall()
        self.db.c.execute('''SELECT * FROM bucket''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5])) for row in
         self.db.c.fetchall()]
        self.items = self.db.c.fetchall()
        a = 0
        for i in range(0, len(self.items)):
            a=a+int(self.items[i][4])*int(self.items[i][5])
            print(a)
        label_count = tk.Label(self, text='Итого: ' + str(a))
        label_count.place(x=500, y=340)

    def buy_something(self):
        #for selection_item in self.tree.selection():
        logging.info("buy something")
        self.db.c.execute('''SELECT * FROM bucket''')
        items = []
        for item in self.db.c:
            items.append(item)
        headers = self.db.c.description
        # thread = Threads.CsvThread("check.csv", "CSV", items, headers)
        # thread.start()
        # thread1 = Threads.HtmlThread("check.csv", "CSV", items, headers)
        # thread1.start()
        # thread1 = Threads.XmlThread("check.csv", "CSV", items, headers)
        # thread1.start()
        #with open("check.csv", "w", newline='') as csv_file:
        #    self.csv_writer = csv.writer(csv_file)
        #    self.csv_writer.writerow([i[0] for i in headers])  # write headers
        #    self.csv_writer.writerows(items)
        self.db.c.execute('''DELETE FROM bucket''')
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):

        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.c.execute('''SELECT * FROM bucket WHERE ID=? ''', (id,))
        logging.info("Delete position")
        item = self.db.c.fetchall()
        it = item[0][5] - 1
        if it < 1:
            self.db.c.execute('''DELETE FROM bucket WHERE ID=?''', (id,))
        else:
            self.db.c.execute('''UPDATE bucket SET title=?, author=?, publisher=?, price=?, amount=? WHERE ID=?''',
                              (item[0][1], item[0][2], item[0][3], item[0][4], it, id))
        self.db.c.execute(''' SELECT count(*) FROM books WHERE title LIKE ?''', (item[0][1],))

        # if the count is 1, then table exists
        if self.db.c.fetchone()[0] == 1:
        # try:
            self.db.c.execute('''SELECT * FROM books WHERE title LIKE ? ''', (item[0][1],))
            item2 = self.db.c.fetchall()

            self.db.c.execute('''UPDATE books SET title=?, author=?, publisher=?, price=?, amount=amount+1 WHERE(title LIKE ? AND price=?)''',
                              (item[0][1], item[0][2], item[0][3], item[0][4], item[0][1], item[0][4]))
        else:
            self.db.c.execute('''INSERT INTO books(title, author, publisher, price, selfprice, amount) VALUES(?, ?, ?, ?, ?, ?)''',
                              (item[0][1], item[0][2], item[0][3], item[0][4], int(item[0][4]*0.8), 1))

        # self.db.c.execute('''UPDATE products SET name=?, category=?, count=?, price=? WHERE ID=?''',
        #                  (name, category, count, price, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()
##################################################################################################################


if __name__ == "__main__":
    logger = logging.getLogger("mainApp")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("manager.log")
    formatter = logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
                                    level=logging.INFO, filename=u'manager.log', filemode="w")


    logging.info("Program started")


    root = tk.Tk()
    db = base.DB()
    app = Main(root)
    app.pack()
    root.title("Bookshop Manager")
    root.geometry("1280x820+400+200")
    root.resizable(False, False)
    root.mainloop()

    thr.log()

    logging.info("Program finished")
