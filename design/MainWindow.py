# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 800)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1381, 841))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.btn_chart_type = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_chart_type.setFont(font)
        self.btn_chart_type.setObjectName("btn_chart_type")
        self.verticalLayout.addWidget(self.btn_chart_type)
        
        self.btn_background = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_background.setFont(font)
        self.btn_background.setObjectName("btn_background")
        self.verticalLayout.addWidget(self.btn_background)
        
        self.btn_settings = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_settings.setFont(font)
        self.btn_settings.setObjectName("btn_settings")
        self.verticalLayout.addWidget(self.btn_settings)
        
        self.btn_exit = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_exit.setFont(font)
        self.btn_exit.setObjectName("btn_exit")
        self.verticalLayout.addWidget(self.btn_exit)
        
        spacerItem = QtWidgets.QSpacerItem(20, 500, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 5, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        
        self.le_Input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_Input.setObjectName("le_Input")
        self.horizontalLayout_7.addWidget(self.le_Input)
        
        self.btn_enter = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_enter.setObjectName("btn_enter")
        self.horizontalLayout_7.addWidget(self.btn_enter)
        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 3, 1, 1)
        
        self.textLbl_TitleSoft = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.textLbl_TitleSoft.setFont(font)
        self.textLbl_TitleSoft.setObjectName("textLbl_TitleSoft")
        self.gridLayout.addWidget(self.textLbl_TitleSoft, 1, 0, 1, 1)
        
        self.lbl_Diagram = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lbl_Diagram.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_Diagram.sizePolicy().hasHeightForWidth())
        self.lbl_Diagram.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_Diagram.setFont(font)
        self.lbl_Diagram.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_Diagram.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_Diagram.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_Diagram.setObjectName("lbl_Diagram")
        self.gridLayout.addWidget(self.lbl_Diagram, 5, 3, 1, 1)
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.textLbl_comparison = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textLbl_comparison.setFont(font)
        self.textLbl_comparison.setObjectName("textLbl_comparison")
        self.verticalLayout_2.addWidget(self.textLbl_comparison)
        
        self.textLbl_filter = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textLbl_filter.setFont(font)
        self.textLbl_filter.setObjectName("textLbl_filter")
        self.verticalLayout_2.addWidget(self.textLbl_filter)
        
        self.checkBox_see_all = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_see_all.setFont(font)
        self.checkBox_see_all.setObjectName("checkBox_see_all")
        self.verticalLayout_2.addWidget(self.checkBox_see_all)
        
        self.checkBox_health = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_health.setFont(font)
        self.checkBox_health.setObjectName("checkBox_health")
        self.verticalLayout_2.addWidget(self.checkBox_health)
        
        self.checkBox_work = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_work.setFont(font)
        self.checkBox_work.setObjectName("checkBox_work")
        self.verticalLayout_2.addWidget(self.checkBox_work)
        
        self.checkBox_family = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_family.setFont(font)
        self.checkBox_family.setObjectName("checkBox_family")
        self.verticalLayout_2.addWidget(self.checkBox_family)
        
        self.checkBox_relaxation = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_relaxation.setFont(font)
        self.checkBox_relaxation.setObjectName("checkBox_relaxation")
        self.verticalLayout_2.addWidget(self.checkBox_relaxation)
        
        self.checkBox_entertainment = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBox_entertainment.setFont(font)
        self.checkBox_entertainment.setObjectName("checkBox_entertainment")
        self.verticalLayout_2.addWidget(self.checkBox_entertainment)
        
        self.checkBoxlbl_dinamic = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkBoxlbl_dinamic.setFont(font)
        self.checkBoxlbl_dinamic.setObjectName("checkBoxlbl_dinamic")
        self.verticalLayout_2.addWidget(self.checkBoxlbl_dinamic)
        spacerItem1 = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout_2, 5, 1, 1, 1)
        
        self.textLbl_Menu = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.textLbl_Menu.setFont(font)
        self.textLbl_Menu.setObjectName("textLbl_Menu")
        self.gridLayout.addWidget(self.textLbl_Menu, 2, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        
        self.btn_daily = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_daily.setFont(font)
        self.btn_daily.setObjectName("btn_daily")
        self.horizontalLayout_9.addWidget(self.btn_daily)
        
        self.btn_monthly = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_monthly.setFont(font)
        self.btn_monthly.setObjectName("btn_monthly")
        self.horizontalLayout_9.addWidget(self.btn_monthly)
        
        self.btn_annually = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_annually.setFont(font)
        self.btn_annually.setObjectName("btn_annually")
        self.horizontalLayout_9.addWidget(self.btn_annually)
        
        self.lbl_user_icon = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_user_icon.setFont(font)
        self.lbl_user_icon.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_user_icon.setObjectName("lbl_user_icon")
        self.horizontalLayout_9.addWidget(self.lbl_user_icon)
        self.lbl_date = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_date.setFont(font)
        self.lbl_date.setObjectName("lbl_date")
        self.horizontalLayout_9.addWidget(self.lbl_date)
        self.gridLayout.addLayout(self.horizontalLayout_9, 2, 3, 1, 1)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.title_diagram = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.title_diagram.setFont(font)
        self.title_diagram.setObjectName("title_diagram")
        self.horizontalLayout.addWidget(self.title_diagram)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        
        self.btn_add_event = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_add_event.setObjectName("btn_add_event")
        self.gridLayout.addWidget(self.btn_add_event, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 18))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_chart_type.setText(_translate("MainWindow", "Тип диаграммы"))
        self.btn_background.setText(_translate("MainWindow", "Тема"))
        self.btn_settings.setText(_translate("MainWindow", "Настройки"))
        self.btn_exit.setText(_translate("MainWindow", "Выход"))
        self.btn_enter.setText(_translate("MainWindow", "Enter"))
        self.textLbl_TitleSoft.setText(_translate("MainWindow", "TimeSoft"))
        self.lbl_Diagram.setText(_translate("MainWindow", "Diagram"))
        self.textLbl_comparison.setText(_translate("MainWindow", "Сравнения по каждому дню"))
        self.textLbl_filter.setText(_translate("MainWindow", "ФИЛЬТР"))
        self.checkBox_see_all.setText(_translate("MainWindow", "Посмотреть все"))
        self.checkBox_health.setText(_translate("MainWindow", "Здоровье"))
        self.checkBox_work.setText(_translate("MainWindow", "Работа"))
        self.checkBox_family.setText(_translate("MainWindow", "Семья"))
        self.checkBox_relaxation.setText(_translate("MainWindow", "Отдых"))
        self.checkBox_entertainment.setText(_translate("MainWindow", "Развлечение"))
        self.checkBoxlbl_dinamic.setText(_translate("MainWindow", "Динамический лейбл"))
        self.textLbl_Menu.setText(_translate("MainWindow", "Меню"))
        self.btn_daily.setText(_translate("MainWindow", "Ежедневно"))
        self.btn_monthly.setText(_translate("MainWindow", "Ежемесячно"))
        self.btn_annually.setText(_translate("MainWindow", "Ежегодно"))
        self.lbl_user_icon.setText(_translate("MainWindow", "Иконка"))
        self.lbl_date.setText(_translate("MainWindow", "Дата"))
        self.title_diagram.setText(_translate("MainWindow", "График сравнений по категориям"))
        self.btn_add_event.setText(_translate("MainWindow", "Добавить событие..."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
