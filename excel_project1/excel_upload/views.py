# views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExcelFileForm, ExcelDataRowForm
import pandas as pd
from .models import ExcelFile
from django.http import JsonResponse

def upload_excel_file(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to the database
            excel_file_instance = ExcelFile(file=request.FILES['file'])
            excel_file_instance.save()

            return redirect('display_table')  # Redirect to the page where you display the uploaded file
    else:
        form = ExcelFileForm()
    return render(request, 'upload_excel_file.html', {'form': form})

def display_table(request):
    # Retrieve data from the database using Django ORM
    excel_files = ExcelFile.objects.all()
    return render(request, 'display_table.html', {'excel_files': excel_files})


def delete(request,excel_file_id):
    s = ExcelFile.objects.get(id=excel_file_id)
    s.delete()
    return display_table(request)


def update(request, excel_file_id):
    # Get the ExcelFile instance
    excel_file = get_object_or_404(ExcelFile, id=excel_file_id)

    if request.method == 'POST':
        # Instantiate the form with the POST data
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form to update the record in the database
            excel_file.file = form.cleaned_data['file']
            excel_file.save()
            # Redirect to the display table page
            return redirect('display_table')
    else:
        # Instantiate the form with the existing data
        initial_data = {'file': excel_file.file}
        form = ExcelFileForm(initial=initial_data)

    # Pass the form to the template
    context = {'form': form}
    return render(request, 'edit_data.html', context)

def display_excel_data(request, excel_file_id):
    excel_file = get_object_or_404(ExcelFile, id=excel_file_id)
    df = excel_file.get_data_frame()
    headers = df.columns
    data = df.to_dict(orient='records')
    return render(request, 'display_excel_data.html', {'excel_file': excel_file, 'headers': headers, 'data': data})


def save_row_changes(request):
    if request.method == 'POST':
        try:
            row_data = json.loads(request.body)
            excel_file_id = row_data.get('excel_file_id')
            row_id = row_data.get('row_id')
            updated_values = row_data.get('updated_values')

            excel_file = get_object_or_404(ExcelFile, id=excel_file_id)
            df = pd.read_excel(excel_file.file)

            for column, value in updated_values.items():
                df.at[row_id, column] = value

            df.to_excel(excel_file.file, index=False)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def save_all_changes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            excel_file_id = data.get('excel_file_id')
            updated_rows = data.get('updated_rows', {})

            excel_file = get_object_or_404(ExcelFile, id=excel_file_id)
            df = pd.read_excel(excel_file.file)

            for row_id, row_data in updated_rows.items():
                row_id = int(row_id)  # Convert row_id to integer
                for column, value in row_data.items():
                    df.at[row_id, column] = value

            df.to_excel(excel_file.file, index=False)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

