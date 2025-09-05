from django.contrib import admin
from .models import Income, Expense, IncomeCategory, ExpenseCategory

# Register your models here.

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color']
    search_fields = ['name']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'date', 'description']
    list_filter = ['category', 'date', 'user']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'date', 'description']
    list_filter = ['category', 'date', 'user']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'
