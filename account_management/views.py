from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense

def index(request):
    return render(request, 'index.html')


def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

def expense_add(request):  # ใช้ฟังก์ชันเดียว ลบ add_expense ออก
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            print('บันทึกสำเร็จ')
            return redirect('expense_list')
        else:
            print('Form ไม่ valid:', form.errors)
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