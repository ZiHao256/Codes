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
    type = forms.ChoiceField(label='type', choices=TYPE_CHOICES)
    content = forms.CharField(label='content', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    feedback = forms.CharField(label='content', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))