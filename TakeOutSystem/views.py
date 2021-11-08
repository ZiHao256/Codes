from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json

from .models import Employee


@require_http_methods(["GET"])
def add_employee(request):
    response = {}
    try:
        employee = Employee(employee_id=request.GET.get('employee_id'))
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
        employees = Employee.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", employees))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
