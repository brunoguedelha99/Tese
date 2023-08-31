from PyQt5.QtWidgets import QMainWindow, QPushButton 
from PyQt5 import uic


class ImportFile(QMainWindow):
	def __init__(self):
		super(ImportFile, self).__init__()
		uic.loadUi("./ImportFile.ui", self)
		self.pushButton_ImportFile=self.findChild(QPushButton,"pushButtonImportFile")
		self.pushButton_ImportFile.clicked.connect(self.clickedImport)

		self.show()
	
	def clickedImport(self):
		print('Imported') 


		

