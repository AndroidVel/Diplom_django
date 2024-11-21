from django.contrib import admin
from .models import User, Product


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'password')
    search_fields = ('email', 'first_name', 'last_name')
    list_per_page = 15

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'price')
    search_fields = 'name'
    list_per_page = 15
