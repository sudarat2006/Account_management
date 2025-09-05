from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Income, Expense, IncomeCategory, ExpenseCategory

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    """หน้า Dashboard หลัก"""
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # สรุปข้อมูลเดือนปัจจุบัน
    monthly_income = Income.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_expense = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_balance = monthly_income - monthly_expense
    
    # สรุปข้อมูลปีปัจจุบัน
    yearly_income = Income.objects.filter(
        user=request.user,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    yearly_expense = Expense.objects.filter(
        user=request.user,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    yearly_balance = yearly_income - yearly_expense
    
    # รายการรายรับ-รายจ่ายล่าสุด
    recent_income = Income.objects.filter(user=request.user).order_by('-date')[:5]
    recent_expense = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    
    context = {
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_balance': monthly_balance,
        'yearly_income': yearly_income,
        'yearly_expense': yearly_expense,
        'yearly_balance': yearly_balance,
        'recent_income': recent_income,
        'recent_expense': recent_expense,
        'current_month': current_month,
        'current_year': current_year,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def monthly_report(request, year=None, month=None):
    """หน้ารายงานรายเดือน"""
    if not year or not month:
        current_date = timezone.now()
        year = current_date.year
        month = current_date.month
    
    # สรุปข้อมูลรายเดือน
    monthly_income = Income.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_expense = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # รายการรายรับ-รายจ่ายรายเดือน
    income_list = Income.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).order_by('-date')
    
    expense_list = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).order_by('-date')
    
    # สรุปตามหมวดหมู่
    income_by_category = Income.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    expense_by_category = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    context = {
        'year': year,
        'month': month,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'monthly_balance': monthly_income - monthly_expense,
        'income_list': income_list,
        'expense_list': expense_list,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
    }
    
    return render(request, 'reports/monthly.html', context)

@login_required
def yearly_report(request, year=None):
    """หน้ารายงานรายปี"""
    if not year:
        year = timezone.now().year
    
    # สรุปข้อมูลรายปี
    yearly_income = Income.objects.filter(
        user=request.user,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    yearly_expense = Expense.objects.filter(
        user=request.user,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # สรุปรายเดือน
    monthly_data = []
    for month in range(1, 13):
        month_income = Income.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        month_expense = Expense.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_data.append({
            'month': month,
            'income': month_income,
            'expense': month_expense,
            'balance': month_income - month_expense
        })
    
    # สรุปตามหมวดหมู่
    income_by_category = Income.objects.filter(
        user=request.user,
        date__year=year
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    expense_by_category = Expense.objects.filter(
        user=request.user,
        date__year=year
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    context = {
        'year': year,
        'yearly_income': yearly_income,
        'yearly_expense': yearly_expense,
        'yearly_balance': yearly_income - yearly_expense,
        'monthly_data': monthly_data,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
    }
    
    return render(request, 'reports/yearly.html', context)

@login_required
def summary(request):
    """หน้าสรุปยอดรวม"""
    current_date = timezone.now()
    
    # สรุปข้อมูลทั้งหมด
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_balance = total_income - total_expense
    
    # สรุปตามหมวดหมู่
    income_by_category = Income.objects.filter(user=request.user).values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    expense_by_category = Expense.objects.filter(user=request.user).values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # สถิติเพิ่มเติม
    total_income_count = Income.objects.filter(user=request.user).count()
    total_expense_count = Expense.objects.filter(user=request.user).count()
    
    # รายการรายรับ-รายจ่ายล่าสุด
    recent_income = Income.objects.filter(user=request.user).order_by('-date')[:10]
    recent_expense = Expense.objects.filter(user=request.user).order_by('-date')[:10]
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_balance': total_balance,
        'total_income_count': total_income_count,
        'total_expense_count': total_expense_count,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
        'recent_income': recent_income,
        'recent_expense': recent_expense,
    }
    
    return render(request, 'summary.html', context)