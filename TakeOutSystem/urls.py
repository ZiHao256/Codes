from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_one_employee$', add_one_employee, ),
    url(r'show_employee$', show_employee, ),
    url(r'change_one_employee$', change_one_employee,),
]