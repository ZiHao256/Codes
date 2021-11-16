from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import json
from datetime import datetime
from .forms import UserForm, RegisterForm, ComplainForm, EmployeeForm, AccountForm, MenuForm, LocationForm, OrderForm

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
                    response['error_num'] = 1
                    return JsonResponse(response)
                else:
                    response['msg'] = 'login failed: wrong password'
                    response['error_num'] = 2
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 3

        return JsonResponse(response)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def user_logout(request):
    response = {}
    try:
        if not request.session.get('is_login'):
            response['msg'] = 'have not login'
            response['error_num'] = 0
            return JsonResponse(response)
        request.session.flush()
        response['msg'] = 'logout successfully'
        response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
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


@csrf_exempt
@require_http_methods(["POST"])
def add_one_employee(request):
    response = {}
    try:
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_id = employee_form.cleaned_data['employee_id']
            try:
                Employee.objects.get(employee_id=employee_id)
                response['msg'] = 'employee_id exsited'
                response['error_num'] = 1
            except:

                employee = Employee(employee_id=employee_id,
                                    name=employee_form.cleaned_data['name'],
                                    password=employee_form.cleaned_data['password'],
                                    department=employee_form.cleaned_data['department'],
                                    position=employee_form.cleaned_data['position']
                                    )
                employee.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
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


@csrf_exempt
@require_http_methods(['POST'])
def change_one_employee(request):
    response = {}
    try:
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_id = employee_form.cleaned_data['employee_id']
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                employee.name = employee_form.cleaned_data['name']
                employee.password = employee_form.cleaned_data['password']
                employee.department = employee_form.cleaned_data['department']
                employee.position = employee_form.cleaned_data['position']
                employee.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'employee does not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def add_one_account(request):
    response = {}
    try:
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_id = account_form.cleaned_data['account_id']
            try:
                Balance_account.objects.get(account_id=account_id)
                response['msg'] = 'account existed'
                response['error_num'] = 0
            except:
                account = Balance_account(
                    employee_id=Employee.objects.get(employee_id=account_form.cleaned_data['employee_id']),
                    account_id=account_id,
                    open_time=datetime.now(),
                    balance=account_form.cleaned_data['balance'],
                    report_loss=account_form.cleaned_data['report_loss']
                )
                account.save()
                response['msg'] = 'success'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods(['GET'])
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


@csrf_exempt
@require_http_methods(['POST'])
def change_one_account(request):
    response = {}
    try:
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_id = account_form.cleaned_data['account_id']
            try:
                account = Balance_account.objects.get(account_id=account_id)
                account.balance += account_form.cleaned_data['balance']
                account.report_loss = account_form.cleaned_data['report_loss']
                account.save()
                t = turnover(
                    account_id=account,
                    business_type='充值',
                    time=datetime.now(),
                    amount=account_form.cleaned_data['balance']
                )
                t.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def add_one_location(request):
    response = {}
    try:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            loc_id = location_form.cleaned_data['loc_id']
            try:
                Location.objects.get(loc_id=loc_id)
                response['msg'] = 'loc_id existed'
                response['error_num'] = 0
            except:
                location = Location(
                    loc_id=loc_id,
                    building=location_form.cleaned_data['building'],
                    floor=location_form.cleaned_data['floor'],
                    room=location_form.cleaned_data['room'],
                    time=datetime.now()
                )
                location.save()
                response['msg'] = 'successfully'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods(['GET'])
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


@csrf_exempt
@require_http_methods(['POST'])
def change_one_location(request):
    response = {}
    try:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            try:
                location = Location.objects.get(loc_id=location_form.cleaned_data['loc_id'])
                location.building = location_form.cleaned_data['building']
                location.floor = location_form.cleaned_data['floor']
                location.room = location_form.cleaned_data['room']
                location.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# R_STAFF


@csrf_exempt
@require_http_methods(['POST'])
def add_one_dish(request):
    response = {}
    try:
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            dish_name = menu_form.cleaned_data['dish_name']
            try:
                menu = Menu.objects.get(dish_name=dish_name)
                response['msg'] = 'dish_name existed'
                response['error_num'] = 0
            except:
                menu = Menu(
                    dish_name=dish_name,
                    r_staff_id=Employee.objects.get(employee_id=menu_form.cleaned_data['r_staff_id']),
                    price=menu_form.cleaned_data['price'],
                    # picture = menu_form.cleaned_data['picture'],
                    stock=menu_form.cleaned_data['stock']
                )
                menu.save()
                response['msg'] = 'successfully'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


@require_http_methods(['GET'])
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


@csrf_exempt
@require_http_methods(['POST'])
def change_one_dish(request):
    response = {}
    try:
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            dish_name = menu_form.cleaned_data['dish_name']
            try:
                menu = Menu.objects.get(dish_name=dish_name)
                menu.price = menu_form.cleaned_data['price']
                # menu.picture = menu_form.cleaned_data['picture']
                menu.stock = menu_form.cleaned_data['stock']
                menu.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except:
                response['mas'] = 'dish_name not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
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
        order.meal_complete_time = datetime.now()
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


@csrf_exempt
@require_http_methods(['POST'])
def order_dish(request):
    response = {}
    try:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_id = order_form.cleaned_data['order_id']
            try:
                Order.objects.get(order_id=order_id)
                response['order_id existed']
                response['error_num'] = 0
            except:
                menu = Menu.objects.get(dish_name=order_form.cleaned_data['dish_name'])
                amount = menu.price
                order = Order(
                    order_id=order_id,
                    order_status='预定状态',
                    build_time=datetime.now(),
                    remark=order_form.cleaned_data['remark'],
                    eat_in_store=order_form.cleaned_data['eat_int_store'],
                    specify_delivery_time=order_form.cleaned_data['specify_delivery_time'],
                    location = Location.objects.get(loc_id=order_form.cleaned_data['location']),
                    payment_method=order_form.cleaned_data['payment_method'],
                    payment_amount=amount,
                    payment_account_id=Balance_account.objects.get(account_id=order_form.cleaned_data['payment_account_id']),
                    cus_id=Employee.objects.get(employee_id=order_form.cleaned_data['cus_id']),
                    r_staff_id=Employee.objects.get(employee_id=menu.r_staff_id)
                )
                order.save()

                order_m = order_menu(
                    order_id=order,
                    dish_name=Menu.objects.get(dish_name=menu.dish_name),
                    amount=amount
                )
                order_m.save()

                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods("GET")
def show_order(request):
    response = {}
    try:
        if request.GET.get('order_id') is not None:
            order_id = request.GET.get('order_id')
            order = Order.objects.get(order_id=order_id)
            response['list'] = object_to_json(order)
        else:
            orders = Order.objects.all()
            response['list'] = json.loads(serializers.serialize('json', orders))
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

        if (request.GET.get('payment_metohd') is None) or (request.GET.get('payment_method') == '余额支付'):
            # 支付方式为余额
            Balance = Balance_account.objects.get(account_id=order.payment_account_id_id)
            Balance.balance -= order_menu.objects.get(order_id=order_id).amount
            Balance.save()

            turn_id = request.GET.get('turn_id')
            t = turnover(
                turn_id=turn_id,
                account_id=Balance_account.objects.get(account_id=order.cus_id_id),
                business_type='支付',
                amount=order_menu.objects.get(order_id=order_id).amount
            )
            t.save()

        order.payment_method = request.GET.get('payment_method')
        order.payment_time = datetime.now()
        order.payment_id = t
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
            response['list'] = json.loads(serializers.serialize('json', turnovers))
            response['error_num'] = 0
        else:
            one_turnover = turnover.objects.get(turn_id=request.GET.get('turn_id'))
            response['list'] = object_to_json(one_turnover)
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def complain(request):
    response = {}
    try:
        if request.session.get('is_login', None):
            response['msg'] = 'check content'
            response['error_num'] = 0
            if request.method == 'POST':
                complain_form = ComplainForm(request.POST)
                response['msg'] = 'check'
                response['error_num'] = 1

                if complain_form.is_valid():
                    order_id = complain_form.cleaned_data['order_id']
                    time = datetime.now()
                    # type = complain_form.cleaned_data['type']
                    content = complain_form.cleaned_data['content']
                    feedback = complain_form.cleaned_data['feedback']
                    complaint = Complaint(
                        order_id=Order.objects.get(order_id=order_id),
                        time=time,
                        type='',
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
            response['error_num'] = 5
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 6
    return JsonResponse(response)


# R_DELIVERY


@require_http_methods("GET")
def accept_delivery_order(request):
    response = {}
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(order_id=order_id)
        order.r_delivery_id = request.GET.get('r_delivery_id')
        order.accept_order_time = datetime.now()
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
        order.delivery_time = datetime.now()
        order.order_status = '完成送达'
        order.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# R_MANAGER


@require_http_methods("GET")
def show_complaints(request):
    response = {}
    try:
        complaints = Complaint.objects.all()
        response['list'] = json.loads(serializers.serialize('json', complaints))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def change_one_complaint(request):
    response = {}
    try:
        complain_form = ComplainForm(request.POST)
        response['msg'] = 'check'
        response['error_num'] = 0
        if complain_form.is_valid():
            order_id = complain_form.cleaned_data['order_id']
            # type = complain_form.cleaned_data['type']
            feed_back = complain_form.cleaned_data['feedback']
            complaint = Complaint.objects.get(order_id=order_id)
            complaint.feedback = feed_back
            complaint.save()
            response['msg'] = 'successfully'
            response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)
