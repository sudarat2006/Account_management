

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.contrib import messages
from django.urls import reverse
from .forms import ExpenseForm
from .models import Expense, Income, IncomeCategory


def index(request):
    return render(request, 'index.html')



def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expense_add.html', {'form': form})


def expense_edit(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_edit.html', {'form': form, 'expense': expense})


def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expense_delete.html', {'expense': expense})




def monthly_report(request):
    return HttpResponse("<h1>Monthly Report</h1>")

def yearly_report(request):
    return HttpResponse("<h1>Yearly Report</h1>")

def summary(request):
    return HttpResponse("<h1>Summary Page</h1>")

# --- Income CRUD Views ---
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'description', 'amount']

def income_list(request):
    incomes = Income.objects.select_related('category').order_by('-date')
    return render(request, 'income_list.html', {'incomes': incomes})

def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มรายรับสำเร็จ')
            return redirect(reverse('income_list'))
    else:
        form = IncomeForm()
    return render(request, 'income_form.html', {'form': form, 'action': 'เพิ่มรายรับ'})

def income_edit(request, id):
    income = get_object_or_404(Income, pk=id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขรายรับสำเร็จ')
            return redirect(reverse('income_list'))
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income_form.html', {'form': form, 'action': 'แก้ไขรายรับ'})

def income_delete(request, id):
    income = get_object_or_404(Income, pk=id)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'ลบรายรับสำเร็จ')
        return redirect(reverse('income_list'))
    return render(request, 'income_confirm_delete.html', {'income': income})

