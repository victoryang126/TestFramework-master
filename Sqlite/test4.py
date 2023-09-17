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
        print_button.clicked.connect(self.show_print_preview)

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

    def print_table(self, printer):
        painter = QPainter()
        painter.begin(printer)

        # 获取表格的内容
        table_content = []
        for row in range(self.table_widget.rowCount()):
            table_content.append([self.table_widget.item(row, 0).text(), self.table_widget.item(row, 1).text()])

        # 设置表格样式
        table_style = '''
            border-collapse: collapse;
            width: 100%;
        '''
        td_style = '''
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        '''

        # 开始绘制表格
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(QFont("Arial", 12))

        table_width = 500
        column_width = table_width / 2

        x, y = 50, 50
        row_height = 30

        for row_data in table_content:
            x = 50
            for item in row_data:
                painter.setPen(Qt.black)
                painter.drawRect(x, y, column_width, row_height)

                painter.setPen(Qt.black)
                painter.drawText(x + 5, y + 20, column_width - 10, row_height - 10, Qt.AlignLeft, item)

                x += column_width
            y += row_height

        painter.end()

    def show_print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)

        # 创建一个打印预览对话框
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_table)

        # 显示打印预览
        preview_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data_dict = {'Name': 'John', 'Age': 30, 'City': 'New York'}
    window = DictionaryToTable(data_dict)
    window.show()
    sys.exit(app.exec_())