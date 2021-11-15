from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import json
from django.utils import timezone
from datetime import datetime
from .forms import UserForm, RegisterForm, ComplainForm

from .models import Employee, Balance_account, Location, Menu, Order, turnover, order_menu, Complaint


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


# USER


@csrf_exempt
@require_http_methods("POST")
def user_login(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'this employee has logined'
        response['error_num'] = 0
        return JsonResponse(response)

    if request.method == 'POST':
        login_form = UserForm(request.POST)
        response['msg'] = 'please check '

        if login_form.is_valid():
            employee_id = login_form.cleaned_data['employee_id']
            password = login_form.cleaned_data['password']
            try:
                user = Employee.objects.get(employee_id=employee_id)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['employee_id'] = user.employee_id
                    request.session['name'] = user.name
                    request.session['position'] = user.position
                    response['msg'] = 'login successfully'
                    response['error_num'] = 0
                    return JsonResponse(response)
                else:
                    response['msg'] = 'login failed: wrong password'
                    response['error_num'] = 0
            except:
                response['msg'] = 'do not have this employee'
                response['error_num'] = 1

        return JsonResponse(response)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def user_logout(request):
    response = {}
    if not request.session.get('is_login'):
        response['msg'] = 'have not login'
        response['error_num'] = 0
        return JsonResponse(response)
    request.session.flush()

    response['msg'] = 'logout successfully'
    response['error_num'] = 0
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def user_register(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'you have logined!'
        response['error_num'] = 0
        return JsonResponse(response)

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        response['msg'] = 'please check content!'
        response['error_num'] = 1

        if register_form.is_valid():
            employee_id = register_form.cleaned_data['employee_id']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            department = register_form.cleaned_data['department']
            # position = register_form.cleaned_data['position']

            if password1 != password2:
                response['msg'] = 'password is not consistent！'
                return JsonResponse(response)
            else:
                same_employee = {}
                try:
                    same_employee = Employee.objects.get(employee_id=employee_id)
                    response['msg'] = 'this employee_id has existed！'
                    response['error_num'] = 2
                    return JsonResponse(response)

                except Exception as e:

                    new_employee = Employee(
                        employee_id=employee_id,
                        name=name,
                        password=password1,
                        department=department,
                        # position=position
                    )
                    response['msg'] = 'register successfully!'
                    response['error_num'] = 3
                    new_employee.save()
                    return JsonResponse(response)
        return JsonResponse(response)
    return JsonResponse(response)


# ADMINISTER


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
def show_one_employee(request):
    response = {}
    try:
        employee = {}
        if request.GET.get('employee_id') is not None:
            employee = Employee.objects.get(employee_id=request.GET.get('employee_id'))
            response['list'] = object_to_json(employee)
        else:
            employee = Employee.objects.all()
            response['list'] = json.loads(serializers.serialize("json", employee))
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
        employee_id = Employee.objects.get(employee_id=int(request.GET.get('employee_id')))
        account = Balance_account(employee_id=employee_id,
                                  account_id=request.GET.get('account_id'),
                                  open_time=datetime.now(),
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
        account_id = int(request.GET.get('account_id'))
        account = Balance_account.objects.get(account_id=account_id)
        if request.GET.get('balance') is not None:
            account.balance += int(request.GET.get('balance'))

            turn_id = request.GET.get('turn_id')
            t = turnover(
                turn_id=turn_id,
                account_id=account,
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


# R_STAFF


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


# EMPLOYEE


@require_http_methods("GET")
def order_dish(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        dish_name = request.GET.get('dish_name')
        menu = Menu.objects.get(dish_name=dish_name)
        amount = menu.price
        r_staff_id = menu.r_staff_id

        request.session['order_id'] = order_id

        order = Order(
            order_id=order_id,
            order_status='订单开始',
            build_time=datetime.now(),
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
        order_id = request.session.get('order_id', None)
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
def show_turnovers(request):
    response = {}
    try:
        if request.GET.get('turn_id') is None:
            turnovers = turnover.objects.all()
            response['list'] = json.loads(serializers.serialize('json',turnovers))
            response['error_num'] = 0
        else:
            one_turnover = turnover.objects.get(turn_id=request.GET.get('turn_id'))
            response['list'] = object_to_json(one_turnover)
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)

@require_http_methods("POST")
def complain(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'check content'
        response['error_num'] = 0
        if request.method == 'POST':
            complain_form = ComplainForm(request.POST)
            response['msg'] = 'check'
            response['error_num'] = 1

            if complain_form.is_valid():
                order_id = request.session.get('order_id')
                time = timezone.localtime()
                type = complain_form.cleaned_data['type']
                content = complain_form.cleaned_data['content']
                feedback = '(空)'
                complaint = Complaint(
                    order_id=order_id,
                    time=time,
                    type=type,
                    content=content,
                    feedback=feedback
                )
                complaint.save()
                response['msg'] = 'complain successfully!'
                response['error_num'] = 2

            else:
                response['msg'] = 'form is not valid'
                response['error_num'] = 3
        else:
            response['msg'] = 'GET'
            response['error_num'] = 4

        return JsonResponse(response)
    else:
        response['msg'] = 'you must login!'
        response['error_num'] = 1
        return JsonResponse(response)


# R_DELIVERY


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
