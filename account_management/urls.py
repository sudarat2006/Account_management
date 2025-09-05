from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/monthly/<int:year>/<int:month>/', views.monthly_report, name='monthly_report_detail'),
    path('reports/yearly/', views.yearly_report, name='yearly_report'),
    path('reports/yearly/<int:year>/', views.yearly_report, name='yearly_report_detail'),
    path('summary/', views.summary, name='summary'),
]