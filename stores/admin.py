from django.contrib import admin
from .models import *


# @admin.register(Category, Item, Bundle, Listing)
class RequestAdmin(admin.ModelAdmin):
    ...
    # Cate = [field.name for field in Category._meta.get_fields()]
    # Item = [field.name for field in Item._meta.get_fields()]
    # Bundle = [field.name for field in Bundle._meta.get_fields()]
    # List = [field.name for field in Listing._meta.get_fields()]
