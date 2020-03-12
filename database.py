import tkinter as tk
from tkinter import ttk
import logging
import pyodbc
import csv
from lxml import etree as et
from xml.etree import ElementTree
import thread as thr
from fpdf import FPDF, HTMLMixin
import pdfkit
from bs4 import BeautifulSoup
from threading import Thread
import codecs


class HTML2PDF(FPDF, HTMLMixin):
    pass


class DB:
    def __init__(self):
        self.server = 'DESKTOP-T7F4G41'
        self.database = 'example'
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + self.server + '; DATABASE=' + self.database +
            '; Trusted_Connection=yes;' + ' MARS_Connection = Yes;')
        self.c = self.conn.cursor()

        print("Successful connection")

        try:
            self.c.execute(
                """
                SELECT count(*) FROM example.dbo.books
                """
            )
            exist = True
        except:
            exist = False

        if not exist:
            self.c.execute(
                '''CREATE TABLE books (id INTEGER IDENTITY NOT NULL PRIMARY KEY, title text, author text, publisher text,
                 price integer, selfprice integer, amount integer )''')
            self.c.execute(
                '''CREATE TABLE bucket (id INTEGER IDENTITY NOT NULL PRIMARY KEY,
                                                                 title text, 
                                                                 author text, 
                                                                 publisher text, 
                                                                 price integer,
                                                                 amount integer)''')
            self.conn.commit()

        # self.conn = sqlite3.connect('files/books.db')
        # self.c = self.conn.cursor()
        # self.c.execute(
        #     '''CREATE TABLE IF NOT EXISTS books (id integer primary key, title text, author text, publisher text,
        #      price integer, selfprice integer, amount integer )''')
        # self.conn.commit()

    def insert_data(self, title, author, publisher, price, selfprice, amount):
        self.c.execute('''INSERT INTO books(title, author, publisher, price, selfprice, amount) VALUES (?, ?, ?, ?, ?,
         ?)''', (title, author, publisher, price, selfprice, amount))
        self.conn.commit()

    def read_from_csv(self):
        with open('test.csv', 'r') as f:
            reader = csv.reader(f)
            columns = next(reader)
            #query = 'insert into books({0}) values ({1})'
            #query = query.format(','.join(columns), ','.join('?' * len(columns)))
            # cursor = connection.cursor()
            for data in reader:
                self.insert_data(data[1], data[2], data[3], data[4], data[5], data[6])
                #self.c.execute(query, data)
            #self.c.commit()

    def write_to_csv(self):
        # cursor = coon.cursor()
        sql = """Select * from books"""
        self.c.execute(sql)

        row = self.c.fetchall()
        with open('test.csv', 'w', newline='') as f:
            a = csv.writer(f, delimiter=',')
            a.writerow(["id", "title", 'author', 'publisher', 'price', 'selfprice', 'amount'])  ## etc
            a.writerows(row)  ## closing paren added

    def read_from_xml(self):
        tree = ElementTree.parse('xml_file.xml')
        root = tree.getroot()
        #query = 'insert into books({0}) values ({1})'

        #query = query.format(','.join(columns), ','.join('?' * len(columns)))


        for book in root:
            #for atr in book:
            #self.insert_data(atr.text[0])
            # query = 'insert into books values ()'
            # self.insert_data(data[1].text, data[2].text, data[3].text, data[4].text, data[5], data[6])
            self.insert_data(book[1].text, book[2].text, book[3].text, int(book[4].text), int(book[5].text), int(book[6].text))
            #print(book[1].text, book[2].text, book[3].text, book[4].text, book[5].text, book[6].text)
            #print(book.tag, book.attrib)
    ####################################################

    def create_html(self):
        # self.write_to_xml()
        # tree = ElementTree.parse("xml_file.xml")
        # root = tree.getroot()
        #
        # #root = ElementTree.getroot()
        # #xhtml = ("xml_file.xml")


        sql = """Select * from books"""
        self.c.execute(sql)
        root = ElementTree.Element("table", width="100%")
        flag = 1
        help = ElementTree.SubElement(root, "tr")
        self.name_to_html(help)
        for row in self.c.fetchall():
            name = "tr"
            book1 = ElementTree.SubElement(root, name)
            # if flag:
            #     flag = 0
            # else:
            self.book_to_html(row, book1)


        tree = ElementTree.ElementTree(root)

        tree.write("html_file.html", "utf-8")

        # pdfkit.from_file('html_file.html', 'chiter.pdf')


    def create_pdf(self):
        pass
        # xml = "xml_file.xml"
        # pdf = "pdf_file.pdf"
        # doc = PDFOrder(xml, pdf)
        # doc.createPDF()
        # doc.savePDF()

        # with open("xml_file.xml") as fobj:
        #     xml = fobj.read()
        # root = ElementTree.fromstring(xml)
        # #pdf = PDFOrder(xml, pdf)
        # pdf = FPDF()
        # pdf.set_font("Arial", size=14)
        # pdf.add_page()
        #
        # col_width = pdf.w / 8
        # row_height = pdf.font_size
        # children = root.getchildren()
        # for row in children:
        #     child = row.getchildren()
        #     for item in child:
        #         pdf.cell(col_width, row_height, txt=item.text, border=1)
        #     pdf.ln(row_height * 1)
        #pdf.output('simple_table.pdf')

        # tree = et.parse("html_file.html")
        # table = et.tostring(tree.getroot())
        # # soup = BeautifulSoup(''.join(table))
        #
        # pdf = HTML2PDF()
        #
        # pdf.add_page()
        #
        # #table =
        # # table = soup
        # html = str(table.decode("utf-8"))
        # # html = soup
        # print(html)
        # pdf.write_html(html)
        # pdf.output("pdf_file.pdf")

        # with open("xml_file.xml", encoding='utf-8') as fobj:
        #     xml = fobj.read()
        # #file = codecs.open("xml_file.xml", "r", "utf-8")
        # #xml = file.read()
        # root = et.fromstring(xml)
        # # root.decode("utf-8")
        # pdf = FPDF()
        # pdf.set_font("Arial", size=14)
        # pdf.add_page()
        #
        # col_width = pdf.w / 8.5
        # row_height = pdf.font_size
        # for row in root:
        #     #for item in row.getchildren():
        #         #text = item.text
        #         #print(text)
        #     pdf.cell(col_width, row_height, txt=row[0].text, border=1)
        #     pdf.ln(row_height * 1)
        #     pdf.cell(col_width, row_height, txt=row[1].text.encode('utf-8', errors="ignore").decode(errors="ignore"), border=1)
        #     pdf.ln(row_height * 1)
        #
        # pdf.output('simple.pdf')

        # for child in root:
        #     print(child[0].text)
        #     row = []
        #     #for item in child:
        #     #row.append(child.id.text)
        #     row.append(child[0].text)
        #     row.append(child[1].text.encode("utf-8"))
        #     row.append(child[2].text.encode("utf-8"))
        #     row.append(child[3].text.encode("utf-8"))
        #     row.append(child[4].text.encode("utf-8"))
        #     row.append(child[5].text.encode("utf-8"))
        #     row.append(child[6].text.encode("utf-8"))
        #     data.append(row)
        # pass


    def book_to_html(self, row, book1):
        id = ElementTree.SubElement(book1, "td", width="10")
        id.text = str(row[0])

        title = ElementTree.SubElement(book1, "td", width="100%")
        title.text = str(row[1])

        author = ElementTree.SubElement(book1, "td", width="100%")
        author.text = str(row[2])

        publisher = ElementTree.SubElement(book1, "td", width="100%")
        publisher.text = str(row[3])

        price = ElementTree.SubElement(book1, "td", width="100%")
        price.text = str(row[4])

        selfprice = ElementTree.SubElement(book1, "td", width="100%")
        selfprice.text = str(row[5])

        amount = ElementTree.SubElement(book1, "td", width="100%")
        amount.text = str(row[6])

    def name_to_html(self, book1):

        id = ElementTree.SubElement(book1, "th", width="10")
        id.text = "id"

        title = ElementTree.SubElement(book1, "th", width="100%")
        title.text = "title"

        author = ElementTree.SubElement(book1, "th", width="100%")
        author.text = "author"

        publisher = ElementTree.SubElement(book1, "th", width="100%")
        publisher.text = "publisher"

        price = ElementTree.SubElement(book1, "th", width="100%")
        price.text = "price"

        selfprice = ElementTree.SubElement(book1, "th", width="100%")
        selfprice.text = "selfprice"

        amount = ElementTree.SubElement(book1, "th", width="100%")
        amount.text = "amount"


    def book_to_xml(self, row, book1):

        id = ElementTree.SubElement(book1, "id")
        id.text = str(row[0])

        title = ElementTree.SubElement(book1, "title")
        title.text = str(row[1])

        author = ElementTree.SubElement(book1, "author")
        author.text = str(row[2])

        publisher = ElementTree.SubElement(book1, "publisher")
        publisher.text = str(row[3])

        price = ElementTree.SubElement(book1, "price")
        price.text = str(row[4])

        selfprice = ElementTree.SubElement(book1, "selfprice")
        selfprice.text = str(row[5])

        amount = ElementTree.SubElement(book1, "amount")
        amount.text = str(row[6])

    def write_to_xml(self):
        sql = """Select * from books"""
        self.c.execute(sql)
        root = ElementTree.Element("books")

        for row in self.c.fetchall():
            name = "book" + str(row[0])
            book1 = ElementTree.SubElement(root, name)
            self.book_to_xml(row, book1)

        tree = ElementTree.ElementTree(root)

        tree.write("xml_file.xml", "utf-8")

    def parallel(self):
        thread1 = Thread(target=self.write_to_xml())
        thread2 = Thread(target=self.write_to_csv())
        thread3 = Thread(target=self.create_html())
