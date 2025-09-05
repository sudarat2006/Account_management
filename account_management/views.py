from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from datetime import datetime, date
from django.contrib.auth.models import User
from .models import Transaction, Category, UserProfile
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, 
    UserProfileForm, UserUpdateForm, TransactionForm, CategoryForm
)

# Authentication Views
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            # Create default categories
            default_income_categories = [
                {'name': 'เงินเดือน', 'icon': '💰', 'color': '#28a745'},
                {'name': 'โบนัส', 'icon': '🎁', 'color': '#17a2b8'},
                {'name': 'รายได้พิเศษ', 'icon': '💵', 'color': '#ffc107'},
            ]
            default_expense_categories = [
                {'name': 'อาหาร', 'icon': '🍽️', 'color': '#fd7e14'},
                {'name': 'เดินทาง', 'icon': '🚗', 'color': '#6f42c1'},
                {'name': 'ค่าใช้จ่ายส่วนตัว', 'icon': '🛒', 'color': '#e83e8c'},
                {'name': 'ค่าบ้าน', 'icon': '🏠', 'color': '#20c997'},
            ]
            
            for cat in default_income_categories:
                Category.objects.create(
                    user=user, type='income', **cat
                )
            for cat in default_expense_categories:
                Category.objects.create(
                    user=user, type='expense', **cat
                )
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'สร้างบัญชีผู้ใช้ {username} เรียบร้อยแล้ว')
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'อัปเดตข้อมูลโปรไฟล์เรียบร้อยแล้ว')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'auth/profile.html', context)

# Dashboard View
@login_required
def dashboard_view(request):
    current_month = date.today().month
    current_year = date.today().year
    
    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    )
    
    total_income = transactions.filter(type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(
        total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    
    recent_transactions = Transaction.objects.filter(user=request.user)[:10]
    
    # Monthly data for chart
    monthly_income = []
    monthly_expense = []
    for month in range(1, 13):
        income = Transaction.objects.filter(
            user=request.user,
            type='income',
            date__month=month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense = Transaction.objects.filter(
            user=request.user,
            type='expense',
            date__month=month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_income.append(float(income))
        monthly_expense.append(float(expense))
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'current_month': current_month,
        'current_year': current_year,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
    }
    return render(request, 'dashboard/index.html', context)

# Transaction Views
@login_required
def transaction_list(request):
    transaction_type = request.GET.get('type', 'all')
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    transactions = Transaction.objects.filter(user=request.user)
    
    if transaction_type and transaction_type != 'all':
        transactions = transactions.filter(type=transaction_type)
    
    if search:
        transactions = transactions.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(user=request.user)
    
    # Calculate totals
    total_income = transactions.filter(type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(
        total=Sum('amount'))['total'] or 0
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'transaction_type': transaction_type,
        'search': search,
        'selected_category': category_id,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
    }
    return render(request, 'transactions/list.html', context)

@login_required
def transaction_add(request):
    transaction_type = request.GET.get('type', 'expense')
    
    if request.method == 'POST':
        form = TransactionForm(
            request.POST, 
            user=request.user, 
            transaction_type=transaction_type
        )
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.type = transaction_type
            transaction.save()
            messages.success(request, f'เพิ่ม{transaction.get_type_display()}เรียบร้อยแล้ว')
            return redirect('transaction_list')
    else:
        form = TransactionForm(
            user=request.user, 
            transaction_type=transaction_type
        )
    
    context = {
        'form': form,
        'transaction_type': transaction_type,
        'title': f'เพิ่ม{dict(Transaction.TRANSACTION_TYPES)[transaction_type]}',
    }
    return render(request, 'transactions/add.html', context)

@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(
            request.POST, 
            instance=transaction,
            user=request.user,
            transaction_type=transaction.type
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขรายการเรียบร้อยแล้ว')
            return redirect('transaction_list')
    else:
        form = TransactionForm(
            instance=transaction,
            user=request.user,
            transaction_type=transaction.type
        )
    
    context = {
        'form': form,
        'transaction': transaction,
        'title': f'แก้ไข{transaction.get_type_display()}',
    }
    return render(request, 'transactions/edit.html', context)

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'ลบรายการเรียบร้อยแล้ว')
        return redirect('transaction_list')
    
    return render(request, 'transactions/delete.html', {'transaction': transaction})