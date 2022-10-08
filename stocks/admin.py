from django.contrib import admin
from .models import Transaction, Item, Category, Client


@admin.register(Transaction, Item, Category, Client)
class RequestAdmin(admin.ModelAdmin):
    transaction_display = [field.name for field in Transaction._meta.get_fields()]
    item_display = [field.name for field in Item._meta.get_fields()]
    category_display = [field.name for field in Category._meta.get_fields()]
    client_display = [field.name for field in Client._meta.get_fields()]