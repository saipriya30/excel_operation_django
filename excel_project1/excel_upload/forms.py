from django import forms

class ExcelFileForm(forms.Form):
    file = forms.FileField(label='Select Excel File')
   
# forms.py

from django import forms
from .models import ExcelFile

class ExcelDataRowForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = '__all__'  # Include all fields from the model

    def __init__(self, *args, **kwargs):
        super(ExcelDataRowForm, self).__init__(*args, **kwargs)
        # Customize form fields here if needed

