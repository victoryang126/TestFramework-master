from Sqlite.Ui_SWA import Ui_SWA
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QtCore import  *
import os,sys
from Sqlite.Inventory import *
import configparser
import traceback
from PyQt5.QtPrintSupport import QPrintDialog,QPrinter,QPageSetupDialog,QPrintPreviewDialog


def bind(objectName,propertyName):
    """
    数据绑定函数，例如，将Line_edit的text属性和对象属性绑定起来，任何一个变化，都能传递过去
    Args:
        objectName: ui object的对象名称
        propertyName: ui object 的对象属性
    Returns:
    """
    def getter(self):
        return self.findChild(QObject,objectName).property(propertyName)
    def setter(self,value):
        return self.findChild(QObject, objectName).setProperty(propertyName,value)
    return property(getter,setter)

class SWA_Widget(QWidget):
    current_path = os.getcwd()
    sql_file = bind("LE_Sql", "text")
    shelf_number = bind("LE_ShelfNumber","text")
    pn = bind("LE_PN", "text")
    quantity = bind("LE_Quantity", "text")
    category = bind("comboBox_Category", "currentText")
    oem = bind("comboBox_OEM", "currentText")
    engineer = bind("comboBox_Engineer", "currentText")
    info = bind("label_info","text")

    def __init__(self):
        super().__init__()  # 调用父类构造函数，创建QWidget窗口
        self.__ui = Ui_SWA()  # 创建UI对象
        self.__ui.setupUi(self)  # 构造UI界面
        self.table = None
        self.data_base_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Database", "")
        self.sql_file = os.path.join(self.data_base_folder,"Inventory.db") #默认使用改数据库

        self.ini =  os.path.join(os.path.dirname(os.path.realpath(__file__)),"Config","Config.ini")
        self.inventory_system = InventorySystem(self.sql_file)
        self.data_model = QStandardItemModel()
        self.history_model = QStandardItemModel()
        self.__ui.tableView_data.setModel(self.data_model)
        self.__ui.tableView_history.setModel(self.history_model)
        self.data = None
        self.history = None

        #validator
        validator = QIntValidator()
        self.__ui.LE_Quantity.setValidator(validator)

        #
        if os.path.exists(self.ini):
            self.load_config()
        else:
            self.warning(f"必须确认配置文件： {self.ini } 的存在")

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.ini)

        if "Engineer" in config:
            engineer_options = config["Engineer"]
            print(engineer_options)
            for engineer in engineer_options.values():

                self.__ui.comboBox_Engineer.addItem(engineer)

        if "OEM" in config:
            oem_options = config["OEM"]
            for oem in oem_options.values():
                self.__ui.comboBox_OEM.addItem(oem)
        if "Category" in config:
            category_options = config["Category"]
            for category in category_options.values():
                self.__ui.comboBox_Category.addItem(category)

    def save_config(self):
        pass

    @pyqtSlot()
    def on_BT_SelectSql_clicked(self):
        self.__ui.LE_Sql.clear()

        file, filetype = QFileDialog.getOpenFileName(self,
                                                     "Please the DB file ",
                                                     self.data_base_folder,
                                                     "db(*.db)")  # 起始路径
        self.sql_file = file

    def validate_input_data(self):
        if self.shelf_number and self.category and self.oem and self.pn and self.quantity:
            pass
        else:
            self.warning("请检查是否有数据没有填写")

    def warning(self, Err):
        title = "Warning Message"
        QMessageBox.warning(self, title, str(Err))

    def done(self, str):
        title = "Information Message"
        QMessageBox.information(self, title, str)


    # def print_item_to_printer(self, table):
    #
    #     printer_diqlog = QPrintDialog()
    #
    #     if printer_diqlog.exec_():
    #         printer_name = printer_diqlog.printer().printerName()
    #         printer_handle = win32print.OpenPrinter(printer_name)
    #         printer_info = win32print.GetPrinter(printer_handle, 2)
    #         printer_dc = win32ui.CreateDC()
    #         printer_dc.CreatePrinterDC(printer_name)
    #
    #         printer_dc.StartDoc('Inventory')
    #         printer_dc.StartPage()
    #         printer_dc.TextOut(100, 100, table)
    #         printer_dc.EndPage()
    #         printer_dc.EndDoc()
    def print_item_to_printer(self, table_content):
        printer_dialog = QPrintDialog()

        if printer_dialog.exec_() == QPrintDialog.Accepted:
            printer = printer_dialog.printer()
            document = QTextDocument()
            cursor = QTextCursor(document)
            cursor.setCharFormat(QTextCharFormat())

            # 创建文档中的表格
            table = QTextTable(document)
            table_format = table.format()
            table_format.setHeaderRowCount(1)  # 如果需要标题行，请设置为1

            for row, row_data in enumerate(table_content):
                for col, cell_data in enumerate(row_data):
                    cell = table.cellAt(row, col)
                    cell_cursor = cell.firstCursorPosition()
                    cell_cursor.insertText(str(cell_data))

            # 调整表格样式和布局
            table_format.setAlignment(Qt.AlignLeft)
            table_format.setBorderStyle(QTextFrameFormat.BorderStyle_Solid)
            table_format.setWidth(QTextLength(QTextLength.PercentageLength, 100))  # 表格宽度自适应

            # 将表格添加到文档中
            cursor.movePosition(QTextCursor.End)
            cursor.insertTable(table)

            # 打印文档
            printer.setDocName('Inventory')
            printer.setResolution(300)  # 设置打印分辨率
            document.print_(printer)
    # def print_item_to_printer(self, table):
    #     printer = QPrinter(QPrinter.HighResolution)
    #     printer.setOutputFormat(QPrinter.PdfFormat)
    #     printer.setOutputFileName('output.pdf')  # 指定输出的 PDF 文件名
    #
    #     dialog = QPrintDialog(printer, self)
    #     if dialog.exec_() == QPrintDialog.Accepted:
    #         painter = QPainter()
    #         painter.begin(printer)
    #
    #         # 设置绘制的位置和样式
    #         x, y = 100, 100
    #         column_width = 100
    #         row_height = 30
    #         font = QFont("Arial", 12)
    #
    #         # 开始绘制表格
    #         painter.setFont(font)
    #         for row_data in table:
    #             x = 100
    #             for item in row_data:
    #                 painter.drawRect(x, y, column_width, row_height)
    #                 painter.drawText(x + 5, y + 20, column_width - 10, row_height - 10, Qt.AlignLeft, str(item))
    #                 x += column_width
    #             y += row_height
    #
    #         painter.end()
    # def print_item_to_printer(self, table):
    #     printer = QPrinter(QPrinter.HighResolution)
    #
    #     # 创建打印预览对话框
    #     preview_dialog = QPrintPreviewDialog(printer, self)
    #     preview_dialog.setWindowTitle('Print Preview')
    #
    #     # 连接打印预览对话框的信号
    #     preview_dialog.paintRequested.connect(self.print_preview)
    #
    #     # 显示打印预览对话框
    #     if preview_dialog.exec_() == QPrintPreviewDialog.Accepted:
    #         self.print(table, printer)

    def print_preview(self, printer):
        # 使用 QPainter 绘制打印内容
        painter = QPainter(printer)
        table_content = self.table  # 获取表格内容

        # 设置绘制的位置和样式
        x, y = 100, 100
        column_width = 100
        row_height = 30
        font = QFont("Arial", 12)

        # 开始绘制表格
        painter.setFont(font)
        for row_data in table_content:
            x = 100
            for item in row_data:
                painter.drawRect(x, y, column_width, row_height)
                painter.drawText(x + 5, y + 20, column_width - 10, row_height - 10, Qt.AlignLeft, str(item))
                x += column_width
            y += row_height

        painter.end()
        # print(painter)

    def print(self, table, printer):
        # 创建 QPainter 对象并连接到打印机
        painter = QPainter()
        painter.begin(printer)

        # 使用 QPainter 绘制打印内容
        self.print_preview(printer)

        # 结束绘制
        painter.end()

    def display_data(self, item):
        # 清空模型
        data  = [item]
        self.data_model.clear()
        # 设置表格头
        self.data_model.setHorizontalHeaderLabels(["ShelfNumber", "Category", "OEM", "PN", "Engineer", "OutboundQuantity", "OutboundDate", "InboundQuantity", "InboundDate", "BalanceQuantity"])
        # 填充数据
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                viewitem = QStandardItem(str(value))
                self.data_model.setItem(i, j, viewitem)

        self.__ui.tableView_data.resizeColumnsToContents()

    def display_history(self, item):
        # 清空模型
        item.reverse()
        data = item
        self.history_model.clear()
        # 设置表格头
        self.history_model.setHorizontalHeaderLabels(["ChangeType", "PN", "Engineer", "Quantity", "Date"])
        # 填充数据
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                viewitem = QStandardItem(str(value))
                self.history_model.setItem(i, j, viewitem)
        self.__ui.tableView_history.resizeColumnsToContents()
    @pyqtSlot()
    def on_BT_Export_clicked(self):
        file = os.path.join(self.data_base_folder,"Inventory.xlsx")
        self.inventory_system.export_to_excel(file)

    @pyqtSlot()
    def on_BT_BackUp_clicked(self):
        try:
            filename,file_extension =  os.path.splitext(self.sql_file)
            today_date = datetime.date.today().strftime('%Y_%m_%d')
            newfile = f"{filename}_{today_date}{file_extension}"
            self.inventory_system.save_as_database(self.sql_file,newfile)
        except Exception as err:
            self.warning(f"异常{err}")
            print(traceback.format_exc())

    def query_pn(self):
        if self.pn:
            self.data = self.inventory_system.query_item_by_pn(self.pn)
            if self.data == None:
                self.info = f"当前库存无此料号：{self.pn}, 如需入库，请确认货架号"
                self.table = None
                self.data_model.clear()
            else:
                self.info = "请检查并确认当前库存和库存更新历史记录"
                self.table = self.inventory_system.print_item_table(self.data)  # 获取库存信息
                self.display_data(self.data)  # 显示库存信息
            self.history = self.inventory_system.view_history_by_pn(self.pn)  # 查询历史记录
            if self.history != None:  # 如果有历史记录，则显示
                self.display_history(self.history)
            else:
                self.history_model.clear()
        else:
            self.warning("内部零件号不能为空")
            self.table = None
            self.data_model.clear()
            self.history_model.clear()

    @pyqtSlot()
    def on_BT_Query_clicked(self):
        try:
            self.query_pn()
            # if self.pn:
            #     self.data = self.inventory_system.query_item_by_pn(self.pn)
            #     if self.data == None:
            #         self.info = f"当前库存无此料号：{self.pn}, 如需入库，请确认货架号"
            #     else:
            #         self.info = "请检查并确认当前库存和库存更新历史记录"
            #         self.table = self.inventory_system.print_item_table(self.data) #获取库存信息
            #         self.display_data(self.data) #显示库存信息
            #     self.history = self.inventory_system.view_history_by_pn(self.pn) #查询历史记录
            #     if self.history != None: #如果有历史记录，则显示
            #         self.display_history(self.history)
            # else:
            #     self.warning("内部零件号不能为空")
        except Exception as err:
            self.warning(f"异常{err}")
            print(traceback.format_exc())

    @pyqtSlot()
    def on_BT_StockIn_clicked(self):
        try:
            if self.pn:
                self.validate_input_data()
                if self.data:
                    self.inventory_system.stock_in(self.pn,self.engineer,int(self.quantity))
                else:
                    self.inventory_system.add_item_if_not_exists(self.shelf_number,self.category,self.oem,self.pn,self.engineer,int(self.quantity))
                self.query_pn()
            else:
                self.warning("内部零件号不能为空")
        except Exception as err:
            self.warning(f"异常{err}")
            print(traceback.format_exc())

    @pyqtSlot()
    def on_BT_StockOut_clicked(self):
        try:
            if self.pn:
                self.validate_input_data()
                self.inventory_system.stock_out(self.pn,self.engineer,int(self.quantity))
                self.query_pn()
            else:
                self.warning("内部零件号不能为空")
        except Exception as err:
            self.warning(f"异常{err}")
            print(traceback.format_exc())
    @pyqtSlot()
    def on_BT_Print_clicked(self):
        try:
            if self.table != None:
                self.print_item_to_printer(self.table)
            else:
                self.warning("没有任何需要打印的")
        except Exception as err:
            self.warning(f"异常{err}")
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    baseWidget = SWA_Widget()

    baseWidget.show()
    sys.exit(app.exec_())