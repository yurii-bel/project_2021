import sys
sys.path.append(".")

from PyQt5 import QtWidgets, uic

from logic.addding_editing_actions_ui import ActionUI

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.mUi = uic.loadUi('design\\main.ui')
        self.aUi = ActionUI()

        self.mUi.btn_plus.clicked.connect(self.add_action)
        
        self.mUi.show()

    def add_action(self):
        self.aUi.aUi.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    sys.exit(app.exec())
