# โปรเจครายรับรายจ่าย (Expense Tracker)

## ภาพรวมโปรเจค
ระบบจัดการรายรับรายจ่ายแบบง่าย สำหรับทีม 4 คน ใช้ Django Framework

## โครงสร้าง Git Branch และการแบ่งงาน

### 🌟 Branch: `main`
**ผู้รับผิดชอบ**: ทีมลีดเดอร์
**หน้าที่**: 
- จัดการ Branch หลักและ Merge การทำงานของทีม
- ตั้งค่าโปรเจคเริ่มต้น
- สร้าง Base Template และ Static Files

**ระบบที่ต้องมี**:
- Django Project Setup
- Base Template (base.html)
- Static Files (CSS, JS พื้นฐาน)
- Settings Configuration
- Requirements.txt

---

### 👤 Branch: `auth-system`
**ผู้รับผิดชอบ**: Developer A
**หน้าที่**: ระบบผู้ใช้งานและการยืนยันตัวตน

**หน้าเว็บที่ต้องสร้าง**:
- หน้า Login (`/login/`)
- หน้า Register (`/register/`)
- หน้า Profile (`/profile/`)
- หน้า Logout

**ระบบที่ต้องมี**:
- User Model (ใช้ Django Built-in หรือ Custom)
- Authentication Views
- User Registration Form
- User Profile Management
- Login/Logout Functionality
- Password Reset (Optional)

**Models**:
```python
# ใช้ Django User Model หรือขยายเพิ่ม
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
```

---

### 💰 Branch: `income-management`
**ผู้รับผิดชอบ**: Developer B
**หน้าที่**: จัดการข้อมูลรายรับ

**หน้าเว็บที่ต้องสร้าง**:
- หน้ารายการรายรับ (`/income/`)
- หน้าเพิ่มรายรับ (`/income/add/`)
- หน้าแก้ไขรายรับ (`/income/edit/<id>/`)
- หน้าลบรายรับ (`/income/delete/<id>/`)

**ระบบที่ต้องมี**:
- Income Model และ Database
- CRUD Operations สำหรับรายรับ
- Income Categories
- Date/Time Tracking
- Amount Validation

**Models**:
```python
class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### 💸 Branch: `expense-management`
**ผู้รับผิดชอบ**: Developer C
**หน้าที่**: จัดการข้อมูลรายจ่าย

**หน้าเว็บที่ต้องสร้าง**:
- หน้ารายการรายจ่าย (`/expense/`)
- หน้าเพิ่มรายจ่าย (`/expense/add/`)
- หน้าแก้ไขรายจ่าย (`/expense/edit/<id>/`)
- หน้าลบรายจ่าย (`/expense/delete/<id>/`)

**ระบบที่ต้องมี**:
- Expense Model และ Database
- CRUD Operations สำหรับรายจ่าย
- Expense Categories
- Receipt Upload (Optional)
- Date/Time Tracking
- Amount Validation

**Models**:
```python
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#000000')  # Hex color

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    receipt = models.ImageField(upload_to='receipts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### 📊 Branch: `dashboard-reports`
**ผู้รับผิดชอบ**: Developer D
**หน้าที่**: หน้าแดชบอร์ดและรายงาน

**หน้าเว็บที่ต้องสร้าง**:
- หน้า Dashboard หลัก (`/dashboard/` หรือ `/`)
- หน้ารายงานรายเดือน (`/reports/monthly/`)
- หน้ารายงานรายปี (`/reports/yearly/`)
- หน้าสรุปยอด (`/summary/`)

**ระบบที่ต้องมี**:
- Dashboard with Summary Cards
- Charts และ Graphs (ใช้ Chart.js หรือ similar)
- Monthly/Yearly Reports
- Income vs Expense Comparison
- Category-wise Analysis
- Export to PDF/Excel (Optional)

**Views ที่ต้องมี**:
```python
# Dashboard calculations
def get_monthly_summary(user, month, year):
    total_income = Income.objects.filter(user=user, date__month=month, date__year=year).aggregate(Sum('amount'))
    total_expense = Expense.objects.filter(user=user, date__month=month, date__year=year).aggregate(Sum('amount'))
    return {
        'income': total_income,
        'expense': total_expense,
        'balance': total_income - total_expense
    }
```

---

## 📋 หน้าเว็บทั้งหมดในระบบ

### หน้าหลัก
- `/` - หน้าแรก/แดชบอร์ด
- `/summary/` - สรุปยอดรวม
- `/about/` - เกี่ยวกับระบบ

### จัดการรายรับ
- `/income/` - รายการรายรับ
- `/income/add/` - เพิ่มรายรับ
- `/income/edit/<id>/` - แก้ไขรายรับ
- `/income/delete/<id>/` - ลบรายรับ

### จัดการรายจ่าย  
- `/expense/` - รายการรายจ่าย
- `/expense/add/` - เพิ่มรายจ่าย
- `/expense/edit/<id>/` - แก้ไขรายจ่าย
- `/expense/delete/<id>/` - ลบรายจ่าย

### รายงาน
- `/reports/monthly/` - รายงานรายเดือน
- `/reports/yearly/` - รายงานรายปี
- `/reports/category/` - รายงานแยกตามหมวดหมู่

---

นางสาว สุดารัตน์ วรรณทวี 6712732127
นางสาว ปัทมาภรณ์ สมอเขียว 6712732122
