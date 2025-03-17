from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import sys
from PyQt6.uic import loadUi
import shutil
from DisplayData import DisplayDataUI

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        loadUi("./Application.ui", self)
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.show()

    #IMPORT FILE TAB
    def clickedImport(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

        if file_name:
            print(f'Selected file: {file_name}')
            try:
                # Copy the selected CSV file to "Data.csv"
                shutil.copy(file_name, "Data.csv")
                print(f'Copied {file_name} to Data.csv')

            except Exception as e:
                print(f'Error copying file: {str(e)}')

app = QApplication(sys.argv)
window = Application()
app.exec()