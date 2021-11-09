from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Employee


@require_http_methods(["GET"])
def add_one_employee(request):
    response = {}
    try:
        employee = Employee(employee_id=request.GET.get('employee_id'),
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
        employees = Employee.objects.filter(employee_id=request.GET.get('employee_id'))
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




