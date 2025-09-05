from django.shortcuts import render, redirect
from .forms import ExpenseForm

def index(request):
    return render(request, 'index.html')

def expense_list(request):
    return render(request, 'expense_list.html')

def expense_edit(request, id):
    return render(request, 'expense_edit.html', {'id': id})

def expense_delete(request, id):
    return redirect('expense_list')

def expense_add(request):
    return render('expenses/expense_add.html')

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # บันทึกข้อมูลรายจ่าย (ตัวอย่างนี้ยังไม่บันทึกลงฐานข้อมูล)
            # สามารถเพิ่มการบันทึกลง model ได้ภายหลัง
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'expense_add.html', {'form': form})

