from django.db import models


# Create your models here.

class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, default='123456')
    department = models.CharField(max_length=255)


class Balance_account(models.Model):
    employee_id = models.IntegerField(primary_key=False, null=False)
    account_id = models.IntegerField(primary_key=True, null=False)
    open_time = models.DateTimeField(auto_now_add=True, null=False)
    balance = models.FloatField(null=False, default=0.0)
    report_loss = models.IntegerField(null=False, default=0)


class Menu(models.Model):
    dish_name = models.CharField(max_length=255, primary_key=True, null=False)
    price = models.FloatField(null=False, default=0.0)
    picture = models.ImageField()
    stock = models.IntegerField(default=0, null=False)


class Location(models.Model):
    loc_id = models.IntegerField(primary_key=True, null=False)
    building = models.CharField(max_length=255, null=False)
    floor = models.IntegerField(null=False, default=1)
    room = models.CharField(max_length=255, null=False, default=0)


class Order(models.Model):
    STATUS_CHOICES = (
        u'预定状态',
        u'订单开始',
        u'完成支付',
        u'完成备餐',
        u'完成接单',
        u'完成送达'
    )
    METHOD_CHOICES = (
        u'微信支付',
        u'支付宝',
        u'余额支付'
    )
    order_id = models.IntegerField(primary_key=False, null=False)
    date = models.DateTimeField(null=False, auto_now=True)
    order_status = models.CharField(choices=STATUS_CHOICES, null=False, default='预定状态')
    build_time = models.DateTimeField()
    payment_time = models.DateTimeField()
    meal_complete_time = models.DateTimeField()
    accept_order_time = models.DateTimeField()
    delivery_time = models.DateTimeField()
    remark = models.CharField(max_length=256)
    eat_in_store = models.IntegerField()
    specify_delivery_time = models.DateTimeField()
    location = models.IntegerField()
    payment_method = models.IntegerField(choices=METHOD_CHOICES)
    payment_amount = models.FloatField()
    payment_account_id = models.IntegerField()
    payment_id = models.IntegerField()
    customer_id = models.IntegerField()
    r_staff_id = models.IntegerField()
    r_delivery_id = models.IntegerField()


class order_menu(models.Model):
    order_id = models.IntegerField(primary_key=True, null=False)
    dish_name = models.CharField(primary_key=True, max_length=255, null=False)
    amount = models.IntegerField(null=False, default=1)


class Complaint(models.Model):
    order_id = models.IntegerField(primary_key=True, null=False)
    time = models.DateTimeField(null=False)
    type = models.CharField(max_length=255, null=False)
    content = models.CharField(max_length=255, null=False)
    feedback = models.CharField(max_length=255)
