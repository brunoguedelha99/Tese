import csv
from PyQt6.QtWidgets import QMainWindow, QTableWidget,QPushButton, QTableWidgetItem, QFileDialog, QComboBox,QLabel
import sys
from PyQt6.uic import loadUi
from DataMasking import DataMaskingUI

class DisplayDataUI(QMainWindow):  # Renamed the class to DisplayDataUI
    def __init__(self):
        super(DisplayDataUI,self).__init__()
        loadUi("./DisplayData.ui", self)
        self.table = self.findChild(QTableWidget,"tableData")
        self.tableAnonymizationSett = self.findChild(QTableWidget,"tableAnonymizationSett")
        self.pushButton_ExportToFile = self.findChild(QPushButton, "pushExportButton")
        self.pushButton_ExportToFile.clicked.connect(self.clickedExport)
        self.pushAddButton = self.findChild(QPushButton,"pushAddButton")
        self.pushAddButton.clicked.connect(self.clickedAdd)
        self.columnComboBox=self.findChild(QComboBox , "columnComboBox")
        self.anonymizationComboBox=self.findChild(QComboBox , "anonymizationComboBox")
        self.anonymizationComboBox.addItem("Generalization")
        self.anonymizationComboBox.addItem("Suppression")
        self.anonymizationComboBox.addItem("Pseudonymization")
        self.anonymizationComboBox.addItem("Data Masking")
        self.anonymizationComboBox.addItem("Aggregation")
        self.dataTypeComboBox=self.findChild(QComboBox,"dataTypeComboBox")
        """ self.dataTypeComboBox.addItem("Text")
        self.dataTypeComboBox.addItem("Number")
        self.dataTypeComboBox.addItem("Date") """
        self.labelAddError = self.findChild(QLabel, "labelAddError") 
        self.populateTables()
        self.anonymization_settings = []
        
    def clickedExport(self):
        # Open a file dialog for the user to choose the save location and file name
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)")
        
        # Proceed only if the user selected a path
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                
                # Write header row
                headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                writer.writerow(headers)

                # Write table data rows
                for row in range(self.table.rowCount()):
                    row_data = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
                    writer.writerow(row_data)

    def populateTables(self):
        self.table.clear()
        self.tableAnonymizationSett.clear()
        self.columnComboBox.clear()

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
        
        #TABLE ANONYMIZATION SETTINGS#
        headerTableAnonymization=['Column','Anonymization type']
        self.tableAnonymizationSett.setColumnCount(len(headerTableAnonymization))
        self.tableAnonymizationSett.setHorizontalHeaderLabels(headerTableAnonymization)
        print(headerTableAnonymization)

        self.columnComboBox.addItems(headerTableData)
        
    
    def clickedAdd(self):
        # Get the selected column and anonymization type from the combo boxes
        selected_column = self.columnComboBox.currentText()
        selected_anonymization = self.anonymizationComboBox.currentText()

        # Check if the selected values are not empty
        if selected_column and selected_anonymization:
            # Append the selected values as a new list to the anonymization_settings
            self.anonymization_settings.append([selected_column, selected_anonymization])
            print(f'Added: {selected_column}, {selected_anonymization}')
            print(f'Current settings: {self.anonymization_settings}')

            # Optionally, you can also update the tableAnonymizationSett to reflect the new entry
            current_row_count = self.tableAnonymizationSett.rowCount()
            self.tableAnonymizationSett.insertRow(current_row_count)
            self.tableAnonymizationSett.setItem(current_row_count, 0, QTableWidgetItem(selected_column))
            self.tableAnonymizationSett.setItem(current_row_count, 1, QTableWidgetItem(selected_anonymization))
            
            # Delete column added from combo box
            self.columnComboBox.removeItem(self.columnComboBox.findText(selected_column))
            
            # Clear the combo boxes after adding
            self.columnComboBox.setCurrentIndex(-1)
            self.anonymizationComboBox.setCurrentIndex(-1)
            self.labelAddError.setText("<span style='color: green;'>Added successfully!</span>")
            self.display_data_masking = DataMaskingUI()
            self.display_data_masking.show()
        else:
            # Optionally, show an error message if inputs are invalid
            self.labelAddError.setText("<span style='color: red;'>Please select a column and an anonymization type!</span>")
            self.display_data_masking = DataMaskingUI()
            self.display_data_masking.show()