from django.contrib import admin
from .models import Transaction, Category, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'icon', 'user', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'amount', 'category', 'user', 'date']
    list_filter = ['type', 'category', 'date', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']