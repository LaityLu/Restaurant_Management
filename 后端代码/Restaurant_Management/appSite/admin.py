from django.contrib import admin
from appSite.models import User
from appSite.models import Customer
from appSite.models import Menu
from appSite.models import FoodTable
from appSite.models import Worker
from appSite.models import Order
from appSite.models import Menu_Order
# Register your models here.


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['account', 'password', 'authority']

@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['C_account', 'C_name', 'C_sex', 'C_birth', 'C_phone', 'C_ordernum']

@admin.register(Menu)
class AdminMenu(admin.ModelAdmin):
    list_display = ['M_id', 'M_name', 'M_class', 'M_price']

@admin.register(FoodTable)
class AdminFoodTable(admin.ModelAdmin):
    list_display = ['Ft_id', 'Ft_number', 'Ft_state']

@admin.register(Worker)
class AdminWorker(admin.ModelAdmin):
    list_display = ['W_id', 'W_name', 'W_sex', 'W_birth', 'W_job', 'W_phone', 'W_salary', 'W_addr']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['O_id', 'W_id', 'C_account', 'O_time', 'Ft_id', 'O_cost', 'O_state']

@admin.register(Menu_Order)
class AdminMenu_Oder(admin.ModelAdmin):
    list_display = ['id', 'O_id','M_num', 'M_cost']