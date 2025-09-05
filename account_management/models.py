from django.db import models
from django.core.exceptions import ValidationError

class IncomeCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Income(models.Model):
	category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
	description = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	date = models.DateField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.description} ({self.amount})"

	def clean(self):
		errors = {}
		if self.amount is None:
			errors['amount'] = 'Amount is required.'
		elif self.amount <= 0:
			errors['amount'] = 'Amount must be greater than zero.'
		elif self.amount > 1000000:
			errors['amount'] = 'Amount is unrealistically high.'
		if errors:
			raise ValidationError(errors)

# Create your models here.
