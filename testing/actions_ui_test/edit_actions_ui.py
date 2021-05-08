import sys
from typing import NamedTuple
from PyQt5 import QtWidgets, uic

class ActionUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.aUi = uic.loadUi('design\\edit_event.ui')

        self.aUi.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ActionUI()
    sys.exit(app.exec())
    