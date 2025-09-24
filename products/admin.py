from django.contrib import admin
from products.models import*
from import_export.admin import ImportExportModelAdmin


admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price', 'stock')


