from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

class Expense(models.Model):
    description = models.CharField(max_length=200, verbose_name="รายการ")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="จำนวนเงิน")
    date = models.DateField(default=timezone.now, verbose_name="วันที่")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - {self.amount} บาท"

    class Meta:
        ordering = ['-date']