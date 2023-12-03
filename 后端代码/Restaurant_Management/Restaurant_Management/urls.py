"""
URL configuration for Restaurant_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appSite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),#登录
    path('register/', views.register),#注册
    path('register/check/', views.is_exist_Username),#校验用户名
    path('home/', views.home_data),#获取首页数据
    path('home/modifypassword/', views.modify_password),#修改密码
    path('customer/', views.get_customer),#获取所有顾客信息
    path('customer/query/', views.query_customer),#查询员工信息
    path('worker/', views.get_worker),#获取所有员工信息
    path('worker/query/', views.query_worker),#查询员工信息
    path('worker/check/', views.is_exist_W_id),#检验员工工号是否存在
    path('worker/add/', views.add_worker),#添加员工信息
    path('worker/update/', views.update_worker),#修改员工信息
    path('worker/delete/', views.delete_worker),#删除员工信息
    path('dish/', views.get_dish),#获取所有菜品信息
    path('dish/query/', views.query_dish),#查询菜品信息
    path('dish/check/', views.is_exist_M_id),#检验菜品编号是否存在
    path('dish/add/', views.add_dish),#添加菜品信息
    path('dish/update/', views.update_dish),#修改菜品信息
    path('dish/delete/', views.delete_dish),#删除菜品信息
    path('foodTable/', views.get_foodTable),#获取所有餐桌信息
    path('foodTable/check/', views.is_exist_Ft_id),  # 检验餐桌号是否存在
    path('foodTable/add/', views.add_foodTable),  # 添加餐桌信息
    path('foodTable/update/', views.update_foodTable),  # 修改餐桌信息
    path('foodTable/delete/', views.delete_foodTable),  # 删除餐桌信息
    path('order/', views.get_Order),  # 获取订单信息
    path('order/detail/', views.get_OrderDetail),  # 获取订单详细信息
    path('order/query/', views.query_order),#查询菜品信息
    path('order/delete/', views.delete_Order),#删除订单信息
    path('order/finish/', views.finish_Order),#删除订单信息
    path('manage/', views.get_user),#获取所有用户信息
    path('manage/update/', views.update_user),#修改用户信息
    path('manage/delete/', views.delete_user),#删除用户信息
    path('excel/export/', views.export_excel),  #将信息写入Excel
]

#允许media中所有的文件被访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)