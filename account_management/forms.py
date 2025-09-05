from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Transaction, Category, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='อีเมล')
    first_name = forms.CharField(max_length=30, required=True, label='ชื่อ')
    last_name = forms.CharField(max_length=30, required=True, label='นามสกุล')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'ชื่อผู้ใช้',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['username'].widget.attrs.update({'placeholder': 'ชื่อผู้ใช้'})
        self.fields['email'].widget.attrs.update({'placeholder': 'อีเมล'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'ชื่อ'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'นามสกุล'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'รหัสผ่าน'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'ยืนยันรหัสผ่าน'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ชื่อผู้ใช้'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'รหัสผ่าน'
        })
        self.fields['username'].label = 'ชื่อผู้ใช้'
        self.fields['password'].label = 'รหัสผ่าน'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'date_of_birth']
        labels = {
            'phone': 'เบอร์โทรศัพท์',
            'date_of_birth': 'วันเกิด',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'ชื่อ',
            'last_name': 'นามสกุล',
            'email': 'อีเมล',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'title', 'description', 'amount', 'date', 'notes']
        labels = {
            'category': 'หมวดหมู่',
            'title': 'ชื่อรายการ',
            'description': 'รายละเอียด',
            'amount': 'จำนวนเงิน',
            'date': 'วันที่',
            'notes': 'หมายเหตุ',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        if user and transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                user=user, 
                type=transaction_type
            )
            
        self.fields['title'].widget.attrs.update({'placeholder': 'ชื่อรายการ'})
        self.fields['description'].widget.attrs.update({'placeholder': 'รายละเอียด (ไม่บังคับ)'})
        self.fields['amount'].widget.attrs.update({'placeholder': '0.00'})
        self.fields['notes'].widget.attrs.update({'placeholder': 'หมายเหตุ (ไม่บังคับ)'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'icon', 'color']
        labels = {
            'name': 'ชื่อหมวดหมู่',
            'type': 'ประเภท',
            'icon': 'ไอคอน',
            'color': 'สี',
        }
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['name'].widget.attrs.update({'placeholder': 'ชื่อหมวดหมู่'})
        self.fields['icon'].widget.attrs.update({'placeholder': '💰'})