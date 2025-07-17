from django.contrib import admin
from .models import Categories, Records

# Admin dashboard title configuration
admin.site.site_header = "Expensy - Panel de Administración"
admin.site.site_title = "Expensy Admin"
admin.site.index_title = "Bienvenido al panel de administración de Expensy"


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
        'description', 'date', 'category', 'amount', 'source'
    )
    list_display_links = ('description',)
    list_filter = ('category', 'source', 'date')
    search_fields = ('description', 'id')
    date_hierarchy = 'date'
    list_per_page = 25
    ordering = ('-date',)

    fieldsets = (
        ('Información básica', {
            'fields': ('description', 'amount')
        }),
        ('Fechas', {
            'fields': ('date',)
        }),
        ('Clasificación', {
            'fields': ('category', 'source')
        }),
    )
