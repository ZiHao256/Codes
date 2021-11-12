from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.utils import timezone

from .models import Employee, Balance_account, Location, Menu, Order, turnover, order_menu


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
                                  balance=0
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
            account.balance += request.GET.get('balance')

            turn_id = request.GET.get('turn_id')
            t = turnover(
                turn_id=turn_id,
                account_id=account_id,
                business_type='充值',
                amount=request.GET.get('balance')
            )
            t.save()

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


@require_http_methods("GET")
def order_dish(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        dish_name = request.GET.get('dish_name')
        menu = Menu.objects.get(dish_name=dish_name)
        amount = menu.price
        r_staff_id = menu.r_staff_id

        order = Order(
            order_id=order_id,
            order_status='订单开始',
            build_time=timezone.localtime(),
            remark=request.GET.get('remark'),
            eat_in_store=request.GET.get('eat_in_store'),
            specify_delivery_time=request.GET.get('specify_delivery_time'),
            location=request.GET.get('location'),
            payment_method='余额支付',
            payment_amount=amount,
            payment_account_id=Balance_account.objects.get(account_id=request.GET.get('payment_account_id')),
            cus_id=request.GET.get('cus_id'),
            r_staff_id=r_staff_id
        )
        order.save()

        order_m = order_menu(
            order_id=order,
            dish_name=dish_name,
            amount=amount
        )
        order_m.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_order(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        response['list'] = json.loads(serializers.serialize("json", order))

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def pay(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)

        if request.GET.get('payment_metohd') is None:
            # 支付方式为余额
            balance = Balance_account.objects.get(account_id=order.payment_account_id)
            balance -= order_menu.objects.get(order_id=order_id).amount
            balance.save()

            turn_id = request.GET.get('turn_id')
            t = turnover(
                turn_id=turn_id,
                account_id=order.cus_id,
                business_type='支付',
                amount=order_menu.objects.get(order_id=order_id).amount
            )
            t.save()

        order.payment_method = request.GET.get('payment_method')
        order.payment_time = timezone.localtime()
        order.order_status = '完成支付'
        order.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def accept_dish_order(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order_m = order_menu.objects.get(order_id=order_id)
        dish = Menu.objects.get(dish_name=order_m.dish_name)
        dish.stock -= 1
        dish.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def request_delivery(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.meal_complete_time = timezone.localtime()
        order.order_status = '完成备餐'

        if order.eat_in_store == '堂食':
            order.order_status = '完成送达'

        order.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def accept_delivery_order(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.r_delivery_id = request.GET.get('r_delivery_id')
        order.accept_order_time = timezone.localtime()
        order.order_status = '完成接单'
        order.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def delivered(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.delivery_time = timezone.localtime()
        order.order_status = '完成送达'
        order.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
