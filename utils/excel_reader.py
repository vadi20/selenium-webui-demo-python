import openpyxl
from pathlib import Path

class ExcelReader:
    @staticmethod
    def get_data(file_name, sheet_name):
        try:
            test_data_path = Path(__file__).parent.parent.joinpath('test-data', file_name)
            workbook = openpyxl.load_workbook(test_data_path)
            sheet = workbook[sheet_name]
            
            headers = [cell.value for cell in sheet[1]]
            
            test_data = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                test_data.append(dict(zip(headers, row)))
            
            return test_data
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")