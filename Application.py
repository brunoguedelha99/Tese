import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog,QTableWidget, QTableWidgetItem, QMessageBox,QComboBox, QCheckBox, QWidget, QHBoxLayout,QStackedWidget,QSlider,QLabel
import sys
from PyQt6.uic import loadUi
import shutil
import pandas as pd
import os

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        loadUi("./Application.ui", self)
        self.tabWidget.setCurrentIndex(0)
        
        #IMPORT FILE TAB
        self.pushButton_ImportFile = self.findChild(QPushButton, "pushButtonImportFile")
        self.pushButton_ImportFile.clicked.connect(self.clickedImport)
        
        #DATA TAB
        self.table = self.findChild(QTableWidget,"tableData")
        
        #ATTRIBUTES TAB
        self.pushButton_ConfirmAttributes = self.findChild(QPushButton, "pushButtonConfirm")
        self.pushButton_ConfirmAttributes.clicked.connect(self.clickedConfirmAttributes)
        self.tableAttributes = self.findChild(QTableWidget, "tableAttributes")

       #ANONYMIZE TAB
        self.stackedWidgetAnonymize = self.findChild(QStackedWidget, "stackedWidgetAnonymize")
        
        # Mode toggle buttons
        self.pushButton_AutoMode = self.findChild(QPushButton, "pushButtonAutoMode")
        self.pushButton_AdvancedMode = self.findChild(QPushButton, "pushButtonAdvancedMode")
        self.pushButton_AutoMode.clicked.connect(lambda: self.switchAnonymizeMode(0))
        self.pushButton_AdvancedMode.clicked.connect(lambda: self.switchAnonymizeMode(1))
        
        # K-Anonymity slider
        self.slider_KAnonymity = self.findChild(QSlider, "sliderKAnonymity")
        self.label_KValue = self.findChild(QLabel, "labelKValue")
        self.slider_KAnonymity.valueChanged.connect(self.updateKValue)
        
        # L-Diversity slider
        self.slider_LDiversity = self.findChild(QSlider, "sliderLDiversity")
        self.label_LValue = self.findChild(QLabel, "labelLValue")
        self.slider_LDiversity.valueChanged.connect(self.updateLValue)
        
        # T-Closeness slider
        self.slider_TCloseness = self.findChild(QSlider, "sliderTCloseness")
        self.label_TValue = self.findChild(QLabel, "labelTValue")
        self.slider_TCloseness.valueChanged.connect(self.updateTValue)
        
        # Navigation buttons
        self.pushButton_BackToAttributes = self.findChild(QPushButton, "pushButtonBackToAttributes")
        self.pushButton_ContinueToPreview = self.findChild(QPushButton, "pushButtonContinueToPreview")
        self.pushButton_BackToAttributes.clicked.connect(self.clickedBackToAttributes)
        self.pushButton_ContinueToPreview.clicked.connect(self.clickedContinueToPreview)

        #EXPORT DATA TAB
        self.pushButton_ExportData = self.findChild(QPushButton, "pushButtonExportData")
        self.pushButton_ExportData.clicked.connect(self.clickedExport)
        
        # Variáveis para guardar configurações
        self.anonymization_config = []
        self.privacy_params = {
            'k': 3,
            'l': 2,
            't': 0.2,
            'mode': 'automatic'
        }
        
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
                self.populateAttributesTable()
                
                # Switch to the Data tab (index 1)
                self.tabWidget.setCurrentIndex(1)
                
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
        #END OF TABLE DATA#        
        self.table.resizeColumnsToContents()
#DATA TAB END

#ATTRIBUTES TAB BEGIN        
    def populateAttributesTable(self):
        """Popula a tabela de atributos sem auto-suggestions"""
        try:
            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)  # Primeira linha = headers

            # Configurar tabela
            self.tableAttributes.clear()
            self.tableAttributes.setRowCount(len(headers))
            self.tableAttributes.setColumnCount(5)

            # Headers da tabela
            attribute_headers = ["Column Name", "Data Type", "Sensitivity Level", "Sample Values", "Include"]
            self.tableAttributes.setHorizontalHeaderLabels(attribute_headers)

            # Ler dados para samples
            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)
                sample_data = data[1:4] if len(data) > 3 else data[1:]

            # Preencher cada linha
            for row_num, column_name in enumerate(headers):
                # Column Name
                name_item = QTableWidgetItem(column_name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tableAttributes.setItem(row_num, 0, name_item)

                # Data Type ComboBox - MANTER AUTO-DETECTION
                data_type_combo = QComboBox()
                data_type_combo.addItems(["Text", "Number", "Date", "Boolean"])
                detected_type = self.detectDataType(column_name, sample_data, row_num)
                data_type_combo.setCurrentText(detected_type)
                self.tableAttributes.setCellWidget(row_num, 1, data_type_combo)

                # Sensitivity ComboBox - SEM AUTO-SUGGESTION, SEMPRE "Low"
                sensitivity_combo = QComboBox()
                sensitivity_combo.addItems(["Low", "Medium", "High", "Critical"])
                sensitivity_combo.setCurrentText("Low")  # SEMPRE "Low" por defeito
                self.tableAttributes.setCellWidget(row_num, 2, sensitivity_combo)

                # Sample Values
                sample_values = self.getSampleValues(sample_data, row_num)
                sample_item = QTableWidgetItem(sample_values)
                sample_item.setFlags(sample_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tableAttributes.setItem(row_num, 3, sample_item)

                # Include Checkbox - SEMPRE DESMARCADA
                include_checkbox = QCheckBox()
                include_checkbox.setChecked(False)  # SEMPRE começa desmarcada

                # Centrar checkbox
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(include_checkbox)
                checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                self.tableAttributes.setCellWidget(row_num, 4, checkbox_widget)

            # Adjust column widths
            self.tableAttributes.resizeColumnsToContents()

        except Exception as e:
            print(f"Error populating attributes table: {e}")

    def detectDataType(self, column_name, sample_data, col_index):
        """Auto-detecta o tipo de dados baseado no conteúdo"""
        try:
            # Verificar se é numérico
            for row in sample_data:
                if col_index < len(row):
                    value = row[col_index].strip()
                    if value:  # Se não estiver vazio
                        try:
                            float(value)
                            return "Number"
                        except ValueError:
                            # Verificar se é data (contém /, - ou :)
                            if any(char in value for char in ['/', '-', ':']):
                                return "Date"
                            return "Text"
            return "Text"  # Default
        except:
            return "Text"

    def getSampleValues(self, sample_data, col_index):
        """Obtém valores de exemplo para a coluna"""
        try:
            values = []
            for row in sample_data:
                if col_index < len(row) and row[col_index].strip():
                    values.append(row[col_index])
            
            # Máximo 3 valores
            display_values = values[:3]
            sample_text = ", ".join(display_values)
            
            # Truncar se muito longo
            if len(sample_text) > 30:
                sample_text = sample_text[:27] + "..."
                
            return sample_text + "..." if len(values) > 3 else sample_text
            
        except:
            return "N/A"
            
    def getSelectedAttributes(self):
        """Retorna lista de colunas selecionadas para anonimização"""
        selected_columns = []

        for row in range(self.tableAttributes.rowCount()):
            # Get column name
            column_item = self.tableAttributes.item(row, 0)
            column_name = column_item.text() if column_item else ""

            # Get checkbox (está dentro de um widget)
            checkbox_widget = self.tableAttributes.cellWidget(row, 4)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    # Get other configurations
                    data_type_combo = self.tableAttributes.cellWidget(row, 1)
                    sensitivity_combo = self.tableAttributes.cellWidget(row, 2)

                    column_config = {
                        'name': column_name,
                        'data_type': data_type_combo.currentText() if data_type_combo else "Text",
                        'sensitivity': sensitivity_combo.currentText() if sensitivity_combo else "Low"
                    }
                    selected_columns.append(column_config)
    
        return selected_columns

    #ATTRIBUTES TAB - CONFIRM BUTTON
    def clickedConfirmAttributes(self):
        """Confirma as configurações dos atributos e avança para próxima aba"""
        print("Confirming attributes...")
        
        # Obter atributos selecionados
        selected_attributes = self.getSelectedAttributes()
        
        # Validação: verificar se pelo menos um atributo foi selecionado
        if not selected_attributes:
            QMessageBox.warning(
                self, 
                "No Attributes Selected", 
                "⚠️ Please select at least one attribute for anonymization!\n\n"
                "Use the checkboxes in the 'Include' column to select which columns to anonymize."
            )
            return
        
        # Guardar configuração para usar nas próximas abas
        self.anonymization_config = selected_attributes
        
        # Criar resumo das configurações
        summary_lines = []
        sensitivity_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        
        for attr in selected_attributes:
            sensitivity_counts[attr['sensitivity']] += 1
            summary_lines.append(f"• {attr['name']} ({attr['data_type']}) - {attr['sensitivity']}")
        
        # Criar texto do resumo
        summary_text = f"✅ {len(selected_attributes)} attributes configured for anonymization:\n\n"
        summary_text += "\n".join(summary_lines)
        summary_text += f"\n\n📊 Sensitivity Distribution:\n"
        
        for level, count in sensitivity_counts.items():
            if count > 0:
                icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}[level]
                summary_text += f"{icon} {level}: {count} attribute(s)\n"
        
        summary_text += f"\n🎯 Ready to configure anonymization parameters!"
        
        # Mostrar confirmação
        reply = QMessageBox.information(
            self, 
            "Attributes Configured Successfully", 
            summary_text,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Ok:
            # Debug: Imprimir configurações no console
            print(f"\n=== ANONYMIZATION CONFIGURATION ===")
            for attr in selected_attributes:
                print(f"Column: {attr['name']:<15} | Type: {attr['data_type']:<8} | Sensitivity: {attr['sensitivity']}")
            print(f"=====================================\n")
            
            # Avançar para a aba Anonymize (index 3)
            self.tabWidget.setCurrentIndex(3)
            
            # Mostrar mensagem de sucesso
            QMessageBox.information(
                self,
                "Ready for Next Step",
                "🔄 Attributes configuration saved!\n\n"
                "You can now configure the anonymization techniques in the 'Anonymize' tab."
            )
#ATTRIBUTES TAB END

#ANONYMIZE TAB BEGIN
    def switchAnonymizeMode(self, mode_index):
            """Alterna entre Modo Automático (0) e Modo Advanced (1)"""
            self.stackedWidgetAnonymize.setCurrentIndex(mode_index)

            if mode_index == 0:
                self.pushButton_AutoMode.setChecked(True)
                self.pushButton_AdvancedMode.setChecked(False)
                self.privacy_params['mode'] = 'automatic'
                print("Switched to Automatic Mode")
            else:
                self.pushButton_AutoMode.setChecked(False)
                self.pushButton_AdvancedMode.setChecked(True)
                self.privacy_params['mode'] = 'advanced'
                print("Switched to Advanced Mode")

    def updateKValue(self, value):
        """Atualiza o valor do K-Anonymity"""
        self.label_KValue.setText(f"k = {value}")
        self.privacy_params['k'] = value
        print(f"K-Anonymity updated to: {value}")

    def updateLValue(self, value):
        """Atualiza o valor do L-Diversity"""
        self.label_LValue.setText(f"l = {value}")
        self.privacy_params['l'] = value
        print(f"L-Diversity updated to: {value}")

    def updateTValue(self, value):
        """Atualiza o valor do T-Closeness"""
        t_value = value / 10.0
        self.label_TValue.setText(f"t = {t_value:.1f}")
        self.privacy_params['t'] = t_value
        print(f"T-Closeness updated to: {t_value}")

    def clickedBackToAttributes(self):
        """Volta para a aba Attributes"""
        self.tabWidget.setCurrentIndex(2)

    def clickedContinueToPreview(self):
        """Valida configurações e avança para Preview"""
        print("Continuing to Preview...")
        
        if not self.anonymization_config:
            QMessageBox.warning(
                self,
                "No Configuration",
                "⚠️ Please configure attributes first!\n\n"
                "Go to the 'Attributes' tab and select columns for anonymization."
            )
            self.tabWidget.setCurrentIndex(2)
            return
        
        mode_text = "Automatic" if self.privacy_params['mode'] == 'automatic' else "Advanced"
        
        if self.privacy_params['mode'] == 'automatic':
            summary = f"""✅ Anonymization Configuration Summary

                📊 Mode: {mode_text}

                Privacy Parameters:
                🔹 K-Anonymity: k = {self.privacy_params['k']}
                   → Minimum {self.privacy_params['k']} indistinguishable records

                🔹 L-Diversity: l = {self.privacy_params['l']}
                   → Minimum {self.privacy_params['l']} different sensitive values

                🔹 T-Closeness: t = {self.privacy_params['t']}
                   → Maximum distance of {self.privacy_params['t']} from global distribution

                Selected Attributes: {len(self.anonymization_config)}
                """
            for attr in self.anonymization_config:
                summary += f"  • {attr['name']} ({attr['sensitivity']})\n"

                summary += "\n🎯 The system will automatically apply appropriate techniques."
        else:
            summary = f"""✅ Anonymization Configuration Summary

                ⚙️ Mode: {mode_text}

                Selected Attributes: {len(self.anonymization_config)}
                """
            for attr in self.anonymization_config:
                summary += f"  • {attr['name']} ({attr['sensitivity']})\n"

                summary += "\n⚠️ Manual technique configuration required."

                reply = QMessageBox.information(
                    self,
                    "Ready for Preview",
                    summary,
                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
                )

                if reply == QMessageBox.StandardButton.Ok:
                    print(f"\n=== PRIVACY PARAMETERS ===")
                    print(f"Mode: {self.privacy_params['mode']}")
                    print(f"K-Anonymity: {self.privacy_params['k']}")
                    print(f"L-Diversity: {self.privacy_params['l']}")
                    print(f"T-Closeness: {self.privacy_params['t']}")
                    print(f"==========================\n")
    
                    QMessageBox.information(
                        self,
                        "Preview Tab",
                        "🚧 Preview tab will be implemented next!\n\n"
                        "Configuration saved successfully."
                    )

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