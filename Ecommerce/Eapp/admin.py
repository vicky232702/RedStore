from django.contrib import admin # type: ignore
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=["id","pname","price","category","description","is_active","pimage"]
    list_filter=["category","is_active"]

admin.site.register(Product,ProductAdmin)