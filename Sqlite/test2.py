import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3
from Inventory import InventorySystem

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 800, 600)
        self.inventory_system = InventorySystem("inventory2.db")
        # 创建主窗口部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout()

        # 创建数据显示表格
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # 创建查询 PN 输入框和按钮
        self.query_pn_label = QLabel('查询 PN:')
        self.query_pn_input = QLineEdit()
        self.query_pn_button = QPushButton('查询')
        layout.addWidget(self.query_pn_label)
        layout.addWidget(self.query_pn_input)
        layout.addWidget(self.query_pn_button)

        # 创建添加物品输入框和按钮
        self.add_pn_label = QLabel('添加 PN:')
        self.add_pn_input = QLineEdit()
        self.add_pn_button = QPushButton('添加')
        layout.addWidget(self.add_pn_label)
        layout.addWidget(self.add_pn_input)
        layout.addWidget(self.add_pn_button)

        # 创建入库输入框和按钮
        self.stock_in_pn_label = QLabel('入库 PN:')
        self.stock_in_pn_input = QLineEdit()
        self.stock_in_quantity_label = QLabel('入库数量:')
        self.stock_in_quantity_input = QLineEdit()
        self.stock_in_button = QPushButton('入库')
        layout.addWidget(self.stock_in_pn_label)
        layout.addWidget(self.stock_in_pn_input)
        layout.addWidget(self.stock_in_quantity_label)
        layout.addWidget(self.stock_in_quantity_input)
        layout.addWidget(self.stock_in_button)

        # 创建出库输入框和按钮
        self.stock_out_pn_label = QLabel('出库 PN:')
        self.stock_out_pn_input = QLineEdit()
        self.stock_out_quantity_label = QLabel('出库数量:')
        self.stock_out_quantity_input = QLineEdit()
        self.stock_out_button = QPushButton('出库')
        layout.addWidget(self.stock_out_pn_label)
        layout.addWidget(self.stock_out_pn_input)
        layout.addWidget(self.stock_out_quantity_label)
        layout.addWidget(self.stock_out_quantity_input)
        layout.addWidget(self.stock_out_button)

        # 设置布局
        central_widget.setLayout(layout)

        # 创建数据库连接
        self.conn = sqlite3.connect("inventory2.db")
        self.cursor = self.conn.cursor()

        # 创建模型
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

        # 连接按钮点击事件
        self.query_pn_button.clicked.connect(self.query_item_by_pn)
        self.add_pn_button.clicked.connect(self.add_item_if_not_exists)
        self.stock_in_button.clicked.connect(self.stock_in)
        self.stock_out_button.clicked.connect(self.stock_out)

    def query_item_by_pn(self):
        pn = self.query_pn_input.text().strip()
        item = self.inventory_system.query_item_by_pn(pn)
        if item:
            self.display_data([item])
        else:
            QMessageBox.warning(self, '警告', f"PN '{pn}' 不存在")

    def add_item_if_not_exists(self):
        pn = self.add_pn_input.text().strip()
        if not pn:
            QMessageBox.warning(self, '警告', '请输入要添加的 PN')
            return

        if self.inventory_system.query_item_by_pn(pn):
            QMessageBox.warning(self, '警告', f"物品 '{pn}' 已存在于库存中")
        else:
            shelf_number = input("请输入ShelfNumber: ")
            category = input("请输入Category: ")
            oem = input("请输入OEM: ")
            engineer = input("请输入Engineer: ")
            inbound_quantity = int(input("请输入InboundQuantity: "))
            self.inventory_system.add_item_if_not_exists(pn, shelf_number, category, oem, engineer, inbound_quantity)
            QMessageBox.information(self, '提示', f"物品 '{pn}' 已成功添加")

    def stock_in(self):
        pn = self.stock_in_pn_input.text().strip()
        quantity = int(self.stock_in_quantity_input.text().strip())
        engineer = input("请输入Engineer: ")
        self.inventory_system.stock_in(pn, quantity, engineer)
        QMessageBox.information(self, '提示', f"物品 '{pn}' 已成功入库")

    def stock_out(self):
        pn = self.stock_out_pn_input.text().strip()
        quantity = int(self.stock_out_quantity_input.text().strip())
        engineer = input("请输入Engineer: ")
        self.inventory_system.stock_out(pn, quantity, engineer)
        QMessageBox.information(self, '提示', f"物品 '{pn}' 已成功出库")

    def display_data(self, data):
        # 清空模型
        self.model.clear()

        # 设置表格头
        self.model.setHorizontalHeaderLabels(["ShelfNumber", "Category", "OEM", "PN", "Engineer", "OutboundQuantity", "OutboundDate", "InboundQuantity", "InboundDate", "BalanceQuantity"])

        # 填充数据
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QStandardItem(str(value))
                self.model.setItem(i, j, item)

    def closeEvent(self, event):
        self.conn.close()

def main():
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
