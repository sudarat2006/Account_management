from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Category(models.Model):
    CATEGORY_TYPES = (
        ('income', 'รายรับ'),
        ('expense', 'รายจ่าย'),
    )
    
    name = models.CharField(max_length=100, verbose_name='ชื่อหมวดหมู่')
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, verbose_name='ประเภท')
    icon = models.CharField(max_length=50, default='💰', verbose_name='ไอคอน')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='สี')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ผู้ใช้')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'หมวดหมู่'
        verbose_name_plural = 'หมวดหมู่'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.icon} {self.name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'รายรับ'),
        ('expense', 'รายจ่าย'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ผู้ใช้')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='หมวดหมู่')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name='ประเภท')
    title = models.CharField(max_length=200, verbose_name='ชื่อรายการ')
    description = models.TextField(blank=True, null=True, verbose_name='รายละเอียด')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='จำนวนเงิน')
    date = models.DateField(verbose_name='วันที่')
    notes = models.TextField(blank=True, null=True, verbose_name='หมายเหตุ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'รายการ'
        verbose_name_plural = 'รายการ'
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.amount:,.2f} บาท"
    
    @property
    def is_income(self):
        return self.type == 'income'
    
    @property
    def is_expense(self):
        return self.type == 'expense'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ผู้ใช้')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='เบอร์โทรศัพท์')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='วันเกิด')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'โปรไฟล์ผู้ใช้'
        verbose_name_plural = 'โปรไฟล์ผู้ใช้'
        
    def __str__(self):
        return f"โปรไฟล์ของ {self.user.username}"