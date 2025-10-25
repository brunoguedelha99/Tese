import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, 
                            QTableWidgetItem, QMessageBox, QComboBox, QCheckBox, QWidget, 
                            QHBoxLayout, QStackedWidget, QSlider, QLabel)
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
        
        #PREVIEW TAB
        self.tableOriginalPreview = self.findChild(QTableWidget, "tableOriginalPreview")
        self.tableAnonymizedPreview = self.findChild(QTableWidget, "tableAnonymizedPreview")
        self.pushButton_BackToAnonymize = self.findChild(QPushButton, "pushButtonBackToAnonymize")
        self.pushButton_ApplyAnonymization = self.findChild(QPushButton, "pushButtonApplyAnonymization")
        self.pushButton_BackToAnonymize.clicked.connect(self.clickedBackToAnonymize)
        self.pushButton_ApplyAnonymization.clicked.connect(self.clickedApplyAnonymization)

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
                file_extension = os.path.splitext(file_name)[1].lower()
                
                if file_extension in ['.xlsx', '.xls']:
                    print(f'Converting Excel file to CSV...')
                    excel_data = pd.read_excel(file_name)
                    excel_data.to_csv("Data.csv", index=False)
                    print(f'Converted {file_name} to Data.csv')
                else:
                    shutil.copy(file_name, "Data.csv")
                    print(f'Copied {file_name} to Data.csv')
                
                self.populateTable()
                self.populateAttributesTable()
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
        print("Populating table...")
        
        with open('Data.csv', 'r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)

        if len(data) == 0:
            return

        headerTableData = data[0]
        data = data[1:]
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headerTableData))
        self.table.setHorizontalHeaderLabels(headerTableData)
        
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                self.table.setItem(row_num, col_num, item)
                
        self.table.resizeColumnsToContents()
    #DATA TAB END    
    #ATTRIBUTES TAB
    def populateAttributesTable(self):
        try:
            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)

            self.tableAttributes.clear()
            self.tableAttributes.setRowCount(len(headers))
            self.tableAttributes.setColumnCount(5)
            attribute_headers = ["Column Name", "Data Type", "Sensitivity Level", "Sample Values", "Include"]
            self.tableAttributes.setHorizontalHeaderLabels(attribute_headers)

            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)
                sample_data = data[1:4] if len(data) > 3 else data[1:]

            for row_num, column_name in enumerate(headers):
                # Column Name
                name_item = QTableWidgetItem(column_name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tableAttributes.setItem(row_num, 0, name_item)

                # Data Type ComboBox
                data_type_combo = QComboBox()
                data_type_combo.addItems(["Text", "Number", "Date", "Boolean"])
                detected_type = self.detectDataType(column_name, sample_data, row_num)
                data_type_combo.setCurrentText(detected_type)
                self.tableAttributes.setCellWidget(row_num, 1, data_type_combo)

                # Sensitivity ComboBox
                sensitivity_combo = QComboBox()
                sensitivity_combo.addItems(["Low", "Medium", "High", "Critical"])
                sensitivity_combo.setCurrentText("Low")
                self.tableAttributes.setCellWidget(row_num, 2, sensitivity_combo)

                # Sample Values
                sample_values = self.getSampleValues(sample_data, row_num)
                sample_item = QTableWidgetItem(sample_values)
                sample_item.setFlags(sample_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tableAttributes.setItem(row_num, 3, sample_item)

                # Include Checkbox
                include_checkbox = QCheckBox()
                include_checkbox.setChecked(False)
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(include_checkbox)
                checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.tableAttributes.setCellWidget(row_num, 4, checkbox_widget)

            self.tableAttributes.resizeColumnsToContents()

        except Exception as e:
            print(f"Error populating attributes table: {e}")

    def detectDataType(self, column_name, sample_data, col_index):
        try:
            for row in sample_data:
                if col_index < len(row):
                    value = row[col_index].strip()
                    if value:
                        try:
                            float(value)
                            return "Number"
                        except ValueError:
                            if any(char in value for char in ['/', '-', ':']):
                                return "Date"
                            return "Text"
            return "Text"
        except:
            return "Text"

    def getSampleValues(self, sample_data, col_index):
        try:
            values = []
            for row in sample_data:
                if col_index < len(row) and row[col_index].strip():
                    values.append(row[col_index])
            
            display_values = values[:3]
            sample_text = ", ".join(display_values)
            
            if len(sample_text) > 30:
                sample_text = sample_text[:27] + "..."
                
            return sample_text + "..." if len(values) > 3 else sample_text
        except:
            return "N/A"
            
    def getSelectedAttributes(self):
        selected_columns = []

        for row in range(self.tableAttributes.rowCount()):
            column_item = self.tableAttributes.item(row, 0)
            column_name = column_item.text() if column_item else ""

            checkbox_widget = self.tableAttributes.cellWidget(row, 4)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    data_type_combo = self.tableAttributes.cellWidget(row, 1)
                    sensitivity_combo = self.tableAttributes.cellWidget(row, 2)

                    column_config = {
                        'name': column_name,
                        'data_type': data_type_combo.currentText() if data_type_combo else "Text",
                        'sensitivity': sensitivity_combo.currentText() if sensitivity_combo else "Low"
                    }
                    selected_columns.append(column_config)
    
        return selected_columns

    def clickedConfirmAttributes(self):
        print("Confirming attributes...")
        selected_attributes = self.getSelectedAttributes()
        
        if not selected_attributes:
            QMessageBox.warning(
                self, 
                "No Attributes Selected", 
                "⚠️ Please select at least one attribute for anonymization!\n\n"
                "Use the checkboxes in the 'Include' column to select which columns to anonymize."
            )
            return
        
        self.anonymization_config = selected_attributes
        
        summary_lines = []
        sensitivity_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        
        for attr in selected_attributes:
            sensitivity_counts[attr['sensitivity']] += 1
            summary_lines.append(f"• {attr['name']} ({attr['data_type']}) - {attr['sensitivity']}")
        
        summary_text = f"✅ {len(selected_attributes)} attributes configured for anonymization:\n\n"
        summary_text += "\n".join(summary_lines)
        summary_text += f"\n\n📊 Sensitivity Distribution:\n"
        
        for level, count in sensitivity_counts.items():
            if count > 0:
                icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}[level]
                summary_text += f"{icon} {level}: {count} attribute(s)\n"
        
        summary_text += f"\n🎯 Ready to configure anonymization parameters!"
        
        reply = QMessageBox.information(
            self, 
            "Attributes Configured Successfully", 
            summary_text,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Ok:
            print(f"\n=== ANONYMIZATION CONFIGURATION ===")
            for attr in selected_attributes:
                print(f"Column: {attr['name']:<15} | Type: {attr['data_type']:<8} | Sensitivity: {attr['sensitivity']}")
            print(f"=====================================\n")
            
            self.tabWidget.setCurrentIndex(3)
            
            QMessageBox.information(
                self,
                "Ready for Next Step",
                "🔄 Attributes configuration saved!\n\n"
                "You can now configure the anonymization techniques in the 'Anonymize' tab."
            )
    #DATA TAB END
    #ANONYMIZE TAB
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
            
            summary += "\n🎯 Ready to preview results!"
        else:
            summary = f"""✅ Anonymization Configuration Summary

⚙️ Mode: {mode_text}

Selected Attributes: {len(self.anonymization_config)}
"""
            for attr in self.anonymization_config:
                summary += f"  • {attr['name']} ({attr['sensitivity']})\n"
        
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
            
            # Popular tabelas de preview
            self.populatePreviewTables()
            
            # Avançar para Preview tab (index 4)
            self.tabWidget.setCurrentIndex(4)
    #ANONYMIZE TAB END
    #PREVIEW TAB
    def clickedBackToAnonymize(self):
        """Volta para a aba Anonymize"""
        self.tabWidget.setCurrentIndex(3)

    def populatePreviewTables(self):
        """Popula as tabelas de preview com dados originais e anonimizados"""
        try:
            # Ler dados originais
            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)
            
            if len(data) == 0:
                return
            
            headers = data[0]
            data_rows = data[1:11]  # Primeiras 10 linhas para preview
            
            # Filtrar apenas colunas selecionadas para anonimização
            selected_column_names = [attr['name'] for attr in self.anonymization_config]
            selected_indices = [i for i, h in enumerate(headers) if h in selected_column_names]
            
            # Configurar tabela ORIGINAL
            self.tableOriginalPreview.clear()
            self.tableOriginalPreview.setRowCount(len(data_rows))
            self.tableOriginalPreview.setColumnCount(len(headers))
            self.tableOriginalPreview.setHorizontalHeaderLabels(headers)
            
            for row_num, row_data in enumerate(data_rows):
                for col_num, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Destacar colunas que serão anonimizadas
                    if col_num in selected_indices:
                        item.setBackground(Qt.GlobalColor.yellow)
                    
                    self.tableOriginalPreview.setItem(row_num, col_num, item)
            
            self.tableOriginalPreview.resizeColumnsToContents()
            
            # Configurar tabela ANONIMIZADA (simulação)
            self.tableAnonymizedPreview.clear()
            self.tableAnonymizedPreview.setRowCount(len(data_rows))
            self.tableAnonymizedPreview.setColumnCount(len(headers))
            self.tableAnonymizedPreview.setHorizontalHeaderLabels(headers)
            
            for row_num, row_data in enumerate(data_rows):
                for col_num, cell_data in enumerate(row_data):
                    # Se coluna está selecionada, aplicar anonimização simulada
                    if col_num in selected_indices:
                        anonymized_value = self.simulateAnonymization(cell_data, headers[col_num])
                        item = QTableWidgetItem(anonymized_value)
                        item.setBackground(Qt.GlobalColor.lightGray)
                    else:
                        item = QTableWidgetItem(cell_data)
                    
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.tableAnonymizedPreview.setItem(row_num, col_num, item)
            
            self.tableAnonymizedPreview.resizeColumnsToContents()
            
            print("Preview tables populated successfully")
            
        except Exception as e:
            print(f"Error populating preview tables: {e}")
            QMessageBox.critical(self, "Error", f"Failed to generate preview:\n{str(e)}")

    def simulateAnonymization(self, value, column_name):
        """Simula anonimização baseada nas configurações"""
        
        # Encontrar configuração da coluna
        column_config = next((attr for attr in self.anonymization_config if attr['name'] == column_name), None)
        
        if not column_config:
            return value
        
        sensitivity = column_config['sensitivity']
        data_type = column_config['data_type']
        
        # Simulação baseada em sensibilidade
        if sensitivity == "Critical":
            # Masking pesado (80%)
            if len(value) > 2:
                return value[:1] + "*" * (len(value) - 2) + value[-1:]
            return "***"
        
        elif sensitivity == "High":
            # Masking moderado (60%)
            if data_type == "Text":
                if len(value) > 3:
                    visible = len(value) // 3
                    return value[:visible] + "*" * (len(value) - visible)
                return value[:1] + "**"
            elif data_type == "Number":
                # Generalização para números
                try:
                    num = float(value)
                    rounded = int(num / 10) * 10
                    return f"{rounded}-{rounded+10}"
                except:
                    return value
        
        elif sensitivity == "Medium":
            # Masking leve (30%)
            if data_type == "Text":
                if len(value) > 4:
                    return value[:2] + "*" * (len(value) - 4) + value[-2:]
                return value
            elif data_type == "Number":
                # Generalização mais ampla
                try:
                    num = float(value)
                    rounded = int(num / 100) * 100
                    return f"{rounded}-{rounded+100}"
                except:
                    return value
        
        else:  # Low
            return value

    def clickedApplyAnonymization(self):
        """Aplica a anonimização e avança para próxima etapa"""
        print("Applying anonymization...")
        
        # Confirmação
        reply = QMessageBox.question(
            self,
            "Apply Anonymization",
            "⚠️ Are you sure you want to apply these anonymization settings?\n\n"
            "This will:\n"
            f"• Anonymize {len(self.anonymization_config)} attribute(s)\n"
            f"• Use {self.privacy_params['mode']} mode\n"
            f"• K={self.privacy_params['k']}, L={self.privacy_params['l']}, T={self.privacy_params['t']}\n\n"
            "You can export the results after this step.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Aqui você aplicaria a anonimização real
            # Por enquanto, vamos simular com uma mensagem
            
            QMessageBox.information(
                self,
                "Processing",
                "🔄 Anonymization applied successfully!\n\n"
                "Data has been anonymized based on your configuration.\n\n"
                "Proceeding to Export tab..."
            )
            
            # Aplicar anonimização aos dados reais
            self.applyAnonymizationToData()
            
            # Avançar para Export tab
            self.tabWidget.setCurrentIndex(5)

    def applyAnonymizationToData(self):
        """Aplica a anonimização aos dados e guarda em Data.csv"""
        try:
            # Ler dados originais
            with open('Data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)
            
            if len(data) == 0:
                return
            
            headers = data[0]
            data_rows = data[1:]
            
            # Encontrar índices das colunas a anonimizar
            selected_column_names = [attr['name'] for attr in self.anonymization_config]
            selected_indices = [i for i, h in enumerate(headers) if h in selected_column_names]
            
            # Aplicar anonimização
            anonymized_data = [headers]
            for row in data_rows:
                new_row = []
                for col_num, cell_data in enumerate(row):
                    if col_num in selected_indices:
                        anonymized_value = self.simulateAnonymization(cell_data, headers[col_num])
                        new_row.append(anonymized_value)
                    else:
                        new_row.append(cell_data)
                anonymized_data.append(new_row)
            
            # Guardar dados anonimizados
            with open('Data.csv', 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(anonymized_data)
            
            print("Anonymization applied to Data.csv")
            
        except Exception as e:
            print(f"Error applying anonymization: {e}")
            QMessageBox.critical(self, "Error", f"Failed to apply anonymization:\n{str(e)}")
    #PREVIEW TAB END
    #EXPORT TAB
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
                df = pd.read_csv("Data.csv")
                
                if file_extension == '.csv':
                    df.to_csv(file_name, index=False)
                elif file_extension in ['.xlsx', '.xls']:
                    df.to_excel(file_name, index=False)
                else:
                    if not file_extension:
                        file_name += '.csv'
                    df.to_csv(file_name, index=False)
                
                QMessageBox.information(self, "Success", f"File exported successfully to {file_name}!")
                
            except Exception as e:
                error_message = f'Error exporting file: {str(e)}'
                print(error_message)
                QMessageBox.critical(self, "Error", error_message)

app = QApplication(sys.argv)
window = Application()
app.exec()