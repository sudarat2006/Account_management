from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/profile/', views.profile_view, name='profile'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
]