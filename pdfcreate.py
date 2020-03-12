from decimal import Decimal
from lxml import etree, objectify

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


########################################################################
class PDFOrder(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, xml_file, pdf_file):
        """Constructor"""
        self.xml_file = xml_file
        self.pdf_file = pdf_file

        self.xml_obj = self.getXMLObject()

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height - y * unit
        return x, y

        # ----------------------------------------------------------------------

    def createPDF(self):
        """
        Create a PDF based on the XML data
        """
        self.canvas = canvas.Canvas(self.pdf_file, pagesize=letter)
        width, self.height = letter
        styles = getSampleStyleSheet()
        xml = self.xml_obj
        tree = etree.parse("xml_file.xml")
        root = tree.getroot()

        address = """ <font size="9">
        SHIP TO:<br/>
        <br/>
        %s<br/>
        %s<br/>
        %s<br/>
        %s<br/>
        </font>
        """

        # order_number = '<font size="14"><b>Order #%s </b></font>' % xml.book266
        # p = Paragraph(order_number, styles["Normal"])
        # p.wrapOn(self.canvas, width, self.height)
        # p.drawOn(self.canvas, *self.coord(18, 50, mm))

        data = []
        data.append(["Item ID", "Name", "Price", "Quantity", "Total", 'f', 'g'])
        grand_total = 0
        for child in root:
            print(child[0].text)
            row = []
            #for item in child:
            #row.append(child.id.text)
            row.append(child[0].text)
            row.append(child[1].text.encode("utf-8"))
            row.append(child[2].text.encode("utf-8"))
            row.append(child[3].text.encode("utf-8"))
            row.append(child[4].text.encode("utf-8"))
            row.append(child[5].text.encode("utf-8"))
            row.append(child[6].text.encode("utf-8"))
            data.append(row)

        t = Table(data, 1.5 * inch)
        t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        t.wrapOn(self.canvas, width, self.height)
        t.drawOn(self.canvas, *self.coord(18, 85, mm))

        txt = "Thank you for your business!"
        p = Paragraph(txt, styles["Normal"])
        p.wrapOn(self.canvas, width, self.height)
        p.drawOn(self.canvas, *self.coord(18, 95, mm))

    # ----------------------------------------------------------------------
    def getXMLObject(self):
        """
        Open the XML document and return an lxml XML document
        """
        with open(self.xml_file, encoding='utf-8') as f:
            xml = f.read()
        return objectify.fromstring(xml)

    # ----------------------------------------------------------------------
    def savePDF(self):
        """
        Save the PDF to disk
        """
        self.canvas.save()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    xml = r"xml_file.xml"
    pdf = r"letter.pdf"
    doc = PDFOrder(xml, pdf)
    doc.createPDF()
    doc.savePDF()