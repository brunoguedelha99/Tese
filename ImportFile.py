from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import sys
from PyQt6.uic import loadUi

class ImportFile(QMainWindow):
    def __init__(self):
        super(ImportFile,self).__init__()
        loadUi("./ImportFile.ui", self)
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.show()

    def clickedImport(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

        if file_name:
            print(f'Selected file: {file_name}')

app = QApplication(sys.argv)
window = ImportFile()
sys.exit(app.exec())
