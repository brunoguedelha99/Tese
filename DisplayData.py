import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget,QPushButton, QTableWidgetItem, QFileDialog
import sys
from PyQt6.uic import loadUi

class DisplayDataUI(QMainWindow):  # Renamed the class to DisplayDataUI
    def __init__(self):
        super(DisplayDataUI,self).__init__()
        loadUi("./DisplayData.ui", self)
        self.show()
        self.table = self.findChild(QTableWidget)
        self.populateTable()
        self.show()
        self.pushButton_ExportToFile = self.findChild(QPushButton, "pushExportButton")
        self.pushButton_ExportToFile.clicked.connect(self.clickedExport)

    def clickedExport(self):
        # Open a file dialog for the user to choose the save location and file name
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
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


    def populateTable(self):
        self.table.clear()

        # Open the CSV file and read its data
        with open('Data.csv', 'r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        if len(data) == 0:
            return  # No data to display

        header = data[0]  # Use the first row as the header
        data = data[1:]   # Remove the header from the data

        # Set the number of rows and columns in the table
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(header))

        # Set the header labels for the columns
        self.table.setHorizontalHeaderLabels(header)

        # Populate the table with data from the CSV file
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                self.table.setItem(row_num, col_num, item)