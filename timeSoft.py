import sys
sys.path.append(".")
from PyQt5 import QtWidgets, uic

from design.new_mainUI import Ui_MainWindow as main_ui  # Main win
from design.new_editUI_view import Ui_MainWindow as edit_ui  # Add action win
from final_test.actions import Actions


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.mui = main_ui()
        self.mui.setupUi(self)

        self.mui.btn_add_action.clicked.connect(self.add_action)

    def add_action(self):
        self.aui = Actions()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainUI()
    win.show()
    sys.exit(app.exec())
