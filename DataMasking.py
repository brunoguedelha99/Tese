import csv
from PyQt6.QtWidgets import QMainWindow, QTableWidget,QPushButton, QTableWidgetItem, QFileDialog, QComboBox,QLabel
import sys
from PyQt6.uic import loadUi

class DataMaskingUI(QMainWindow):
    def __init__(self):
        super(DataMaskingUI, self).__init__()
        loadUi("./DataMasking.ui", self)
        self.pushButton_DataMaskingConfirm = self.findChild(QPushButton, "pushDataMaskingConfirmButton")
        self.pushButton_DataMaskingCancel.clicked.connect(self.clickedConfirmDataMasking)
        self.pushButton_DataMaskingCancel = self.findChild(QPushButton, "pushDataMaskingCancelButton")
        self.pushButton_DataMaskingCancel.clicked.connect(self.clickedCancelDataMasking)
        self.show()

    def clickedConfirmDataMasking(self):
        print("Confirm")

    def clickedCancelDataMasking(self):
        print("Cancel")