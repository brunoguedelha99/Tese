import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys
from PyQt6.uic import loadUi


class DisplayData(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./DisplayData.ui", self)
        self.show()
        self.table = self.findChild(QTableWidget)
        self.populateTable()
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayData()
    sys.exit(app.exec())
