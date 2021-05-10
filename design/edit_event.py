# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_event.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 356)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 401, 221))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lbl_name = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_name.setFont(font)
        self.lbl_name.setObjectName("lbl_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_name)
        self.lE_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lE_name.setObjectName("lE_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lE_name)
        self.lbl_category = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_category.setFont(font)
        self.lbl_category.setObjectName("lbl_category")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_category)
        self.cB_category = QtWidgets.QComboBox(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.cB_category.setFont(font)
        self.cB_category.setEditable(True)
        self.cB_category.setObjectName("cB_category")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cB_category)
        self.lbl_time = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_time.setFont(font)
        self.lbl_time.setObjectName("lbl_time")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lbl_time)
        self.lE_duration = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lE_duration.setObjectName("lE_duration")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lE_duration)
        self.lbl_date = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_date.setFont(font)
        self.lbl_date.setObjectName("lbl_date")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lbl_date)
        self.dE_date = QtWidgets.QDateEdit(self.formLayoutWidget)
        self.dE_date.setObjectName("dE_date")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dE_date)
        self.lbl_time_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_time_2.setFont(font)
        self.lbl_time_2.setObjectName("lbl_time_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lbl_time_2)
        self.tE_time = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.tE_time.setObjectName("tE_time")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tE_time)
        self.lbl_comment = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_comment.setFont(font)
        self.lbl_comment.setObjectName("lbl_comment")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lbl_comment)
        self.tE_comment = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.tE_comment.setObjectName("tE_comment")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.tE_comment)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 240, 261, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактировать событие"))
        self.lbl_name.setText(_translate("Form", "Название события:"))
        self.lbl_category.setText(_translate("Form", "Категория:"))
        self.lbl_time.setText(_translate("Form", "Потратил времени:"))
        self.lbl_date.setText(_translate("Form", "Дата:"))
        self.lbl_time_2.setText(_translate("Form", "Время:"))
        self.lbl_comment.setText(_translate("Form", "Комментарий:"))
        self.btn_save.setText(_translate("Form", "Сохранить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
