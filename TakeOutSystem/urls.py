from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_employee$', add_employee, ),
    url(r'show_employee$', show_employee, ),
]