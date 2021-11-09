from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'add_one_employee$', add_one_employee, ),
    url(r'show_employee$', show_employee,),
    url(r'change_one_employee$', change_one_employee,),
    url(r'add_one_account$', add_one_account),
    url(r'show_account$', show_account),
    url(r'change_one_account$', change_one_account),
    url(r'add_one_location$', add_one_location),
    url(r'show_location$', show_location),
    url(r'change_one_location$', change_one_location),
    url(r'add_one_dish$', add_one_dish),
    url(r'show_dish$', show_dish),
    url(r'change_one_dish$', change_one_dish),

]