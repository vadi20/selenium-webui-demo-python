import json
import os
from pathlib import Path

class JSONReader:
    @staticmethod
    def get_data(file_name, key):
        try:
            test_data_path = Path(__file__).parent.parent.joinpath('test-data', file_name)
            with open(test_data_path) as f:
                data = json.load(f)
            return data[key]
        except Exception as e:
            raise Exception(f"Error reading JSON file: {str(e)}")