import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
from PyQt5.QtGui import QPainter, QPen, QFont,QTextDocument

class BarcodePrinter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Barcode Printer')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.print_button = QPushButton('Print Barcode', self)
        self.print_button.clicked.connect(self.printBarcode)
        self.layout.addWidget(self.print_button)

        self.central_widget.setLayout(self.layout)

    def generateBarcode(self, text):
        d = Drawing(50, 10)
        barcode = code128.Code128(text)
        d.add(barcode)
        return d

    def printBarcode(self):
        text = self.text_edit.toPlainText()

        if text:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec_() == QPrintDialog.Accepted:
                painter = QPainter()
                painter.begin(printer)

                barcode = self.generateBarcode(text)
                width, height = letter
                barcode_width = 2.0 * inch
                barcode_height = 0.5 * inch

                # 居中绘制条形码
                x = (width - barcode_width) / 2
                y = (height - barcode_height) / 2

                barcode.drawOn(painter, x, y)
                painter.end()
        else:
            print("Please enter barcode text.")

def main():
    app = QApplication(sys.argv)
    window = BarcodePrinter()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
