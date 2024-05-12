from django.contrib import admin

from django.contrib import admin
from .models import ExcelFile

# Register your models here.

# Option 1: Register the model directly
admin.site.register(ExcelFile)