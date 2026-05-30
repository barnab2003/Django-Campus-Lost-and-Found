# items/admin.py
from django.contrib import admin
from .models import Item

# This registers the Item model with the admin site
admin.site.register(Item)