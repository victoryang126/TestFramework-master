import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
import sqlite3

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Inventory Management')
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout()

        # 创建 QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # 7 列
        self.table_widget.setHorizontalHeaderLabels(["ShelfNumber", "Category", "OEM", "PN", "Engineer", "Quantity", ""])
        layout.addWidget(self.table_widget)

        # 创建输入框和按钮
        input_layout = QVBoxLayout()

        self.shelf_number_input = QLineEdit()
        self.shelf_number_input.setPlaceholderText('ShelfNumber')
        input_layout.addWidget(self.shelf_number_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Category')
        input_layout.addWidget(self.category_input)

        self.oem_input = QLineEdit()
        self.oem_input.setPlaceholderText('OEM')
        input_layout.addWidget(self.oem_input)

        self.pn_input = QLineEdit()
        self.pn_input.setPlaceholderText('PN')
        input_layout.addWidget(self.pn_input)

        self.engineer_input = QLineEdit()
        self.engineer_input.setPlaceholderText('Engineer')
        input_layout.addWidget(self.engineer_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Quantity')
        input_layout.addWidget(self.quantity_input)

        self.add_button = QPushButton('添加')
        self.add_button.clicked.connect(self.add_item)
        input_layout.addWidget(self.add_button)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        layout.addWidget(input_widget)

        central_widget.setLayout(layout)

        # 创建数据库连接
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()

    def add_item(self):
        shelf_number = self.shelf_number_input.text().strip()
        category = self.category_input.text().strip()
        oem = self.oem_input.text().strip()
        pn = self.pn_input.text().strip()
        engineer = self.engineer_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not shelf_number or not category or not oem or not pn or not engineer or not quantity:
            return

        # 添加数据到表格
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(shelf_number))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(category))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(oem))
        self.table_widget.setItem(row_position, 3, QTableWidgetItem(pn))
        self.table_widget.setItem(row_position, 4, QTableWidgetItem(engineer))
        self.table_widget.setItem(row_position, 5, QTableWidgetItem(quantity))

        # 调用添加到数据库的函数
        self.add_item_if_not_exists(pn, shelf_number, category, oem, engineer, quantity)

    def add_item_if_not_exists(self, pn, shelf_number, category, oem, engineer, quantity):
        # 检查数据库中是否已存在具有相同PN的记录
        self.cursor.execute("SELECT PN FROM inventory WHERE PN=?", (pn,))
        existing_item = self.cursor.fetchone()

        if existing_item:
            print(f"物品 '{pn}' 已存在于库存中")
        else:
            current_date = datetime.date.today()
            # 插入新记录
            self.cursor.execute("INSERT INTO inventory (ShelfNumber, Category, OEM, PN, Engineer, InboundQuantity, InboundDate, BalanceQuantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (shelf_number, category, oem, pn, engineer, quantity, current_date, quantity))
            self.conn.commit()

            self.record_history("New",pn,engineer,quantity,current_date)

    def record_history(self, change_type, pn, engineer, quantity, date):
        """
        记录历史记录
        """
        self.cursor.execute("INSERT INTO history (ChangeType, PN, Engineer, Quantity, Date) VALUES (?, ?, ?, ?, ?)",
                            (change_type, pn, engineer, quantity, date))
        self.conn.commit()

    def closeEvent(self, event):
        self.conn.close()

def main():
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
