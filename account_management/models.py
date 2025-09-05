from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "หมวดหมู่รายรับ"
        verbose_name_plural = "หมวดหมู่รายรับ"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} บาท"
    
    class Meta:
        verbose_name = "รายรับ"
        verbose_name_plural = "รายรับ"

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#000000')  # Hex color
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "หมวดหมู่รายจ่าย"
        verbose_name_plural = "หมวดหมู่รายจ่าย"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    receipt = models.FileField(upload_to='receipts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} บาท"
    
    class Meta:
        verbose_name = "รายจ่าย"
        verbose_name_plural = "รายจ่าย"
