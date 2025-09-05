from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')  # ถ้าไม่ล็อกอินจะไปหน้า login
def profile(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
    }
    return render(request, 'profile.html', context)

from django.contrib.auth.decorators import login_required

def profile(request):
    user = request.user
    
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'profile.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ตรวจสอบว่ามี username ซ้ำไหม
        if User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้ไปแล้ว')
        else:
        
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name='',
                last_name=''
            )
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')

    return render(request, 'register.html')