from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Expense CRUD
    path('expense/', views.expense_list, name='expense_list'),
    path('expense/add/', views.expense_add, name='expense_add'),  
    path('expense/edit/<int:id>/', views.expense_edit, name='expense_edit'),
    path('expense/delete/<int:id>/', views.expense_delete, name='expense_delete'),
]
