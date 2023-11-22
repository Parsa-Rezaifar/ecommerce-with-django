from django.contrib import admin
from . models import Category,Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)
    prepopulated_fields = {'category_slug':('category_name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_availability','created','updated',)
    search_fields = ('product_name',)
    list_filter = ('related_category','created','updated',)
    raw_id_fields = ('related_category',)
    prepopulated_fields = {'product_slug':('product_name',)}