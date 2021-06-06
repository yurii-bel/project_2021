import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SignalsSlots(QMainWindow):
    def __init__(self):
        super().__init__()

        widg = QWidget()
        lay = QHBoxLayout()
        self.lbl = QLabel()
        self.lbl.setText("Lorem ipsum dolor")

        qbtn = QPushButton()
        qbtn.setText("Press me!")

        lay.addWidget(self.lbl)
        lay.addWidget(qbtn)

        widg.setLayout(lay)
        self.setCentralWidget(widg)

        qbtn.clicked.connect(self.changeText)

        self.show()

    def changeText(self):
        self.lbl.setText("Yo, it works!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SignalsSlots()
    sys.exit(app.exec())
