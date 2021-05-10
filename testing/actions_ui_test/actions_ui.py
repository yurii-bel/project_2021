import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTime, QDate
from PyQt5 import QtCore, QtGui, QtWidgets
import uuid
from actions import Actions


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


class ActionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # self.aUi = uic.loadUi('design\\edit_event.ui')
        self.aUi = Ui_Form()
        self.aUi.setupUi(self)
        self.user_events = {}   

        # Settings for 'dE_date' control element.
        self.aUi.dE_date.setCalendarPopup(True)
        self.aUi.dE_date.setDate(QDate(QDate.currentDate()))
        self.aUi.dE_date.setMaximumDate(QDate(QDate.currentDate()))

        # Settings for 'tE_time' control element.
        self.aUi.tE_time.setTime(QTime.currentTime())

        # Settings for cB_category control element.
        # self.aUi.cB_category.addItems()

        self.aUi.btn_save.clicked.connect(self.add_event)

        self.act = Actions

    def add_event(self):
        userId = uuid.uuid4()

        title = self.aUi.lE_name.text()
        category = self.aUi.cB_category.currentText()
        
        time = self.aUi.tE_time.time()
        hour = time.hour()
        minute = time.minute()

        date = self.aUi.dE_date.date()
        year = date.year()
        month = date.month()
        day = date.day()

        duration = self.aUi.lE_duration.text()        
        comment = self.aUi.tE_comment.toPlainText()

        a = self.act(title, category, hour, minute, year, month, day, \
            duration, comment)
        b = {userId:a.__str__()}

        self.user_events.update(b)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionUI()
    win.show()
    sys.exit(app.exec())
    