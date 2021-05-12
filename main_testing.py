import sys

from PyQt5 import QtWidgets, uic

from addding_editing_actions_ui import ActionUI
from design.mainUI import MainWindowUI


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.mUi = MainWindowUI()
        self.mUi.setupUi(self)

        self.aUi = ActionUI()

        self.mUi.btn_add_action.clicked.connect(self.add_action)

    def add_action(self):
        self.aUi.show()
        self.aUi.save_event()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec())
