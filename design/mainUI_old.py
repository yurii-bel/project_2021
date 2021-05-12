import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.window()
        

    def init_ui(self):
        # set the title
        self.setWindowTitle("Geometry")
  
        # setting  the geometry of window
        # setGeometry(left, top, width, height)
        self.setGeometry(0, 0, 1024, 768)
        self.center()
        self.setWindowTitle('TimeSoft')
        self.show()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def window(self):
        # self.win = QWidget()
        self.grid = QGridLayout()
	
        # for i in range(0,5):
        #     for j in range(0,5):
        #         self.grid.addWidget(QPushButton(str(i)+str(j)),i,j)
        self.lbl_action = QtWidgets.QLabel()
        self.lbl_action.setText('Run Health 10 min dassadasdasdsadsadasda 01.01.2021 Some shit')
        self.lbl_action.resize(200,20)
        self.lbl_cat = QtWidgets.QLabel()
        self.lbl_cat.setText('Health')
        self.lbl_cat.resize(200,20)
        self.lbl_dur = QtWidgets.QLabel()
        self.lbl_dur.setText('10 min')
        self.lbl_dur.resize(200,20)
        self.lbl_data = QtWidgets.QLabel()
        self.lbl_data.setText('01.01.2021')
        self.lbl_data.resize(200,20)
        self.lbl_com = QtWidgets.QLabel()
        self.lbl_com.setText('Some shit')
        self.lbl_com.resize(200,20)
        
        self.grid.addWidget(self.lbl_action,1,0,1,4)
        # self.grid.addWidget(self.lbl_cat,0,1)
        # self.grid.addWidget(self.lbl_dur,0,2)
        # self.grid.addWidget(self.lbl_data,0,3)
        # self.grid.addWidget(self.lbl_com,0,4)
        self.grid.addWidget(QPushButton(str('Edit')),1,1,1,4)
        self.grid.addWidget(QPushButton(str('Delete')),1,2,1,4)
        
        
        # self.grid.addWidget(QPushButton(str(50)),2,0)
        # self.grid.addWidget(QPushButton(str(50)),3,0)
        # self.grid.addWidget(QPushButton(str(50)),4,0)
        # self.grid.addWidget(QPushButton(str(50)),5,0)
        self.grid.setRowStretch(6,3)	

        
        self.setLayout(self.grid)
        self.setWindowTitle("PyQt Grid Example")
        self.setGeometry(0, 0, 800, 600)

        self.center()

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())