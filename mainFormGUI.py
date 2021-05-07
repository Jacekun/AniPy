import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from mainForm import Ui_mainForm

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_mainForm()
        self.ui.setupUi(self)
    
    def setUsername(self, text):
        self.ui.txtUsername.setText(text)
    
    def getUsername(self):
        return self.ui.txtUsername.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    window.setUsername("Username")
    print(window.getUsername())

    sys.exit(app.exec_())