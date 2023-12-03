import os

import openpyxl
from django.shortcuts import render
from django.http import JsonResponse
import json
from datetime import date

from Restaurant_Management import settings
from appSite.models import User
from appSite.models import Customer
from appSite.models import Worker
from appSite.models import Menu
from appSite.models import FoodTable
from appSite.models import Order
from appSite.models import Menu_Order
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
import hashlib


# Create your views here.

def login(request):
    """实现登录功能"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        users = User.objects.filter(account=data['username'], password=data['password'], authority=data['radio'])
        if not users:
            return JsonResponse({"code": 2})
        else:
            user = users[0].account
            return JsonResponse({"code": 1, "username": user})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取用户数据异常，具体错误：" + str(e)})


def modify_password(request):
    """修改密码"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_user = User.objects.get(account=data['username'])
        # 修改
        obj_user.password = data['password']
        obj_user.save()
        return JsonResponse({"code": 1})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "修改到数据库异常，具体错误：" + str(e)})


def is_exist_Username(request):
    """查询用户名是否存在"""
    data = json.loads(request.body.decode('utf-8'))
    obj_user = User.objects.filter(account=data['username'])
    try:
        if obj_user.count() == 0:
            return JsonResponse({'code': 1, 'exist': False})
        else:
            return JsonResponse({'code': 1, 'exist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验用户名失败，原因：{e}" + str(e)})


def register(request):
    """实现注册功能"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_new_user = User(account=data['username'], password=data['password'], authority='1')
        # 执行添加
        obj_new_user.save()
        return JsonResponse({"code": 1})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "注册到数据库异常，具体错误：" + str(e)})


def get_customer(request):
    """获取所有顾客信息"""
    try:
        # 使用ORM获取所有顾客信息
        obj_customer = Customer.objects.all().values()
        # 把结果转为List
        customer = list(obj_customer)
        return JsonResponse({"code": 1, "data": customer})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取顾客信息异常，具体错误：" + str(e)})


def query_customer(request):
    """查询顾客信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型（'inputstr'）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的顾客信息，并把对象转为字典格式
        obj_customer = Customer.objects.filter(
            Q(C_account__icontains=data['inputstr']) | Q(C_name__icontains=data['inputstr'])
            | Q(C_sex__icontains=data['inputstr']) | Q(C_birth__icontains=data['inputstr'])
            | Q(C_phone__icontains=data['inputstr'])).values()
        customer_list = []
        for customer in obj_customer:
            today = date.today()
            age = today.year - customer['C_birth'].year - (
                    (today.month, today.day) < (customer['C_birth'].month, customer['C_birth'].day))
            customer['C_age'] = age
            customer_list.append(customer)
        return JsonResponse({"code": 1, "data": customer_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "查询顾客信息异常，具体错误：" + str(e)})


def get_worker(request):
    """获取所有员工信息"""
    try:
        # 使用ORM获取所有员工信息
        obj_worker = Worker.objects.all().values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                    (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            worker_list.append(worker)
        return JsonResponse({"code": 1, "data": worker_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取员工信息异常，具体错误：" + str(e)})


def query_worker(request):
    """查询员工信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型（'inputstr'）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_worker = Worker.objects.filter(
            Q(W_id__icontains=data['inputstr']) | Q(W_name__icontains=data['inputstr'])
            | Q(W_sex__icontains=data['inputstr']) | Q(W_birth__icontains=data['inputstr'])
            | Q(W_job__icontains=data['inputstr']) | Q(W_phone__icontains=data['inputstr'])
            | Q(W_addr__icontains=data['inputstr'])).values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                    (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            worker_list.append(worker)
        return JsonResponse({"code": 1, "data": worker_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "查询员工信息异常，具体错误：" + str(e)})


def is_exist_W_id(request):
    """查询员工工号是否存在"""
    # 接收传递过来的工号
    data = json.loads(request.body.decode('utf-8'))
    obj_worker = Worker.objects.filter(W_id=data['W_id'])
    try:
        if obj_worker.count() == 0:
            return JsonResponse({'code': 1, 'exist': False})
        else:
            return JsonResponse({'code': 1, 'exist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验工号失败，原因：{e}" + str(e)})


def add_worker(request):
    """添加员工信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_new_worker = Worker(W_id=data['W_id'], W_name=data['W_name'], W_sex=data['W_sex'],
                                W_birth=data['W_birth'], W_job=data['W_job'], W_phone=data['W_phone'],
                                W_salary=data['W_salary'], W_addr=data['W_addr'])
        # 执行添加
        obj_new_worker.save()
        # 使用ORM获取所有员工信息
        obj_worker = Worker.objects.all().values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                    (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            worker_list.append(worker)
        return JsonResponse({"code": 1, "data": worker_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "添加到数据库异常，具体错误：" + str(e)})


def update_worker(request):
    """修改员工信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_worker = Worker.objects.get(W_id=data['W_id'])
        # 依次修改
        obj_worker.W_name = data['W_name']
        obj_worker.W_sex = data['W_sex']
        obj_worker.W_birth = data['W_birth']
        obj_worker.W_job = data['W_job']
        obj_worker.W_phone = data['W_phone']
        obj_worker.W_salary = data['W_salary']
        obj_worker.W_addr = data['W_addr']
        obj_worker.save()
        # 使用ORM获取所有员工信息
        obj_worker = Worker.objects.all().values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                    (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            worker_list.append(worker)
        return JsonResponse({"code": 1, "data": worker_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "修改到数据库异常，具体错误：" + str(e)})


def delete_worker(request):
    """删除员工信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_worker = Worker.objects.get(W_id=data['W_id'])
        # 执行删除
        obj_worker.delete()
        # 使用ORM获取所有员工信息
        obj_worker = Worker.objects.all().values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                    (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            worker_list.append(worker)
        return JsonResponse({"code": 1, "data": worker_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "删除到数据库异常，具体错误：" + str(e)})


def get_dish(request):
    """获取所有菜品信息"""
    try:
        # 使用ORM获取所有菜品信息
        obj_menu = Menu.objects.all().values()
        # 把结果转为List
        menu = list(obj_menu)
        return JsonResponse({"code": 1, "data": menu})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取菜品信息异常，具体错误：" + str(e)})


def query_dish(request):
    """查询菜品信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型（'inputstr'）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的菜品信息，并把对象转为字典格式
        obj_dish = Menu.objects.filter(
            Q(M_id__icontains=data['inputstr']) | Q(M_name__icontains=data['inputstr'])
            | Q(M_class__icontains=data['inputstr'])).values()
        dish_list = list(obj_dish)
        return JsonResponse({"code": 1, "data": dish_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "查询菜品信息异常，具体错误：" + str(e)})


def is_exist_M_id(request):
    """查询菜品编号是否存在"""
    # 接收传递过来的编号
    data = json.loads(request.body.decode('utf-8'))
    obj_dish = Menu.objects.filter(M_id=data['M_id'])
    try:
        if obj_dish.count() == 0:
            return JsonResponse({'code': 1, 'exist': False})
        else:
            return JsonResponse({'code': 1, 'exist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验编号失败，原因：{e}" + str(e)})


def add_dish(request):
    """添加菜品信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_new_dish = Menu(M_id=data['M_id'], M_name=data['M_name'],
                            M_class=data['M_class'], M_price=data['M_price'], )
        # 执行添加
        obj_new_dish.save()
        # 使用ORM获取所有菜品信息
        obj_menu = Menu.objects.all().values()
        # 把结果转为List
        menu = list(obj_menu)
        return JsonResponse({"code": 1, "data": menu})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取菜品信息异常，具体错误：" + str(e)})


def update_dish(request):
    """修改菜品信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_dish = Menu.objects.get(M_id=data['M_id'])
        # 依次修改
        obj_dish.M_name = data['M_name']
        obj_dish.M_class = data['M_class']
        obj_dish.M_price = data['M_price']
        # 保存
        obj_dish.save()
        # 使用ORM获取所有菜品信息
        obj_menu = Menu.objects.all().values()
        # 把结果转为List
        menu = list(obj_menu)
        return JsonResponse({"code": 1, "data": menu})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取菜品信息异常，具体错误：" + str(e)})


def delete_dish(request):
    """删除菜品信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_dish = Menu.objects.get(M_id=data['M_id'])
        # 执行删除
        obj_dish.delete()
        # 使用ORM获取所有菜品信息
        obj_menu = Menu.objects.all().values()
        # 把结果转为List
        menu = list(obj_menu)
        return JsonResponse({"code": 1, "data": menu})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取菜品信息异常，具体错误：" + str(e)})


def get_foodTable(request):
    """获取所有餐桌信息"""
    try:
        # 使用ORM获取所有菜品信息
        obj_foodTable = FoodTable.objects.all().values()
        # 把结果转为List
        foodTable = list(obj_foodTable)
        return JsonResponse({"code": 1, "data": foodTable})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取餐桌信息异常，具体错误：" + str(e)})


def is_exist_Ft_id(request):
    """查询餐桌号是否存在"""
    # 接收传递过来的编号
    data = json.loads(request.body.decode('utf-8'))
    obj_table = FoodTable.objects.filter(Ft_id=data['Ft_id'])
    try:
        if obj_table.count() == 0:
            return JsonResponse({'code': 1, 'exist': False})
        else:
            return JsonResponse({'code': 1, 'exist': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验编号失败，原因：{e}" + str(e)})


def add_foodTable(request):
    """添加餐桌信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_new_table = FoodTable(Ft_id=data['Ft_id'], Ft_number=data['Ft_number'], )
        # 执行添加
        obj_new_table.save()
        # 使用ORM获取所有菜品信息
        obj_foodTable = FoodTable.objects.all().values()
        # 把结果转为List
        foodTable = list(obj_foodTable)
        return JsonResponse({"code": 1, "data": foodTable})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "添加餐桌信息异常，具体错误：" + str(e)})


def update_foodTable(request):
    """修改餐桌信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_table = FoodTable.objects.get(Ft_id=data['Ft_id'])
        # 依次修改
        obj_table.Ft_number = data['Ft_number']
        obj_table.Ft_state = data['Ft_state']
        # 保存
        obj_table.save()
        # 使用ORM获取所有菜品信息
        obj_foodTable = FoodTable.objects.all().values()
        # 把结果转为List
        foodTable = list(obj_foodTable)
        return JsonResponse({"code": 1, "data": foodTable})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "添加餐桌信息异常，具体错误：" + str(e)})


def delete_foodTable(request):
    """删除餐桌信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的员工信息，并把对象转为字典格式
        obj_table = FoodTable.objects.get(Ft_id=data['Ft_id'])
        # 执行删除
        obj_table.delete()
        # 使用ORM获取所有菜品信息
        obj_foodTable = FoodTable.objects.all().values()
        # 把结果转为List
        foodTable = list(obj_foodTable)
        return JsonResponse({"code": 1, "data": foodTable})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "添加餐桌信息异常，具体错误：" + str(e)})


def get_Order(request):
    """获取订单信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取订单信息
        obj_order = Order.objects.filter(O_state=data['O_state']).values()
        # 将时间转化成指定格式
        for order in obj_order:
            order['O_time'] = order['O_time'].strftime('%Y-%m-%d %H:%M:%S')
        # 把结果转为List
        order_list = list(obj_order)
        return JsonResponse({"code": 1, "data": order_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取订单信息异常，具体错误：" + str(e)})


def get_OrderDetail(request):
    """获取订单详细信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取订单信息
        obj_detail = Menu_Order.objects.filter(O_id=data['O_id']).values()
        order_list = []
        for obj_one in obj_detail:
            obj_detail_Mid = obj_one['M_id_id']
            obj_dish_name = Menu.objects.filter(M_id=obj_detail_Mid).values().first()
            obj_one['M_name'] = obj_dish_name['M_name']
            order_list.append(obj_one)
        return JsonResponse({"code": 1, "data": order_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取订单信息异常，具体错误：" + str(e)})


def query_order(request):
    """查询订单信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取订单信息
        obj_order = Order.objects.filter(Q(O_state=data['state']) & (
                Q(O_id__icontains=data['inputstr']) | Q(C_account__C_account__icontains=data['inputstr']))).values()
        # 将时间转化成指定格式
        for order in obj_order:
            order['O_time'] = order['O_time'].strftime('%Y-%m-%d %H:%M:%S')
        # 把结果转为List
        order_list = list(obj_order)
        print(order_list)
        return JsonResponse({"code": 1, "data": order_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取订单信息异常，具体错误：" + str(e)})


def delete_Order(request):
    """删除订单信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的订单信息
        obj_Order_e = Order.objects.get(O_id=data['O_id'])
        # 执行删除
        obj_Order_e.delete()
        # 使用ORM获取满足条件的点菜信息
        obj_Order_f = Menu_Order.objects.filter(O_id=data['O_id'])
        # 执行删除
        obj_Order_f.delete()
        # 使用ORM获取订单信息
        obj_order = Order.objects.filter(O_state='已支付').values()
        # 将时间转化成指定格式
        for order in obj_order:
            order['O_time'] = order['O_time'].strftime('%Y-%m-%d %H:%M:%S')
        # 把结果转为List
        order_list = list(obj_order)
        return JsonResponse({"code": 1, "data": order_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取订单信息异常，具体错误：" + str(e)})


def finish_Order(request):
    """完成订单"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取订单信息
        obj_order = Order.objects.get(O_id=data['O_id'])
        obj_order.O_state = '已支付'
        obj_order.save()
        # 使用ORM获取订单信息
        obj_order = Order.objects.filter(O_state='未支付').values()
        # 将时间转化成指定格式
        for order in obj_order:
            order['O_time'] = order['O_time'].strftime('%Y-%m-%d %H:%M:%S')
        # 把结果转为List
        order_list = list(obj_order)
        return JsonResponse({"code": 1, "data": order_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取订单信息异常，具体错误：" + str(e)})


def home_data(request):
    """获取首页所需数据"""
    try:
        # ------------------------查询今日/本月已支付订单数和总收入-------------------
        today = timezone.now().replace(hour=0, minute=0, second=0)
        month = timezone.now().date()
        # 获取本月的第一天和最后一天
        first_day_of_month = month.replace(day=1)
        if month.month!=12:
            last_day_of_month = month.replace(month=month.month + 1, day=1)  # 不同月份天数不同
        else:
            last_day_of_month = month.replace(month=month.month, day=31)  # 不同月份天数不同
        # 查询今日已支付订单数和总收入
        today_paid_data = Order.objects.filter(O_time__date=today, O_state='已支付').aggregate(
            order_count=Count('O_id'),
            total_income=Coalesce(Sum('O_cost'), 0)
        )
        # 查询本月已支付订单数和总收入
        month_paid_data = Order.objects.filter(O_time__date__range=[first_day_of_month, last_day_of_month],
                                               O_state='已支付').aggregate(
            order_count=Count('O_id'),
            total_income=Coalesce(Sum('O_cost'), 0)
        )
        result_list = [
            {'today_order_count': today_paid_data['order_count'],
             'today_total_income': today_paid_data['total_income'],
             'month_paid_data': month_paid_data['order_count'],
             'month_total_income': month_paid_data['total_income']}
        ]
        # ------------------------查询近五天已支付订单数和总收入-------------------
        # 定义日期范围
        date_range = [today - timedelta(days=i) for i in range(4, -1, -1)]
        serial_list = []
        # 循环查询每一天的已支付订单数和总收入
        for day in date_range:
            paid_data = Order.objects.filter(O_time__date=day, O_state='已支付').aggregate(
                order_count=Count('O_id'),
                total_income=Coalesce(Sum('O_cost'), 0)
            )
            each_data = {'day': day.strftime('%m-%d'), 'order_count': paid_data['order_count'],
                         'total_income': paid_data['total_income']}
            serial_list.append(each_data)
        # print(serial_list)
        # ------------------------查询菜品销量-------------------
        # 计算每道菜的总数量
        menu_totals = (
            Menu_Order.objects
            .values('M_id__M_name')  # 按照菜品名称分组
            .annotate(total_quantity=Coalesce(Sum('M_num'), 0))  # 计算总数量，Coalesce 用于处理没有订单的情况
            .order_by('-total_quantity')  # 根据总数量降序排序
        )
        order_list = list(menu_totals)
        return JsonResponse(
            {"code": 1, "dish_data": order_list, "order_data": result_list, "echarts_data": serial_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取信息异常，具体错误：" + str(e)})


def get_user(request):
    """获取所有用户信息"""
    try:
        # 使用ORM获取所有信息
        obj_user = User.objects.exclude(authority='2').values()
        user_list = []
        for user in obj_user:
            if user['authority'] == '0':
                user['Authority'] = '店长'
            elif user['authority'] == '1':
                user['Authority'] = '副店长'
            user_list.append(user)
        return JsonResponse({"code": 1, "data": user_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取用户信息异常，具体错误：" + str(e)})


def update_user(request):
    """更新用户信息"""
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的信息，并把对象转为字典格式
        obj_User = User.objects.get(account=data['account'])
        # 依次修改
        obj_User.authority = data['authority']
        # 保存
        obj_User.save()
        # 使用ORM获取所有信息
        obj_user = User.objects.exclude(authority='2').values()
        user_list = []
        for user in obj_user:
            if user['authority'] == '0':
                user['Authority'] = '店长'
            elif user['authority'] == '1':
                user['Authority'] = '副店长'
            user_list.append(user)
        return JsonResponse({"code": 1, "data": user_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取用户信息异常，具体错误：" + str(e)})


def delete_user(request):
    """删除用户信息"""
    # 接收传递过来的查询条件---axios默认的是json格式---转为字典类型
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的信息
        obj_User = User.objects.get(account=data['account'])
        # 执行删除
        obj_User.delete()
        # 使用ORM获取所有信息
        obj_user = User.objects.exclude(authority='2').values()
        user_list = []
        for user in obj_user:
            if user['authority'] == '0':
                user['Authority'] = '店长'
            elif user['authority'] == '1':
                user['Authority'] = '副店长'
            user_list.append(user)
        return JsonResponse({"code": 1, "data": user_list})
    except Exception as e:
        return JsonResponse({"code": 0, "msg": "获取用户信息异常，具体错误：" + str(e)})


def get_random_str():
    # 获取uuid随机数
    uuid_val = uuid.uuid4()
    # 获取uuid随机数字符串
    uuid_str = str(uuid_val).encode("utf_8")
    # 获取md5实例
    md5 = hashlib.md5()
    # 拿取uuid的md5摘要
    md5.update(uuid_str)
    # 返回固定长度的字符串
    return md5.hexdigest()


def write_to_excel(data: list, path: str, title):
    """把数据写入excel"""
    # 实例化一个workbook
    workbook = openpyxl.Workbook()
    # 激活一个sheet
    sheet = workbook.active
    # 为sheet命名
    sheet.title = title
    # 准备key
    keys = data[0].keys()
    # 准备写入
    for index, item in enumerate(data):
        # 遍历每个元素
        for k, v in enumerate(keys):
            sheet.cell(row=index + 1, column=k + 1, value=str(item[v]))
    # 写入
    workbook.save(path)


def export_excel(request):
    """导出数据到excel"""
    data = json.loads(request.body.decode('utf-8'))
    if data['name'] == "Menu":
        # 获取所有信息
        obj_info = Menu.objects.all().values()
    elif data['name'] == "Worker":
        # 获取所有信息
        obj_info = Worker.objects.all().values()
    elif data['name'] == "Customer":
        # 获取所有信息
        obj_info = Customer.objects.all().values()
    # 转为list
    info = list(obj_info)
    # 准备名称
    excel_name = get_random_str() + ".xlsx"
    # 准备写入的路径
    path = os.path.join(settings.MEDIA_ROOT, excel_name)
    # 写入
    write_to_excel(info, path, data['name'])
    # 返回
    return JsonResponse({'code': 1, 'name': excel_name})
