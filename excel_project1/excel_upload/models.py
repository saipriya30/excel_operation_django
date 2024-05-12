# models.py

import pandas as pd
from django.db import models

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def get_data_frame(self):
        try:
            df = pd.read_excel(self.file)
            return df
        except Exception as e:
            return None

    def update_data(self, row_data):
        try:
            df = self.get_data_frame()
            for key, value in row_data.items():
                row_index, column_name = key.split('-')[1:]
                row_index = int(row_index)
                df.at[row_index, column_name] = value
            df.to_excel(self.file, index=False)
            return True
        except Exception as e:
            return False
