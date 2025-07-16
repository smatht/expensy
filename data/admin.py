from django.contrib import admin
from .models import Categories, Records


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alt_name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'alt_name')
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'date', 'category', 'amount', 'sync', 'source'
    )
    list_display_links = ('id', 'description')
    list_filter = ('category', 'sync', 'source', 'date')
    search_fields = ('description', 'id')
    date_hierarchy = 'date'
    list_per_page = 25
    ordering = ('-date', '-time')

    fieldsets = (
        ('Información básica', {
            'fields': ('id', 'description', 'amount')
        }),
        ('Fechas', {
            'fields': ('date', 'time')
        }),
        ('Clasificación', {
            'fields': ('category', 'source')
        }),
        ('Estado', {
            'fields': ('sync',)
        }),
    )