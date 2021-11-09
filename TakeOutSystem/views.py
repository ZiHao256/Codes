from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Employee, Balance_account, Location, Menu


@require_http_methods(["GET"])
def add_one_employee(request):
    response = {}
    try:
        employee_id = request.GET.get('employee_id')
        employee = Employee(employee_id=employee_id,
                            name=request.GET.get('name'),
                            password=request.GET.get('password'),
                            department=request.GET.get('department'),
                            position=request.GET.get('position')
                            )
        employee.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_employee(request):
    response = {}
    try:
        employees = Employee.objects.all()
        response['list'] = json.loads(serializers.serialize("json", employees))

        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def change_one_employee(request):
    response = {}
    try:
        employee_id = request.GET.get('employee_id')
        employee = Employee.objects.get(employee_id=employee_id)

        if request.GET.get('name') is not None:
            employee.name = request.GET.get('name')
        if request.GET.get('password') is not None:
            employee.password = request.GET.get('password')
        if request.GET.get('department') is not None:
            employee.department = request.GET.get('department')
        if request.GET.get('position') is not None:
            employee.position = request.GET.get('position')
        employee.save()

        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def add_one_account(request):
    response = {}
    try:
        employee_id = Employee.objects.get(employee_id=request.GET.get('employee_id'))
        account = Balance_account(employee_id=employee_id,
                                  account_id=request.GET.get('account_id'),
                                  balance=request.GET.get('balance')
                                  )
        account.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_account(request):
    response = {}
    try:
        account = Balance_account.objects.all()
        response['list'] = json.loads(serializers.serialize("json", account))

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def change_one_account(request):
    response = {}
    try:
        account_id = request.GET.get('account_id')
        account = Balance_account.objects.get(account_id=account_id)
        if request.GET.get('balance') is not None:
            account.balance = request.GET.get('balance')
        if request.GET.get('report_loss') is not None:
            account.report_loss = request.GET.get('report_loss')
        account.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def add_one_location(request):
    response = {}
    try:
        loc_id = request.GET.get('loc_id')
        location = Location(
            loc_id=loc_id,
            building=request.GET.get('building'),
            floor=request.GET.get('floor'),
            room=request.GET.get('room')
        )
        location.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_location(request):
    response = {}
    try:
        location = Location.objects.all()
        response['list'] = json.loads((serializers.serialize("json", location)))

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def change_one_location(request):
    response = {}
    try:
        loc_id = request.GET.get('loc_id')
        location = Location.objects.get(loc_id=loc_id)
        if request.GET.get('building') is not None:
            location.building = request.GET.get('building')
        if request.GET.get('floor') is not None:
            location.floor = request.GET.get('floor')
        if request.GET.get('room') is not None:
            location.room = request.GET.get('room')
        location.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def add_one_dish(request):
    response = {}
    try:
        dish_name = request.GET.get('dish_name')
        r_staff_id = Employee.objects.get(employee_id=request.GET.get('r_staff_id'))
        dish = Menu(
            dish_name=dish_name,
            r_staff_id=r_staff_id,
            price=request.GET.get('price'),
            picture=request.GET.get('picture'),
            stock=request.GET.get('stock')
        )
        dish.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_dish(request):
    response = {}
    try:
        dish = Menu.objects.all()
        response['list'] = json.loads(serializers.serialize("json", dish))

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def change_one_dish(request):
    response = {}
    try:
        dish_name = request.GET.get('dish_name')
        r_staff_id = request.GET.get('r_staff_id')
        dish = Menu.objects.get(dish_name=dish_name)
        if request.GET.get('price') is not None:
            dish.price = request.GET.get('price')
        if request.GET.get('picture') is not None:
            dish.picture = request.GET.get('picture')
        if request.GET.get('stock'):
            dish.stock = request.GET.get('stock')
        dish.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
