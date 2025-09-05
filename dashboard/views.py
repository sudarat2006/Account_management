# account/views.py

from django.http import HttpResponse

def home_view(request):
    return HttpResponse("ยินดีต้อนรับสู่หน้าแรกของเว็บไซต์")
