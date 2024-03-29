from django.contrib import admin
from .models import Diagnostic,PhotoDiagnostic


# Register your models here.

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ['type', 'slug']
    prepopulated_fields = {'slug': ('type',)}


@admin.register(PhotoDiagnostic)
class PhotoDiagnosticAdmin(admin.ModelAdmin):
    list_display = ['user', 'type','date',]
    list_filter = ['date', 'type']
