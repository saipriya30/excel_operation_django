# urls.py
from django.urls import path
from . import views

urlpatterns = [
path('upload/', views.upload_excel_file, name='upload_excel_file'),
path('display/', views.display_table, name='display_table'),
path('delete/<int:excel_file_id>/', views.delete, name='delete'),
path('update/<int:excel_file_id>/', views.update, name='update'),
path('excel_data/<int:excel_file_id>/', views.display_excel_data, name='display_excel_data'),
path('save-row-changes/', views.save_row_changes, name='save_row_changes'),
path('save-all-changes/', views.save_all_changes, name='save_all_changes'),
]