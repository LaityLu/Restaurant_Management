from django.db import models

# Create your models here.
class User(models.Model):
    """用户信息"""
    account = models.CharField(max_length=10, verbose_name='账号', primary_key=True)
    password = models.CharField(max_length=100, verbose_name='密码')
    choices = (('1', '副店长'), ('0', '店长'),('2', '管理员'),)
    authority = models.CharField(max_length=5, choices=choices, default='1', verbose_name='身份')


class Customer(models.Model):
    """顾客信息"""
    C_account = models.CharField(max_length=10, verbose_name='账号', primary_key=True)
    C_name = models.CharField(max_length=10, verbose_name='姓名')
    choices = (
        ('男', '男'),
        ('女', '女'),
    )
    C_sex = models.CharField(max_length=5, choices=choices, verbose_name='性别')
    C_birth = models.DateField(max_length=20, verbose_name='出生日期')
    C_phone = models.CharField(max_length=11, verbose_name='电话', unique=True)
    C_ordernum = models.IntegerField(verbose_name='完成订单数', default=0)
    def __str__(self):
        return self.C_account

class Menu(models.Model):
    """菜单信息"""
    M_id = models.CharField(primary_key=True, max_length=10, verbose_name='菜品编号')
    M_name = models.CharField(max_length=10, verbose_name='菜名', unique=True)
    M_class = models.CharField(max_length=10, verbose_name='类别')
    M_price = models.IntegerField(verbose_name='价格')

    def __str__(self):
        return f"{self.M_name} - {self.M_price}"


class FoodTable(models.Model):
    """餐桌信息"""
    Ft_id = models.CharField(primary_key=True, max_length=10, verbose_name='餐桌号')
    Ft_number = models.IntegerField(verbose_name='座位数')
    choices = (
        ('使用中', '使用中'),
        ('待清洁', '待清洁'),
        ('空闲', '空闲'),
    )
    Ft_state = models.CharField(max_length=10, choices=choices, default='空闲', verbose_name='状态')
    def __str__(self):
        return self.Ft_id

class Worker(models.Model):
    """员工信息"""
    W_id = models.CharField(primary_key=True, max_length=10, verbose_name='工号')
    W_name = models.CharField(max_length=10, verbose_name='姓名')
    choices = (
        ('男', '男'),
        ('女', '女'),
    )
    W_sex = models.CharField(max_length=5, choices=choices, verbose_name='性别')
    W_birth = models.DateField(max_length=20, verbose_name='出生日期')
    job = (('服务员', '服务员'), ('厨师', '厨师'), ('保洁', '保洁'),)
    W_job = models.CharField(max_length=10, choices=job, verbose_name='职务')
    W_phone = models.CharField(max_length=11, verbose_name='电话', unique=True)
    W_salary = models.IntegerField(verbose_name='工资')
    W_addr = models.CharField(max_length=30, verbose_name='家庭住址')
    def __str__(self):
        return self.W_id

class Order(models.Model):
    """订单信息"""
    O_id = models.CharField(primary_key=True, max_length=10, verbose_name='订单号')
    W_id = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, to_field='W_id', verbose_name='服务员工号')
    C_account = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='C_account', verbose_name='顾客账号')
    O_time = models.DateTimeField(max_length=20, verbose_name='消费时间')
    Ft_id = models.ForeignKey(FoodTable, on_delete=models.CASCADE, to_field='Ft_id', verbose_name='餐桌号')
    O_cost = models.IntegerField(verbose_name='消费金额')
    choices = (
        ('未支付', '未支付'),
        ('已支付', '已支付'),
    )
    O_state = models.CharField(max_length=10, choices=choices, default='未支付', verbose_name='订单状态')
    def __str__(self):
        return self.O_id

class Menu_Order(models.Model):
    """点餐信息"""
    id = models.AutoField(primary_key=True)
    O_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单号')
    M_id = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field='M_id', related_name='menu_orders_by_id', verbose_name='菜品编号')
    M_num = models.IntegerField(verbose_name='菜品数量')
    M_cost = models.IntegerField(verbose_name='总价格', default=0)
    unique_together = (("O_id", "M_id"),)

