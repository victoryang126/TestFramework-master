import shutil
import sqlite3
import datetime
import pandas as pd
import win32print
import win32ui
from tabulate import tabulate


class InventorySystem:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                                ShelfNumber TEXT,
                                Category TEXT,
                                OEM TEXT,
                                PN TEXT PRIMARY KEY,
                                Engineer TEXT,
                                StockOutQuantity INTEGER,
                                StockOutDate DATE,
                                StockInQuantity INTEGER,
                                StockInDate DATE,
                                BalanceQuantity INTEGER
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                ChangeType TEXT,
                                PN TEXT,
                                Engineer TEXT,
                                Quantity INTEGER,
                                Date DATE,
                                FOREIGN KEY (PN) REFERENCES inventory (PN)
                            )''')
        self.conn.commit()


    def record_history(self, change_type, pn,engineer,quantity, date,):
        """
        once there any change, shall record the history
        :param change_type:
        :param pn:
        :param engineer:
        :param quantity:
        :param date:
        :return:
        """
        self.cursor.execute("INSERT INTO history (ChangeType, PN,Engineer, Quantity, Date) VALUES (?, ?, ?, ?,?)",
                            (change_type, pn, engineer, quantity, date))
        self.conn.commit()

    def view_history_by_pn(self, pn):
        """

        :param pn:
        :return:
        :  list of data like below[('New', 'PN123ABCDEEDE', 'VictorYang', 50, '2023-09-16'), ('stock_in', 'PN123ABCDEEDE', 'Victor', 100, '2023-09-16')]
           or None
        """
        # 查询特定PN的历史记录
        self.cursor.execute("SELECT * FROM history WHERE PN=?", (pn,))
        history_data = self.cursor.fetchall()

        if history_data:
            # print(history_data)
            # print(f"PN '{pn}' 的变更历史：")
            # for record in history_data:
            #     change_type, pn,engineer, quantity, date = record
            #     print(f"日期: {date}, 类型: {change_type}, 数量: {quantity}")
            return history_data
        else:
            print(f"PN '{pn}' 没有相关的变更历史记录")
            return None

    def close(self):
        self.conn.close()

    def query_item_by_pn(self, pn):
        self.cursor.execute("SELECT * FROM inventory WHERE PN=?", (pn,))
        item = self.cursor.fetchone()
        if item:
            return item
        else:
            return None

    def add_item_if_not_exists(self,shelf_number,category,oem, pn, engineer, inbound_quantity):
        # 检查数据库中是否已存在具有相同PN的记录
        self.cursor.execute("SELECT PN FROM inventory WHERE PN=?", (pn,))
        existing_item = self.cursor.fetchone()

        if existing_item:
            print(f"物品 '{pn}' 已存在于库存中")
        else:
            current_date = datetime.date.today()
            # 插入新记录
            self.cursor.execute("INSERT INTO inventory (ShelfNumber, Category, OEM, PN, Engineer, StockInQuantity, StockInDate, BalanceQuantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (shelf_number, category, oem, pn, engineer, inbound_quantity, current_date, inbound_quantity))
            self.conn.commit()

            self.record_history("初次入库",pn,engineer,inbound_quantity,current_date)


    def stock_in(self, pn,engineer, quantity):
        current_date = datetime.date.today()
        self.cursor.execute("SELECT StockInQuantity, BalanceQuantity FROM inventory WHERE PN=?", (pn,))
        result = self.cursor.fetchone()
        # print()
        if result:
            inbound_quantity = quantity
            balance_quantity = result[1] + quantity
            self.cursor.execute("UPDATE inventory SET Engineer=?,StockInQuantity=?, StockInDate=?, BalanceQuantity=? WHERE PN=?",
                                (engineer,inbound_quantity, current_date, balance_quantity, pn))
            self.conn.commit()
            self.record_history("入库",pn,engineer,quantity,current_date)
        else:
            print("物品不存在")

    def stock_out(self, pn,engineer,quantity):
        current_date = datetime.date.today()
        self.cursor.execute("SELECT StockOutQuantity, BalanceQuantity FROM inventory WHERE PN=?", (pn,))
        result = self.cursor.fetchone()
        if result:
            outbound_quantity =  quantity
            balance_quantity = result[1] - quantity
            self.cursor.execute("UPDATE inventory SET Engineer=?,StockOutQuantity=?, StockOutDate=?, BalanceQuantity=? WHERE PN=?",
                                (engineer,outbound_quantity, current_date, balance_quantity, pn))
            self.conn.commit()
            self.record_history("出库",pn,engineer,quantity,current_date)
        else:
            print("物品不存在")


    # def export_to_excel(self, file_name):
        # self.cursor.execute("SELECT ShelfNumber, Category, OEM, PN,Engineer,"
        #                     "StockOutQuantity,StockOutDate,StockInQuantity,StockInDate,BalanceQuantity FROM inventory")
        # items = self.cursor.fetchall()
        # if items:
        #     df = pd.DataFrame(items, columns=["ShelfNumber", "Category", "OEM", "PN","Engineer",
        #                                       "StockOutQuantity","StockOutDate","StockInQuantity", "StockInDate","BalanceQuantity"])
        #     df.to_excel(file_name, index=False)
        #     print(f"已将库存数据导出到 '{file_name}'")
        # else:
        #     print("库存为空")
    def export_to_excel(self, file_name):
        # 导出 "inventory" 表格
        self.cursor.execute("SELECT * FROM inventory")
        inventory_data = self.cursor.fetchall()
        inventory_df = pd.DataFrame(inventory_data, columns=["ShelfNumber", "Category", "OEM", "PN", "Engineer", "StockOutQuantity", "StockOutDate", "StockInQuantity", "StockInDate", "BalanceQuantity"])

        # 导出 "history" 表格
        self.cursor.execute("SELECT * FROM history")
        history_data = self.cursor.fetchall()
        history_df = pd.DataFrame(history_data, columns=["ChangeType", "PN","Engineer","Quantity", "Date"])
        # print(history_df)

        # 将两个表格写入同一个Excel文件的不同工作表
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            inventory_df.to_excel(writer, sheet_name='Inventory', index=False)
            history_df.to_excel(writer, sheet_name='History', index=False)

        print(f"已将库存数据和变更历史导出到 '{file_name}'")

    def print_item_table(self, item):
        # item = self.query_item_by_pn(pn)
        if item:
            columns_to_print = [0, 1, 2, 3,9]
            # columns_to_print = ["ShelfNumber", "Category", "OEM", "PN", "BalanceQuantity"]
            table_data = [["ShelfNumber", "Category", "OEM", "PN", "BalanceQuantity"]]
            table_data.append([ item[column] for column in columns_to_print])
            table = tabulate(table_data,headers="firstrow",tablefmt="fancy_grid",numalign="left")
            print(table)
            return table
        else:

            return None




    def save_as_database(self, new_db_name):
        self.conn.close()
        shutil.copy("inventory.db", new_db_name)
        print(f"数据库已另存为 '{new_db_name}'")
        self.conn = sqlite3.connect(new_db_name)
        self.cursor = self.conn.cursor()

    def import_from_excel(self, excel_file):
        try:
            df = pd.read_excel(excel_file)
            df.to_sql('imported_data', self.conn, if_exists='replace', index=False)

            self.cursor.execute('INSERT OR IGNORE INTO inventory SELECT * FROM imported_data')
            self.conn.commit()
            print("数据已成功导入到数据库")
        except Exception as e:
            print(f"导入数据时发生错误: {str(e)}")
# 示例用法
if __name__ == '__main__':

    inventory_system = InventorySystem("inventory2.db")
    inventory_system.add_item_if_not_exists("PN123ABCDEEDE", "001", "RSU", "SAIC", "VictorYang", 50)
    inventory_system.add_item_if_not_exists("PN123ABCDEEDe4", "002", "RSU", "SAIC", "VictorYang", 50)
    inventory_system.print_item_table("PN123ABCDEED")
    inventory_system.stock_in("PN123ABCDEEDE", 100,"Victor")
    inventory_system.view_history_by_pn("PN123ABCDEEDE")
    # inventory_system.stock_in("PN123ABCDEED", 100,"Victor")
    # inventory_system.stock_out("PN123ABCDEED",200,"Ziki")
    inventory_system.export_to_excel("test2.xlsx")

    inventory_system.close()


