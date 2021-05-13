import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Widget(QtWidgets.QWidget):
    
    def __init__(self, parent= None):
        super(Widget, self).__init__()

        btn_new = QtWidgets.QPushButton("Append new label")
        btn_new.clicked.connect(self.add_new_label)
        # self.connect(btn_new, SIGNAL('clicked()'), self.add_new_label)

        #Container Widget       
        self.widget = QtWidgets.QWidget()
        #Layout of Container Widget
        layout = QtWidgets.QVBoxLayout(self)
        for _ in range(10):
            label = QtWidgets.QLabel("test")
            layout.addWidget(label)
        layout.addStretch()
        self.widget.setLayout(layout)

        #Scroll Area Properties
        scroll = QtWidgets.QScrollArea()
        # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        #Scroll Area Layer add
        vLayout = QtWidgets.QVBoxLayout(self)
        vLayout.addWidget(btn_new)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)

    # def add_new_label(self):
    #     label = QLabel("new")
    #     self.widget.layout().addWidget(label)

    def add_new_label(self):
        label = QtWidgets.QLabel("new")
        layout = self.widget.layout()
        layout.insertWidget(layout.count() - 1, label)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    dialog = Widget()
    dialog.show()

    app.exec_()