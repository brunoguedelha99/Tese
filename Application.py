import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
import sys
from PyQt6.uic import loadUi
import shutil
import pandas as pd
import os

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        loadUi("./Application.ui", self)
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        self.pushButton_ExportData = self.findChild(QPushButton, "pushButtonExportData")
        self.pushButton_ExportData.clicked.connect(self.clickedExport)
        self.table = self.findChild(QTableWidget,"tableData")
        self.show()

    #IMPORT TAB BEGIN
    def clickedImport(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Data File", 
            "", 
            "Data Files (*.csv *.xlsx *.xls);;CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if file_name:
            print(f'Selected file: {file_name}')
            try:
                # Check if it's an Excel file
                file_extension = os.path.splitext(file_name)[1].lower()
                
                if file_extension in ['.xlsx', '.xls']:
                    # Convert Excel to CSV
                    print(f'Converting Excel file to CSV...')
                    excel_data = pd.read_excel(file_name)
                    excel_data.to_csv("Data.csv", index=False)
                    print(f'Converted {file_name} to Data.csv')
                else:
                    # Copy the selected CSV file to "Data.csv"
                    shutil.copy(file_name, "Data.csv")
                    print(f'Copied {file_name} to Data.csv')
                
                self.populateTable()
                
                # Switch to the Data tab (index 3)
                self.tabWidget.setCurrentIndex(3)
                
                QMessageBox.information(self, "Success", "File imported successfully!")

            except Exception as e:
                error_message = f'Error processing file: {str(e)}'
                print(error_message)
                QMessageBox.critical(self, "Error", error_message)
    #IMPORT TAB END

    #DATA TAB BEGIN
    def populateTable(self):
        self.table.clear()
        print("Populating...")
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
    
    #EXPORT TAB BEGIN
    def clickedExport(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data File",
            "",
            "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_name:
            try:
                file_extension = os.path.splitext(file_name)[1].lower()
                
                # Read the current data from Data.csv
                df = pd.read_csv("Data.csv")
                
                # Export based on the selected file extension
                if file_extension == '.csv':
                    df.to_csv(file_name, index=False)
                elif file_extension in ['.xlsx', '.xls']:
                    df.to_excel(file_name, index=False)
                else:
                    # Default to CSV if no extension or unrecognized extension
                    if not file_extension:
                        file_name += '.csv'
                    df.to_csv(file_name, index=False)
                
                QMessageBox.information(self, "Success", f"File exported successfully to {file_name}!")
                
            except Exception as e:
                error_message = f'Error exporting file: {str(e)}'
                print(error_message)
                QMessageBox.critical(self, "Error", error_message)
    #EXPORT TAB END

app = QApplication(sys.argv)
window = Application()
app.exec()