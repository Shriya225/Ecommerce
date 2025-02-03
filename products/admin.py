from django.contrib import admin
from .models import (Product,Category,Size,ProductImage)
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model=ProductImage
    extra=4

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageInline]
    filter_horizontal=("size",)

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)


