from django import forms


class UserForm(forms.Form):
    employee_id = forms.CharField(label="employee_id", max_length=128)
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)
