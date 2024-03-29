from django.contrib import admin
from .models import ResultDiagnostic


# Register your models here.

@admin.register(ResultDiagnostic)
class ResultDiagnosticAdmin(admin.ModelAdmin):
    list_display = ['type_diagnostic', 'date']
    list_filter = ['type_diagnostic', 'date']
