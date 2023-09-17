import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPen, QFont,QTextDocument
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog

class DictionaryToTable(QMainWindow):
    def __init__(self, data_dict):
        super().__init__()

        self.setWindowTitle('Dictionary to Table and Print Preview')
        self.setGeometry(100, 100, 600, 400)

        self.data_dict = data_dict

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(50, 50, 500, 200)

        # 创建打印按钮
        print_button = QPushButton('打印', self)
        print_button.setGeometry(50, 270, 100, 30)
        print_button.clicked.connect(self.print_preview)

        # 将字典数据填充到表格中
        self.fill_table()

    def fill_table(self):
        headers = list(self.data_dict.keys())
        data = list(self.data_dict.values())

        self.table_widget.setRowCount(len(headers))
        self.table_widget.setColumnCount(2)

        for row, header in enumerate(headers):
            self.table_widget.setItem(row, 0, QTableWidgetItem(header))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(data[row])))

    def print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)

        # 创建一个文档对象
        doc = QTextDocument()

        # 添加表格内容到文档中
        doc.setHtml(self.table_to_html(self.table_widget))

        # 设置文档为打印机
        printer.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(printer)

    def table_to_html(self, table_widget):
        html = "<html><body><table border='1' cellspacing='0' cellpadding='2'>"

        for row in range(table_widget.rowCount()):
            html += "<tr>"
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                if item:
                    html += f"<td>{item.text()}</td>"
                else:
                    html += "<td></td>"
            html += "</tr>"

        html += "</table></body></html>"
        return html

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_dict = {'Name': 'John', 'Age': 30, 'City': 'New York'}
    window = DictionaryToTable(data_dict)
    window.show()
    sys.exit(app.exec_())