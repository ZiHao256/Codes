from django import forms


class UserForm(forms.Form):
    employee_id = forms.IntegerField(label="employee_id")
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput)
