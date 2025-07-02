import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QTableWidget, QTableWidgetItem, QLabel
import sys
from PyQt6.uic import loadUi
import shutil
from DisplayData import DisplayDataUI

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        loadUi("./Application.ui", self)
        #IMPORT FILE TAB
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.labelAddError = self.findChild(QLabel, "labelAddError") 
        
        #DATA TAB
        self.table = self.findChild(QTableWidget, "tableData")
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
                self.labelAddError.setText("<span style='color: green;'>Added successfully!</span>")
            except Exception as e:
                print(f'Error copying file: {str(e)}')
                self.labelAddError.setText("<span style='color: red;'>Error copying file: "+{str(e)}+"</span>")
        self.populateDataTable()
                
    #DATA TAB
    def populateDataTable(self):
        self.table.clear()
        #TABLE DATA#
        
        # Open the CSV file and read its data
        with open('Data.csv', 'r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        if len(data) == 0:
            return  # No data to display

        headerTableData = data[0]  # Use the first row as the header
        print(headerTableData)
        data = data[1:]   # Remove the header from the data

        # Set the number of rows and columns in the table
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headerTableData))
        
        # Set the header labels for the columns
        self.table.setHorizontalHeaderLabels(headerTableData)
        
        # Populate the table with data from the CSV file
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                self.table.setItem(row_num, col_num, item) 
        #END OF TABLE DATA#        
        
    def populateAttributesTable(self):
        
        pass

app = QApplication(sys.argv)
window = Application()
app.exec()