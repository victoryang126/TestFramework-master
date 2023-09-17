# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SWA.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SWA(object):
    def setupUi(self, SWA):
        SWA.setObjectName("SWA")
        SWA.resize(1363, 781)
        self.gridLayout_2 = QtWidgets.QGridLayout(SWA)
        self.gridLayout_2.setContentsMargins(20, 30, 20, 50)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LE_Sql = QtWidgets.QLineEdit(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LE_Sql.setFont(font)
        self.LE_Sql.setObjectName("LE_Sql")
        self.gridLayout_2.addWidget(self.LE_Sql, 0, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(SWA)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.gridLayout_2.addWidget(self.frame_4, 6, 0, 1, 2)
        self.BT_Query = QtWidgets.QPushButton(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_Query.setFont(font)
        self.BT_Query.setObjectName("BT_Query")
        self.gridLayout_2.addWidget(self.BT_Query, 1, 3, 1, 1)
        self.BT_BackUp = QtWidgets.QPushButton(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_BackUp.setFont(font)
        self.BT_BackUp.setObjectName("BT_BackUp")
        self.gridLayout_2.addWidget(self.BT_BackUp, 1, 2, 1, 1)
        self.frame = QtWidgets.QFrame(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(5, 5, 6, 0)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox_OEM = QtWidgets.QComboBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_OEM.setFont(font)
        self.comboBox_OEM.setObjectName("comboBox_OEM")
        self.gridLayout.addWidget(self.comboBox_OEM, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 5, 1, 1)
        self.LE_PN = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_PN.setFont(font)
        self.LE_PN.setObjectName("LE_PN")
        self.gridLayout.addWidget(self.LE_PN, 1, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)
        self.LE_ShelfNumber = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_ShelfNumber.setFont(font)
        self.LE_ShelfNumber.setObjectName("LE_ShelfNumber")
        self.gridLayout.addWidget(self.LE_ShelfNumber, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.comboBox_Category = QtWidgets.QComboBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Category.setFont(font)
        self.comboBox_Category.setObjectName("comboBox_Category")
        self.gridLayout.addWidget(self.comboBox_Category, 1, 1, 1, 1)
        self.LE_Quantity = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.LE_Quantity.setFont(font)
        self.LE_Quantity.setObjectName("LE_Quantity")
        self.gridLayout.addWidget(self.LE_Quantity, 1, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 4, 1, 1)
        self.comboBox_Engineer = QtWidgets.QComboBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_Engineer.setFont(font)
        self.comboBox_Engineer.setObjectName("comboBox_Engineer")
        self.gridLayout.addWidget(self.comboBox_Engineer, 1, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 4)
        self.gridLayout.setColumnStretch(5, 2)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 4)
        self.frame_3 = QtWidgets.QFrame(SWA)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setLineWidth(1)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.label_info = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_info.setFont(font)
        self.label_info.setFrameShape(QtWidgets.QFrame.Box)
        self.label_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_info.setText("")
        self.label_info.setObjectName("label_info")
        self.horizontalLayout_2.addWidget(self.label_info)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 4)
        self.gridLayout_2.addWidget(self.frame_3, 4, 0, 1, 4)
        self.tableView_data = QtWidgets.QTableView(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableView_data.setFont(font)
        self.tableView_data.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableView_data.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView_data.setObjectName("tableView_data")
        self.gridLayout_2.addWidget(self.tableView_data, 5, 0, 1, 4)
        self.label = QtWidgets.QLabel(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.BT_SelectSql = QtWidgets.QPushButton(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_SelectSql.setFont(font)
        self.BT_SelectSql.setObjectName("BT_SelectSql")
        self.gridLayout_2.addWidget(self.BT_SelectSql, 0, 2, 1, 1)
        self.BT_Export = QtWidgets.QPushButton(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_Export.setFont(font)
        self.BT_Export.setObjectName("BT_Export")
        self.gridLayout_2.addWidget(self.BT_Export, 0, 3, 1, 1)
        self.tableView_history = QtWidgets.QTableView(SWA)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableView_history.setFont(font)
        self.tableView_history.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableView_history.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView_history.setGridStyle(QtCore.Qt.DashDotLine)
        self.tableView_history.setObjectName("tableView_history")
        self.gridLayout_2.addWidget(self.tableView_history, 7, 0, 1, 4)
        self.frame_2 = QtWidgets.QFrame(SWA)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BT_StockIn = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_StockIn.setFont(font)
        self.BT_StockIn.setObjectName("BT_StockIn")
        self.horizontalLayout.addWidget(self.BT_StockIn)
        self.BT_StockOut = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_StockOut.setFont(font)
        self.BT_StockOut.setObjectName("BT_StockOut")
        self.horizontalLayout.addWidget(self.BT_StockOut)
        self.BT_Print = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.BT_Print.setFont(font)
        self.BT_Print.setObjectName("BT_Print")
        self.horizontalLayout.addWidget(self.BT_Print)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 3)
        self.gridLayout_2.addWidget(self.frame_2, 8, 0, 1, 4)

        self.retranslateUi(SWA)
        QtCore.QMetaObject.connectSlotsByName(SWA)

    def retranslateUi(self, SWA):
        _translate = QtCore.QCoreApplication.translate
        SWA.setWindowTitle(_translate("SWA", "库存管理"))
        self.label_9.setText(_translate("SWA", "库存变更历史"))
        self.BT_Query.setText(_translate("SWA", "查询"))
        self.BT_BackUp.setText(_translate("SWA", "备份"))
        self.label_3.setText(_translate("SWA", "产品分类"))
        self.label_2.setText(_translate("SWA", "货架号"))
        self.label_7.setText(_translate("SWA", "数量"))
        self.label_5.setText(_translate("SWA", "工程师"))
        self.label_4.setText(_translate("SWA", "OEM"))
        self.label_6.setText(_translate("SWA", "内部零件号"))
        self.label_8.setText(_translate("SWA", "库存信息如下："))
        self.label.setText(_translate("SWA", "数据库"))
        self.BT_SelectSql.setText(_translate("SWA", "选择数据库"))
        self.BT_Export.setText(_translate("SWA", "导出数据库为Excel"))
        self.BT_StockIn.setText(_translate("SWA", "入库"))
        self.BT_StockOut.setText(_translate("SWA", "出库"))
        self.BT_Print.setText(_translate("SWA", "打印"))
