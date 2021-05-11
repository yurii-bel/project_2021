import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # self.window()

    def init_ui(self):
        # set the title
        self.setWindowTitle("Geometry")
  
        # setting  the geometry of window
        # setGeometry(left, top, width, height)
        self.setGeometry(0, 0, 1400, 900)
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

    # def window(self):
    #     self.win = QWidget()
    #     self.grid = QGridLayout()
	
    #     for i in range(0,5):
    #         for j in range(0,5):
    #             self.grid.addWidget(QPushButton(str(i)+str(j)),i,j)
			
    #     self.win.setLayout(self.grid)
    #     self.win.setWindowTitle("PyQt Grid Example")
    #     self.win.setGeometry(50,50,200,200)
    #     self.win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())