from django.contrib import admin

# Register your models here.

# admin.py
from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['description']