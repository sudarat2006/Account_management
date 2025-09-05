from django import forms

class ExpenseForm(forms.Form):
    description = forms.CharField(label='รายละเอียด', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(label='จำนวนเงิน', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date = forms.DateField(label='วันที่', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
