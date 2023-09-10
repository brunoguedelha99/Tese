from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
import sys
from PyQt6.uic import loadUi


def populateTable(self,csv):
		self.tableData.clear()
		
		
class DisplayData(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./ImportFile.ui", self)
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.show()

    def clickedImport(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

        if file_name:
            print(f'Selected file: {file_name}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayData()
    sys.exit(app.exec())
