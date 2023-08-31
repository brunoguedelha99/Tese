from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import sys
from PyQt5 import uic

class ImportFile(QMainWindow):
    def __init__(self):
        super(ImportFile, self).__init__()
        uic.loadUi("./ImportFile.ui", self)
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.show()

    def clickedImport(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_name:
            print(f'Selected file: {file_name}')

app = QApplication(sys.argv)
window = ImportFile()
app.exec_()
