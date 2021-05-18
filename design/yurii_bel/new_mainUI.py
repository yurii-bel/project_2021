# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1198, 848)
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radio_family = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_family.setGeometry(QtCore.QRect(50, 330, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_family.setFont(font)
        self.radio_family.setObjectName("radio_family")
        self.radio_filter_work = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_filter_work.setGeometry(QtCore.QRect(50, 310, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_filter_work.setFont(font)
        self.radio_filter_work.setObjectName("radio_filter_work")
        self.btn_january = QtWidgets.QPushButton(self.centralwidget)
        self.btn_january.setGeometry(QtCore.QRect(50, 550, 61, 23))
        self.btn_january.setObjectName("btn_january")
        self.radio_filter_all = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_filter_all.setGeometry(QtCore.QRect(50, 270, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_filter_all.setFont(font)
        self.radio_filter_all.setObjectName("radio_filter_all")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(50, 760, 161, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.lbl_filter = QtWidgets.QLabel(self.centralwidget)
        self.lbl_filter.setGeometry(QtCore.QRect(40, 240, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_filter.setFont(font)
        self.lbl_filter.setObjectName("lbl_filter")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(40, 220, 161, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.btn_month = QtWidgets.QPushButton(self.centralwidget)
        self.btn_month.setGeometry(QtCore.QRect(50, 520, 131, 23))
        self.btn_month.setObjectName("btn_month")
        self.btn_week = QtWidgets.QPushButton(self.centralwidget)
        self.btn_week.setGeometry(QtCore.QRect(50, 490, 131, 23))
        self.btn_week.setObjectName("btn_week")
        self.radio__filter_rest = QtWidgets.QRadioButton(self.centralwidget)
        self.radio__filter_rest.setGeometry(QtCore.QRect(50, 350, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio__filter_rest.setFont(font)
        self.radio__filter_rest.setObjectName("radio__filter_rest")
        self.lbl_menu = QtWidgets.QLabel(self.centralwidget)
        self.lbl_menu.setGeometry(QtCore.QRect(80, 10, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lbl_menu.setFont(font)
        self.lbl_menu.setObjectName("lbl_menu")
        self.radio_diag_type_diagram = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_diag_type_diagram.setGeometry(QtCore.QRect(50, 180, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_diag_type_diagram.setFont(font)
        self.radio_diag_type_diagram.setObjectName("radio_diag_type_diagram")
        self.btn_september = QtWidgets.QPushButton(self.centralwidget)
        self.btn_september.setGeometry(QtCore.QRect(50, 630, 61, 23))
        self.btn_september.setObjectName("btn_september")
        self.radio_filter_entertainment = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_filter_entertainment.setGeometry(QtCore.QRect(50, 370, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_filter_entertainment.setFont(font)
        self.radio_filter_entertainment.setObjectName("radio_filter_entertainment")
        self.btn_june = QtWidgets.QPushButton(self.centralwidget)
        self.btn_june.setGeometry(QtCore.QRect(120, 590, 61, 23))
        self.btn_june.setObjectName("btn_june")
        self.btn_december = QtWidgets.QPushButton(self.centralwidget)
        self.btn_december.setGeometry(QtCore.QRect(120, 650, 61, 23))
        self.btn_december.setObjectName("btn_december")
        self.find_to = QtWidgets.QLineEdit(self.centralwidget)
        self.find_to.setGeometry(QtCore.QRect(70, 710, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.find_to.setFont(font)
        self.find_to.setObjectName("find_to")
        self.btn_may = QtWidgets.QPushButton(self.centralwidget)
        self.btn_may.setGeometry(QtCore.QRect(50, 590, 61, 23))
        self.btn_may.setObjectName("btn_may")
        self.btn_november = QtWidgets.QPushButton(self.centralwidget)
        self.btn_november.setGeometry(QtCore.QRect(50, 650, 61, 23))
        self.btn_november.setObjectName("btn_november")
        self.lbl_from = QtWidgets.QLabel(self.centralwidget)
        self.lbl_from.setGeometry(QtCore.QRect(50, 680, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_from.setFont(font)
        self.lbl_from.setObjectName("lbl_from")
        self.btn_today = QtWidgets.QPushButton(self.centralwidget)
        self.btn_today.setGeometry(QtCore.QRect(50, 460, 131, 23))
        self.btn_today.setObjectName("btn_today")
        self.btn_august = QtWidgets.QPushButton(self.centralwidget)
        self.btn_august.setGeometry(QtCore.QRect(120, 610, 61, 23))
        self.btn_august.setObjectName("btn_august")
        self.lbl_to = QtWidgets.QLabel(self.centralwidget)
        self.lbl_to.setGeometry(QtCore.QRect(50, 710, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_to.setFont(font)
        self.lbl_to.setObjectName("lbl_to")
        self.btn_march = QtWidgets.QPushButton(self.centralwidget)
        self.btn_march.setGeometry(QtCore.QRect(50, 570, 61, 23))
        self.btn_march.setObjectName("btn_march")
        self.btn_october = QtWidgets.QPushButton(self.centralwidget)
        self.btn_october.setGeometry(QtCore.QRect(120, 630, 61, 23))
        self.btn_october.setObjectName("btn_october")
        self.btn_april = QtWidgets.QPushButton(self.centralwidget)
        self.btn_april.setGeometry(QtCore.QRect(120, 570, 61, 23))
        self.btn_april.setObjectName("btn_april")
        self.radio_diag_type_table = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_diag_type_table.setGeometry(QtCore.QRect(50, 160, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_diag_type_table.setFont(font)
        self.radio_diag_type_table.setObjectName("radio_diag_type_table")
        self.btn_february = QtWidgets.QPushButton(self.centralwidget)
        self.btn_february.setGeometry(QtCore.QRect(120, 550, 61, 23))
        self.btn_february.setObjectName("btn_february")
        self.btn_july = QtWidgets.QPushButton(self.centralwidget)
        self.btn_july.setGeometry(QtCore.QRect(50, 610, 61, 23))
        self.btn_july.setObjectName("btn_july")
        self.lbl_type_diagram = QtWidgets.QLabel(self.centralwidget)
        self.lbl_type_diagram.setGeometry(QtCore.QRect(40, 130, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_type_diagram.setFont(font)
        self.lbl_type_diagram.setObjectName("lbl_type_diagram")
        self.radio_filter_health = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_filter_health.setGeometry(QtCore.QRect(50, 290, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_filter_health.setFont(font)
        self.radio_filter_health.setObjectName("radio_filter_health")
        self.radio_diag_type_graph = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_diag_type_graph.setGeometry(QtCore.QRect(50, 200, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_diag_type_graph.setFont(font)
        self.radio_diag_type_graph.setObjectName("radio_diag_type_graph")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(40, 410, 161, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(40, 110, 161, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lbl_display_data = QtWidgets.QLabel(self.centralwidget)
        self.lbl_display_data.setGeometry(QtCore.QRect(40, 430, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_display_data.setFont(font)
        self.lbl_display_data.setObjectName("lbl_display_data")
        self.lbl_example = QtWidgets.QLabel(self.centralwidget)
        self.lbl_example.setGeometry(QtCore.QRect(50, 740, 141, 16))
        self.lbl_example.setObjectName("lbl_example")
        self.btn_add_action = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_action.setGeometry(QtCore.QRect(40, 62, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_add_action.setFont(font)
        self.btn_add_action.setObjectName("btn_add_action")
        self.btn_find = QtWidgets.QPushButton(self.centralwidget)
        self.btn_find.setGeometry(QtCore.QRect(120, 680, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_find.setFont(font)
        self.btn_find.setObjectName("btn_find")
        self.find_from = QtWidgets.QLineEdit(self.centralwidget)
        self.find_from.setGeometry(QtCore.QRect(70, 680, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.find_from.setFont(font)
        self.find_from.setObjectName("find_from")
        self.radio_filter_other = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_filter_other.setGeometry(QtCore.QRect(50, 390, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radio_filter_other.setFont(font)
        self.radio_filter_other.setObjectName("radio_filter_other")
        self.widget_main = QtWidgets.QWidget(self.centralwidget)
        self.widget_main.setGeometry(QtCore.QRect(220, 70, 931, 691))
        self.widget_main.setObjectName("widget_main")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1198, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radio_family.setText(_translate("MainWindow", "Семья"))
        self.radio_filter_work.setText(_translate("MainWindow", "Работа"))
        self.btn_january.setText(_translate("MainWindow", "январь"))
        self.radio_filter_all.setText(_translate("MainWindow", "Все"))
        self.lbl_filter.setText(_translate("MainWindow", "Фильтр"))
        self.btn_month.setText(_translate("MainWindow", "за этот месяц"))
        self.btn_week.setText(_translate("MainWindow", "за эту неделю"))
        self.radio__filter_rest.setText(_translate("MainWindow", "Отдых"))
        self.lbl_menu.setText(_translate("MainWindow", "Menu"))
        self.radio_diag_type_diagram.setText(_translate("MainWindow", "Диаграмма"))
        self.btn_september.setText(_translate("MainWindow", "сентябрь"))
        self.radio_filter_entertainment.setText(_translate("MainWindow", "Развлечения"))
        self.btn_june.setText(_translate("MainWindow", "июнь"))
        self.btn_december.setText(_translate("MainWindow", "декабрь"))
        self.btn_may.setText(_translate("MainWindow", "май"))
        self.btn_november.setText(_translate("MainWindow", "ноябрь"))
        self.lbl_from.setText(_translate("MainWindow", "С"))
        self.btn_today.setText(_translate("MainWindow", "за сегодня"))
        self.btn_august.setText(_translate("MainWindow", "август"))
        self.lbl_to.setText(_translate("MainWindow", "по"))
        self.btn_march.setText(_translate("MainWindow", "март"))
        self.btn_october.setText(_translate("MainWindow", "октябрь"))
        self.btn_april.setText(_translate("MainWindow", "апрель"))
        self.radio_diag_type_table.setText(_translate("MainWindow", "Таблица"))
        self.btn_february.setText(_translate("MainWindow", "февраль"))
        self.btn_july.setText(_translate("MainWindow", "июль"))
        self.lbl_type_diagram.setText(_translate("MainWindow", "Тип диаграммы"))
        self.radio_filter_health.setText(_translate("MainWindow", "Здоровье"))
        self.radio_diag_type_graph.setText(_translate("MainWindow", "График"))
        self.lbl_display_data.setText(_translate("MainWindow", "Отобразить данные"))
        self.lbl_example.setText(_translate("MainWindow", "*Пример: С 11.05 по 15.06"))
        self.btn_add_action.setText(_translate("MainWindow", "Добавить событие"))
        self.btn_find.setText(_translate("MainWindow", "Найти"))
        self.radio_filter_other.setText(_translate("MainWindow", "Другое"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())