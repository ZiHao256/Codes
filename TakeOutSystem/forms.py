from django import forms


class UserForm(forms.Form):
    employee_id = forms.IntegerField(label="employee_id")
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    POSITION_CHOICES=(
        (u'A', u'admin'),
        (u'E', u'employee'),
        (u'S', u'r_staff'),
        (u'M', u'r_manager'),
        (u'D', u'r_delivery')
    )
    name = forms.CharField(label="name", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    employee_id = forms.IntegerField(label="employee_id", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="ensure password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="department", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # position = forms.ChoiceField(label="position", choices=POSITION_CHOICES)
    # email = forms.EmailField(label="e-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # sex = forms.ChoiceField(label='gender', choices=gender)


class ComplainForm(forms.Form):
    TYPE_CHOICES = (
        (u'r_staff', u'餐厅员工'),
        (u'r_delivery', u'餐厅外卖员')
    )
    order_id = forms.IntegerField(label='order_id')
    # type = forms.ChoiceField(label='type', choices=TYPE_CHOICES)
    content = forms.CharField(label='content', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(label='content', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class EmployeeForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label='department', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(label='position', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class AccountForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_id = forms.IntegerField(label='account_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    balance = forms.IntegerField(label='balance', widget=forms.TextInput(attrs={'class': 'form-control'}))
    report_loss = forms.IntegerField(label='report_loss', widget=forms.TextInput(attrs={'class': 'form-control'}))


class MenuForm(forms.Form):
    dish_name = forms.CharField(label='dish_name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    r_staff_id = forms.IntegerField(label='r_staff_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='price')
    # picture = forms.ImageField(label='picture', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stock = forms.IntegerField(label='stock', widget=forms.TextInput(attrs={'class': 'form-control'}))


class LocationForm(forms.Form):
    loc_id = forms.IntegerField(label='loc_id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    building = forms.CharField(label='building', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    floor = forms.IntegerField(label='floor', widget=forms.TextInput(attrs={'class': 'form-control'}))
    room = forms.IntegerField(label='room', widget=forms.TextInput(attrs={'class': 'form-control'}))